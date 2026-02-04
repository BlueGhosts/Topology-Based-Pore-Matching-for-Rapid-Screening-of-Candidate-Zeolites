"""
Setup configuration for Topology-Based Pore Matching for Zeolite Screening
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line)

setup(
    name="topology-pore-matching",
    version="0.1.0",
    author="BlueGhosts",
    author_email="58764089+BlueGhosts@users.noreply.github.com",
    description="A topology-based pore matching method for rapid screening of candidate zeolites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BlueGhosts/Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.900",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/BlueGhosts/Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites/issues",
        "Source": "https://github.com/BlueGhosts/Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites",
    },
)
