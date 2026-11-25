# pyNIMA

`pyNIMA` is a command-line tool and Python library for calling **Non-Inherited Maternal Alleles (NIMA)** and identifying **Mendelian Errors (MER)** from PLINK additive `.raw` genotype files and `.fam` pedigree files.

## Overview

In family-based genetic and HLA association studies, `pyNIMA` evaluates child-mother-father trios (and mother-child or father-child duos when one parent is missing) at each variant to:

1. **Call Non-Inherited Maternal Alleles (`_nima.tsv`):** Determines whether the mother carries a heterozygous genotype with a non-transmitted allele that can be unambiguously distinguished from the child's inherited alleles, returning the non-inherited maternal allele, `"0"` when no NIMA can be called, `"MEND_ERR"` when a Mendelian inconsistency is detected, or `"NA"` when required genotypes are missing.
2. **Detect Mendelian Errors (`_mer.tsv`):** Checks parent-offspring allele transmission consistency, returning `"0"` (consistent), `"1"` (Mendelian error), or `"NA"` (insufficient parental/offspring genotype data).

## Requirements

* Python `>= 3.8`
* Standard library only (no third-party runtime dependencies)
* `pytest` (optional, for running the test suite)

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/USF-HII/pyNIMA.git](https://github.com/USF-HII/pyNIMA.git
cd pyNIMA
pip install --no-build-isolation --no-deps -e .
```

> **Note for older `setuptools` environments (e.g., `setuptools < 61`):** This repository includes both `pyproject.toml` and `setup.py` so editable installs (`pip install --no-build-isolation --no-deps -e .`) work across modern and legacy Python 3.8 environments.

## Command-Line Usage

```bash
pynima -i <input.raw> -f <pedigree.fam> -o <output_prefix> [-t <threads>]
```

### CLI Options

| Flag | Description |
| :--- | :--- |
| `-i`, `--input` | Path to PLINK additive `.raw` genotype file (generated with `plink --recode A` or `--recode AD`). |
| `-f`, `--fam` | Path to PLINK `.fam` pedigree file defining family relationships (`FID`, `IID`, `PAT`, `MAT`, `SEX`, `PHENOTYPE`). |
| `-o`, `--output` | Prefix for output TSV files (`<output>_nima.tsv` and `<output>_mer.tsv`). |
| `-t`, `--threads` | Number of worker threads/processes (`max` or integer; defaults to available cores / single-process fallback). |

### Example

```bash
pynima \
  -i test_data/cohort_hla.raw \
  -f test_data/cohort_hla.fam \
  -o results/cohort_hla \
  -t max
```

This produces:
* `results/cohort_hla_nima.tsv`
* `results/cohort_hla_mer.tsv`

## Input File Formats

### PLINK `.raw` File
A whitespace-delimited PLINK additive genotype file where:
* Columns 1–6 are standard PLINK sample metadata: `FID`, `IID`, `PAT`, `MAT`, `SEX`, `PHENOTYPE`.
* Columns 7+ are variant dosage columns formatted as `<VARIANT_ID>_<COUNTED_ALLELE>` with additive counts (`0`, `1`, `2`, or `NA`).

You can generate the `.raw` file from PLINK binary files (`.bed`/`.bim`/`.fam`) using PLINK 1.9:

```bash
plink \
  --bfile <plink_prefix> \
  --chr <chr> \
  --recode A \
  --out <output_prefix>
```

### PLINK `.fam` File
A standard 6-column whitespace-delimited PLINK pedigree file:
1. Family ID (`FID`)
2. Individual ID (`IID`)
3. Paternal ID (`PAT`, `0` if missing)
4. Maternal ID (`MAT`, `0` if missing)
5. Sex (`1` = male, `2` = female, `0` = unknown)
6. Phenotype

## Output File Formats

Both output files are tab-delimited matrices with subjects as rows and variants as columns:

* **`<output>_nima.tsv`**:
  * Specific allele string (e.g., `DR3`, `DR4`, `C`, `T`) when a non-inherited maternal allele is present.
  * `0` when no NIMA is present or when NIMA status cannot be resolved (e.g., homozygous mother, or mother and child share the same heterozygous genotype with ambiguous parental origin).
  * `MEND_ERR` when child and parental genotypes violate Mendelian inheritance.
  * `NA` when child or maternal genotype data is missing.

* **`<output>_mer.tsv`**:
  * `0` when observed genotypes are consistent with Mendelian inheritance.
  * `1` when a Mendelian error is detected.
  * `NA` when child or both parental genotypes are missing/incomplete.

## Python API

You can also import and call the core functions directly in Python:

```python
from pynima.core import call_nima, check_mer

# Call NIMA for a child-mother-father trio (child_a1, child_a2, mat_a1, mat_a2, pat_a1, pat_a2)
nima_call = call_nima("DR3", "DR8", "DR3", "DR4", "DR8", "DR9")
# Returns: "DR4"

# Check Mendelian error status
mer_call = check_mer("DR3", "DR3", "DR4", "DR4", "NA", "NA")
# Returns: "1"
```

## Running Tests

Run the unit test suite with `pytest`:

```bash
python -m pytest
```

## Project Structure

```text
pyNIMA/
├── LICENSE
├── README.md
├── pyproject.toml
├── setup.py
├── src/
│   └── pynima/
│       ├── __init__.py
│       ├── cli.py
│       ├── core.py
│       └── io.py
└── tests/
    ├── test_DR_2opt_nima.py
    ├── test_DR_3opt_nima.py
    ├── test_DR_4opt_nima.py
    ├── test_mer.py
    └── test_snp_nima.py
```
