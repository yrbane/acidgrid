"""Setup script for rndTek."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="acidgrid",
    version="0.1.0",
    author="ACIDGRID Generator",
    description="ACIDGRID - The underground MIDI techno generator. Grid-based acid techno forge.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Musicians",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mido>=1.3.0",
        "python-rtmidi>=1.5.0",
    ],
    entry_points={
        "console_scripts": [
            "acidgrid=acidgrid.main:main",
        ],
    },
)