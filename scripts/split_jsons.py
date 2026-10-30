"""Copy LabelMe JSON files into the repository's fixed train/val/test splits."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPLIT_DIR = REPOSITORY_ROOT / "guia-estratificacao-arquivos"


def read_split(path: Path) -> set[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo de divisão não encontrado: {path}")
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def split_annotations(
    input_dir: Path, split_dir: Path, output_dir: Path
) -> dict[str, int]:
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Diretório de entrada não encontrado: {input_dir}")

    splits = {
        "train": read_split(split_dir / "train.txt"),
        "val": read_split(split_dir / "val.txt"),
        "test": read_split(split_dir / "test.txt"),
    }

    owner: dict[str, str] = {}
    for split_name, names in splits.items():
        for name in names:
            previous = owner.setdefault(name, split_name)
            if previous != split_name:
                raise ValueError(
                    f"O arquivo {name!r} aparece em {previous} e {split_name}."
                )

    source_paths = {path.name: path for path in input_dir.glob("*.json")}
    counts: dict[str, int] = {}
    for split_name, names in splits.items():
        destination = output_dir / f"{split_name}_jsons"
        destination.mkdir(parents=True, exist_ok=True)
        matched_names = sorted(names & source_paths.keys())
        for name in matched_names:
            shutil.copy2(source_paths[name], destination / name)
        missing_count = len(names - source_paths.keys())
        counts[split_name] = len(matched_names)
        print(
            f"{split_name}: copiados {len(matched_names)}; "
            f"ausentes na entrada {missing_count}"
        )

    unassigned_count = len(source_paths.keys() - owner.keys())
    print(f"JSONs sem divisão definida: {unassigned_count}")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estratifica JSONs usando os arquivos fixos train/val/test."
    )
    parser.add_argument(
        "-t",
        "--path_annotation_jsons",
        required=True,
        type=Path,
        help="Diretório com os arquivos JSON de anotação.",
    )
    parser.add_argument(
        "--split-dir",
        type=Path,
        default=DEFAULT_SPLIT_DIR,
        help=(
            "Diretório com train.txt, val.txt e test.txt "
            f"(padrão: {DEFAULT_SPLIT_DIR})."
        ),
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("splitting_jsons"),
        help="Diretório de saída (padrão: ./splitting_jsons).",
    )
    args = parser.parse_args()

    split_annotations(args.path_annotation_jsons, args.split_dir, args.output_dir)


if __name__ == "__main__":
    main()
