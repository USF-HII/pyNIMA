from __future__ import annotations


def read_pedigree_map(fam_path: str) -> dict[str, tuple[str, str]]:
    pedigree_map: dict[str, tuple[str, str]] = {}
    with open(fam_path, encoding="utf-8") as handle:
        for line in handle:
            parts = line.strip().split()
            if len(parts) >= 4:
                _, subject_id, pat, mat = parts[:4]
                pedigree_map[subject_id] = (pat, mat)
    return pedigree_map


def read_raw_variant_index(raw_path: str) -> tuple[list[str], dict[str, int]]:
    with open(raw_path, encoding="utf-8") as handle:
        header_line = handle.readline().rstrip("\r\n")
    header_cols = header_line.split(" ")
    variant_ids = header_cols[6:]
    variant_col_index = {snp: idx for idx, snp in enumerate(variant_ids, start=6)}
    return variant_ids, variant_col_index


def write_matrix_tsv(
    output_path: str,
    subject_variant_map: dict[str, dict[str, str]],
    variant_ids: list[str],
    missing_value: str = "NA",
) -> None:
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(" \t" + "\t".join(variant_ids) + "\n")
        for subject_id, variant_map in subject_variant_map.items():
            row_vals = [str(variant_map.get(var_id, missing_value)) for var_id in variant_ids]
            handle.write(subject_id + "\t" + "\t".join(row_vals) + "\n")
