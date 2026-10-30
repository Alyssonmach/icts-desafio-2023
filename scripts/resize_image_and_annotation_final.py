"""Resize LabelMe images and scale polygon annotations to 640x360 by default."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import cv2


def resize_dataset(
    input_dir: Path, output_dir: Path, width: int = 640, height: int = 360
) -> int:
    """Resize annotated JPG files and return the number of images resized."""
    if width <= 0 or height <= 0:
        raise ValueError("A largura e a altura devem ser maiores que zero.")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Diretório de entrada não encontrado: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    resized_count = 0

    for image_path in sorted(input_dir.glob("*.jpg")):
        annotation_path = image_path.with_suffix(".json")
        if not annotation_path.is_file():
            print(f"Ignorando imagem sem anotação: {image_path.name}")
            continue

        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Não foi possível ler a imagem: {image_path}")

        with annotation_path.open(encoding="utf-8") as file:
            annotation: dict[str, Any] = json.load(file)
        if not isinstance(annotation, dict):
            raise ValueError(f"Anotação deve ser um objeto JSON em {annotation_path}")
        shapes = annotation.get("shapes")
        if not isinstance(shapes, list):
            raise ValueError(f"Campo 'shapes' ausente ou inválido em {annotation_path}")

        original_height, original_width = image.shape[:2]
        if original_width == 0 or original_height == 0:
            raise ValueError(f"Imagem com dimensões inválidas: {image_path}")

        scale_x = width / original_width
        scale_y = height / original_height
        for shape in shapes:
            if not isinstance(shape, dict):
                raise ValueError(f"Forma inválida em {annotation_path}: {shape!r}")
            points = shape.get("points")
            if not isinstance(points, list) or any(
                not isinstance(point, (list, tuple)) or len(point) != 2
                for point in points
            ):
                raise ValueError(
                    f"Anotação sem lista de pontos em {annotation_path}: {shape!r}"
                )
            shape["points"] = [
                [float(x) * scale_x, float(y) * scale_y] for x, y in points
            ]

        if (original_width, original_height) != (width, height):
            image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
            resized_count += 1

        # Embedded imageData refers to the original image and would become stale.
        annotation["imageData"] = None
        annotation["imagePath"] = image_path.name
        annotation["imageWidth"] = width
        annotation["imageHeight"] = height

        output_image_path = output_dir / image_path.name
        if not cv2.imwrite(str(output_image_path), image):
            raise OSError(f"Não foi possível salvar a imagem: {output_image_path}")
        with (output_dir / annotation_path.name).open("w", encoding="utf-8") as file:
            json.dump(annotation, file, ensure_ascii=False, indent=2)

    return resized_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Redimensiona imagens e polígonos de anotações LabelMe."
    )
    parser.add_argument(
        "-t",
        "--path_imgs_annotation",
        required=True,
        type=Path,
        help="Diretório com imagens JPG e seus arquivos JSON do LabelMe.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("sized_data"),
        help="Diretório de saída (padrão: ./sized_data).",
    )
    parser.add_argument("--width", type=int, default=640, help="Largura de saída.")
    parser.add_argument("--height", type=int, default=360, help="Altura de saída.")
    args = parser.parse_args()

    count = resize_dataset(
        args.path_imgs_annotation, args.output_dir, args.width, args.height
    )
    print(f"Imagens redimensionadas: {count}")


if __name__ == "__main__":
    main()
