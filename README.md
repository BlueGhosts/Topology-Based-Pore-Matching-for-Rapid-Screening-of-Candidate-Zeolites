# Topology-Based Pore Matching for Rapid Screening of Candidate Zeolites

A topology-based pore matching method for rapid screening of candidate zeolites by simplifying complex pore channels into node-link networks, enabling efficient screening from massive zeolite structure databases.

---

## Overview

This repository contains the supporting code to assist in completing the research work associated with the following paper:

"Topology-Based Pore Matching for Rapid Screening of Candidate Zeolites"

Jiaze Wang, Rui Lin, Yurong Hu, Lin Li, Wenfu Yan, and Yi Li*

Chinese Chemical Letters (2026)

Zeolites are microporous materials whose performance is governed by their pore structures. This method simplifies complex pore channels into "node-link" networks, capturing both connectivity and global topological characteristics of accessible pores. It enables efficient pore matching and rapid screening of candidate zeolites from massive structure databases.

<img width="1918" height="786" alt="PoreTopology-Figure1" src="https://github.com/user-attachments/assets/9ee57a9e-0537-4c34-aaae-b9ec75dec9b5" />


The core idea:
- Simplify complex pore channels into **node-link topological networks**
- Capture both connectivity and global topological features
- Enable fast and accurate pore matching and screening from large structure databases

---

## Repository Structure

| Folder             | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `ToposPro/`         | Post-processing scripts for ToposPro output files                           |
| `MaterialsStudio/`  | Automation and format conversion scripts for Materials Studio               |
| `PoreTopology/`     | Core pore topology analysis and matching algorithms                         |

---

## Computational Workflow

All pore topological network construction and analysis follow these steps:

1. **Structure Import**  
   Zeolite crystal structures (CIF format) are imported into ToposPro (v5.3.3.1).

2. **Natural Tiling & Dual Net Generation**  
   Use `AutoCN` to identify atomic connectivity, then `ADS` to generate natural tiling and dual net.

3. **Probe-Based Filtering**  
   Probe sizes: 0.33, 0.42, 0.50, 0.59 nm.  
   Use `Modify Adjacency Matrix` to remove inaccessible connections in the dual net.

4. **Structure Export & Format Conversion**  
   Export filtered structures from ToposPro.  
   Use custom scripts:
   - `Topocif2MScif.py`: Convert CIF for Materials Studio
   - `SplitAdo.py`, `GetPoreDimension.py`: Extract structure and pore dimension info

5. **Connectivity & Geometry Analysis**  
   Use Perl script `CalculatenNodeAndConnection.pl` with Materials Studio  
   to compute node connectivity and inter-node angles.

6. **Similarity Matching & Screening**  
   Use Python scripts:
   - `FindSameCsq.py`
   - `FindSamebyCsq&Bond&Angel.py`

   Classification:
   - **Similar**: Identical topological coordination sequences
   - **Highly similar**: Similar topology + geometry within ±15% (link length & angle)

---

## Requirements

- Python ≥ 3.8
- NumPy ≥ 1.20
- Pandas ≥ 1.3

<img width="897" height="926" alt="PoreTopology-Figure2" src="https://github.com/user-attachments/assets/b9b3b3aa-d51a-4631-99a3-8646b459c9f7" />
