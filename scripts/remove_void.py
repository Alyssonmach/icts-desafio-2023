"""Remove shapes labelled ``void`` from LabelMe JSON annotations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def remove_void_annotations(input_dir: Path, output_dir: Path) -> tuple[int, int]:
    """Write corrected JSON files and return (file count, removed shape count)."""
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Diretório de entrada não encontrado: {input_dir}")

    annotation_paths = sorted(input_dir.glob("*.json"))
    if not annotation_paths:
        raise FileNotFoundError(f"Nenhum arquivo JSON encontrado em {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    removed_count = 0

    for annotation_path in annotation_paths:
        with annotation_path.open(encoding="utf-8") as file:
            annotation: dict[str, Any] = json.load(file)
        if not isinstance(annotation, dict):
            raise ValueError(f"Anotação deve ser um objeto JSON em {annotation_path}")

        shapes = annotation.get("shapes", [])
        if not isinstance(shapes, list):
            raise ValueError(f"Campo 'shapes' inválido em {annotation_path}")
        if any(not isinstance(shape, dict) for shape in shapes):
            raise ValueError(f"Forma inválida no campo 'shapes' de {annotation_path}")

        filtered_shapes = [
            shape
            for shape in shapes
            if str(shape.get("label", "")).casefold() != "void"
        ]
        removed_from_file = len(shapes) - len(filtered_shapes)
        removed_count += removed_from_file
        annotation["shapes"] = filtered_shapes

        output_path = output_dir / annotation_path.name
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(annotation, file, ensure_ascii=False, indent=2)
        print(f"{annotation_path.name}: removidos {removed_from_file} rótulos void")

    return len(annotation_paths), removed_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove polígonos com o rótulo 'void' dos JSONs do LabelMe."
    )
    parser.add_argument(
        "-t",
        "--path_annotation_jsons",
        required=True,
        type=Path,
        help="Diretório com os arquivos JSON de anotação.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("newjsons"),
        help="Diretório de saída (padrão: ./newjsons).",
    )
    args = parser.parse_args()

    file_count, removed_count = remove_void_annotations(
        args.path_annotation_jsons, args.output_dir
    )
    print(f"Arquivos processados: {file_count}; rótulos void removidos: {removed_count}")


if __name__ == "__main__":
    main()
