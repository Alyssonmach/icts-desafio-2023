"""Convert a directory of LabelMe polygon annotations to COCO JSON."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def polygon_area(points: list[list[float]]) -> float:
    """Return polygon area using the shoelace formula."""
    return abs(
        sum(
            points[index][0] * points[(index + 1) % len(points)][1]
            - points[(index + 1) % len(points)][0] * points[index][1]
            for index in range(len(points))
        )
    ) / 2


def convert_labelme_jsons(annotation_paths: list[Path]) -> dict[str, Any]:
    """Convert sorted LabelMe JSON paths into a COCO instance segmentation object."""
    labels: set[str] = set()
    records: list[tuple[Path, dict[str, Any]]] = []
    for path in annotation_paths:
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError(f"Anotação deve ser um objeto JSON em {path}")
        if not isinstance(data.get("shapes"), list):
            raise ValueError(f"Campo 'shapes' ausente ou inválido em {path}")
        for shape in data["shapes"]:
            if not isinstance(shape, dict):
                raise ValueError(f"Forma inválida em {path}: {shape!r}")
            label = shape.get("label")
            if not isinstance(label, str) or not label:
                raise ValueError(f"Rótulo ausente em {path}: {shape!r}")
            labels.add(label)
        records.append((path, data))

    category_ids = {label: index for index, label in enumerate(sorted(labels), start=1)}
    images: list[dict[str, Any]] = []
    annotations: list[dict[str, Any]] = []
    annotation_id = 1

    for image_id, (path, data) in enumerate(records, start=1):
        width = data.get("imageWidth")
        height = data.get("imageHeight")
        if not isinstance(width, (int, float)) or not isinstance(height, (int, float)):
            raise ValueError(f"Dimensões da imagem ausentes ou inválidas em {path}")
        if width <= 0 or height <= 0:
            raise ValueError(f"Dimensões da imagem devem ser positivas em {path}")

        image_path = Path(data.get("imagePath") or path.with_suffix(".jpg").name)
        images.append(
            {
                "id": image_id,
                "file_name": image_path.name,
                "width": int(width),
                "height": int(height),
            }
        )

        for shape in data["shapes"]:
            raw_points = shape.get("points")
            if not isinstance(raw_points, list) or len(raw_points) < 3:
                raise ValueError(f"Polígono inválido em {path}: {shape!r}")
            try:
                points = []
                for point in raw_points:
                    if not isinstance(point, (list, tuple)) or len(point) != 2:
                        raise ValueError
                    x, y = float(point[0]), float(point[1])
                    if not math.isfinite(x) or not math.isfinite(y):
                        raise ValueError
                    points.append([x, y])
            except (TypeError, ValueError) as error:
                raise ValueError(f"Coordenadas inválidas em {path}: {shape!r}") from error

            x_values = [point[0] for point in points]
            y_values = [point[1] for point in points]
            x_min, x_max = min(x_values), max(x_values)
            y_min, y_max = min(y_values), max(y_values)
            annotations.append(
                {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": category_ids[shape["label"]],
                    "segmentation": [
                        coordinate for point in points for coordinate in point
                    ],
                    "area": polygon_area(points),
                    "bbox": [x_min, y_min, x_max - x_min, y_max - y_min],
                    "iscrowd": 0,
                }
            )
            annotation_id += 1

    categories = [
        {"id": category_ids[label], "name": label, "supercategory": label}
        for label in sorted(labels)
    ]
    return {"images": images, "annotations": annotations, "categories": categories}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converte anotações poligonais LabelMe para o formato COCO."
    )
    parser.add_argument(
        "labelme_images",
        type=Path,
        help="Diretório com arquivos JSON de anotação LabelMe.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("trainval.json"),
        help="Caminho do COCO JSON gerado (padrão: ./trainval.json).",
    )
    args = parser.parse_args()

    if not args.labelme_images.is_dir():
        parser.error(f"Diretório não encontrado: {args.labelme_images}")
    annotation_paths = sorted(args.labelme_images.glob("*.json"))
    if not annotation_paths:
        parser.error(f"Nenhum arquivo JSON encontrado em {args.labelme_images}")

    coco = convert_labelme_jsons(annotation_paths)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as file:
        json.dump(coco, file, ensure_ascii=False, indent=2)
    print(
        f"COCO salvo em {args.output}: {len(coco['images'])} imagens, "
        f"{len(coco['annotations'])} anotações, {len(coco['categories'])} categorias."
    )


if __name__ == "__main__":
    main()
