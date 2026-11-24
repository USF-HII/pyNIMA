from setuptools import find_packages, setup

setup(
    name="pynima",
    version="0.1.0",
    description="Call Non-Inherited Maternal Allele (NIMA) and Mendelian error (MER) matrices from PLINK genotype files.",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pynima=pynima.cli:main",
        ],
    },
)
