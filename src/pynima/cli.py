from __future__ import annotations

import argparse
from pathlib import Path
import time

from pynima.core import run_nima_calling
from pynima.io import read_pedigree_map, read_raw_variant_index, write_matrix_tsv


def parse_threads_arg(value: str) -> int | str:
    if value == "max":
        return "max"
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("--threads must be a positive integer or 'max'")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pynima",
        description="Call Non-Inherited Maternal Allele (NIMA) and MER matrices from PLINK files.",
    )
    parser.add_argument("-i", "--raw", required=True, help="Path to PLINK additive (.raw) file")
    parser.add_argument("-f", "--fam", required=True, help="Path to PLINK pedigree (.fam) file")
    parser.add_argument(
        "-t",
        "--threads",
        type=parse_threads_arg,
        default=1,
        help="Number of worker processes or 'max' (default: 1)",
    )
    parser.add_argument(
        "-o",
        "--output-prefix",
        required=True,
        help="Output path prefix (writes <prefix>_nima.tsv and <prefix>_mer.tsv)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    start_time = time.perf_counter()
    pedigree_map = read_pedigree_map(args.fam)
    variant_ids, variant_col_index = read_raw_variant_index(args.raw)

    nima_matrix, mer_matrix = run_nima_calling(
        raw_path=args.raw,
        variant_ids=variant_ids,
        variant_col_index=variant_col_index,
        pedigree_map=pedigree_map,
        threads=args.threads,
    )

    out_prefix = Path(args.output_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    write_matrix_tsv(f"{args.output_prefix}_nima.tsv", nima_matrix, variant_ids)
    write_matrix_tsv(f"{args.output_prefix}_mer.tsv", mer_matrix, variant_ids)

    elapsed = time.perf_counter() - start_time
    print(f"Processed {len(variant_ids)} variants in {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
