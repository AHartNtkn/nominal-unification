"""
nominal-unification - a simple implementation of nominal unification.
"""
import setuptools

REQUIRED = [
    "pymonad"
]

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
    setuptools.setup(
    name="nominal-unification",
    version = "0.1.0",
    author = "Anthony Hart",
    description = "a simple implementation of nominal unification.",
    long_description = LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/AHartNtkn/nominal-unification",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires = REQUIRED,
    classifiers=["Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]
    )