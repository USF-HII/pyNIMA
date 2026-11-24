from __future__ import annotations

from collections import defaultdict
from functools import partial
import multiprocessing
from typing import Iterable


def call_nima(
    i1: str,
    i2: str,
    m1: str,
    m2: str,
    f1: str,
    f2: str,
) -> str:
    """Call Non-Inherited Maternal Allele (NIMA) for an individual given parents."""
    if "NA" in (m1, m2):
        return "NA"

    a = i1 in (m1, m2)
    _b = i1 in (f1, f2)
    c = i2 in (m1, m2)
    _d = i2 in (f1, f2)

    if not a and not c:
        return "MEND_ERR"

    if m1 == m2:
        return "0"

    nima = "NA"
    if i1 == i2:
        if a and c:
            if i1 == m1:
                nima = m2
            elif i1 == m2:
                nima = m1
    elif sorted([i1, i2]) == sorted([m1, m2]):
        nima = "0"
    elif a and not c:
        if i1 == m1:
            nima = m2
        elif i1 == m2:
            nima = m1
    elif not a and c:
        if i2 == m1:
            nima = m2
        elif i2 == m2:
            nima = m1

    return nima


def check_mer(
    i1: str,
    i2: str,
    m1: str,
    m2: str,
    f1: str,
    f2: str,
) -> str:
    """Check Mendelian inheritance error (MER) for an individual and available parents."""
    a = i1 in (m1, m2)
    b = i1 in (f1, f2)
    c = i2 in (m1, m2)
    d = i2 in (f1, f2)

    if "NA" not in (i1, i2):
        # Only mother data available
        if "NA" not in (m1, m2) and "NA" in (f1, f2):
            return "1" if (not a and not c) else "0"

        # Only father data available
        if "NA" in (m1, m2) and "NA" not in (f1, f2):
            return "1" if (not b and not d) else "0"

        # Both parents data available
        if "NA" not in (m1, m2, f1, f2):
            if (not a and not c) or (not b and not d):
                return "1"
            if (not a and not b) or (not c and not d):
                return "1"
            return "0"

    return "NA"


def genotype_to_alleles(allele_count: str, variant_id: str) -> list[str]:
    if allele_count == "0":
        return ["dom", "dom"]
    if allele_count == "1":
        return [variant_id, "dom"]
    if allele_count == "2":
        return [variant_id, variant_id]
    return ["NA", "NA"]


def chunk_items(items: list[str], n_chunks: int) -> list[list[str]]:
    if n_chunks <= 1 or len(items) <= 1:
        return [items] if items else []
    chunk_size = max(1, round(len(items) / n_chunks))
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def call_variant_for_subject(
    subject_id: str,
    variant_id: str,
    allele_map: dict[str, list[str]],
    pedigree_map: dict[str, tuple[str, str]],
) -> tuple[str, str]:
    pat, mat = pedigree_map.get(subject_id, ("NA", "NA"))
    subj_alleles = allele_map[subject_id]
    pat_alleles = allele_map.get(pat, ["NA", "NA"])
    mat_alleles = allele_map.get(mat, ["NA", "NA"])

    nima_raw = call_nima(
        subj_alleles[0],
        subj_alleles[1],
        mat_alleles[0],
        mat_alleles[1],
        pat_alleles[0],
        pat_alleles[1],
    )
    mer = check_mer(
        subj_alleles[0],
        subj_alleles[1],
        mat_alleles[0],
        mat_alleles[1],
        pat_alleles[0],
        pat_alleles[1],
    )

    if nima_raw == variant_id:
        nima = "1"
    elif nima_raw == "dom":
        nima = "0"
    else:
        nima = str(nima_raw)

    return nima, str(mer)


def process_variant_chunk(
    variant_chunk: list[str],
    raw_path: str,
    pedigree_map: dict[str, tuple[str, str]],
    variant_col_index: dict[str, int],
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    out_nima: dict[str, dict[str, str]] = defaultdict(dict)
    out_mer: dict[str, dict[str, str]] = defaultdict(dict)

    for variant_id in variant_chunk:
        allele_map: dict[str, list[str]] = {}
        col_idx = variant_col_index[variant_id]

        with open(raw_path, encoding="utf-8") as handle:
            next(handle, None)
            for line in handle:
                stripped = line.strip()
                if not stripped:
                    continue
                cols = stripped.split()
                if len(cols) <= col_idx:
                    continue
                subject_id = cols[1]
                allele_map[subject_id] = genotype_to_alleles(cols[col_idx], variant_id)

        for subject_id in allele_map:
            nima_val, mer_val = call_variant_for_subject(
                subject_id, variant_id, allele_map, pedigree_map
            )
            out_nima[subject_id][variant_id] = nima_val
            out_mer[subject_id][variant_id] = mer_val

    return dict(out_nima), dict(out_mer)


def merge_subject_variant_maps(
    maps: Iterable[dict[str, dict[str, str]]],
) -> dict[str, dict[str, str]]:
    merged: dict[str, dict[str, str]] = defaultdict(dict)
    for part in maps:
        for subject_id, variant_values in part.items():
            merged[subject_id].update(variant_values)
    return dict(merged)


def run_nima_calling(
    raw_path: str,
    variant_ids: list[str],
    variant_col_index: dict[str, int],
    pedigree_map: dict[str, tuple[str, str]],
    threads: int | str = 1,
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    n_workers = multiprocessing.cpu_count() if threads == "max" else max(1, int(threads))
    chunks = chunk_items(variant_ids, n_workers)

    worker = partial(
        process_variant_chunk,
        raw_path=raw_path,
        pedigree_map=pedigree_map,
        variant_col_index=variant_col_index,
    )

    if n_workers == 1 or len(chunks) <= 1:
        chunk_results = [worker(c) for c in chunks]
    else:
        with multiprocessing.Pool(processes=n_workers) as pool:
            chunk_results = pool.map(worker, chunks)

    nima_parts = [res[0] for res in chunk_results]
    mer_parts = [res[1] for res in chunk_results]
    return merge_subject_variant_maps(nima_parts), merge_subject_variant_maps(mer_parts)
