# Topology-Based Pore Matching for Rapid Screening of Candidate Zeolites

[English](#english) | [中文](#中文)

---

## English

### Project Overview

This project implements a topology-based pore matching method for rapid screening of candidate zeolites. The approach simplifies complex pore channels into node-link networks, enabling efficient comparison and identification of zeolites with desired pore structures.

### Key Features

- **Topological Network Analysis**: Converts complex 3D pore structures into simplified node-link networks
- **Rapid Screening**: Efficient algorithms for comparing zeolite pore topologies
- **Structure Matching**: Identifies candidate zeolites based on pore channel characteristics
- **Visualization Tools**: Graphical representation of pore networks and matching results

### Environment Requirements

#### Python Version
- Python >= 3.8

#### Core Dependencies
- **numpy** (>=1.21.0): Numerical computing and array operations
- **scipy** (>=1.7.0): Scientific computing and optimization algorithms
- **pandas** (>=1.3.0): Data manipulation and analysis
- **networkx** (>=2.6.0): Graph and network analysis for topology representation
- **matplotlib** (>=3.4.0): Data visualization and plotting
- **ase** (>=3.22.0): Atomic Simulation Environment for structure handling
- **pymatgen** (>=2022.0.0): Materials analysis and structure processing

#### Additional Dependencies
See `requirements.txt` for a complete list of dependencies.

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/BlueGhosts/Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites.git
cd Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites
```

#### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### Project Structure

```
Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites/
├── README.md                 # Project documentation
├── requirements.txt          # Python package dependencies
├── src/                      # Source code (to be implemented)
│   ├── topology_analyzer.py  # Topology analysis module
│   ├── pore_matcher.py      # Pore matching algorithms
│   ├── structure_loader.py  # Zeolite structure loading utilities
│   └── visualization.py     # Visualization tools
├── data/                     # Data directory (to be created)
│   ├── structures/          # Input zeolite structures
│   └── results/             # Analysis results
├── examples/                 # Usage examples (to be implemented)
│   └── example_screening.py # Example screening workflow
└── tests/                    # Unit tests (to be implemented)
```

### Usage

#### Basic Workflow

```python
# Example usage (to be implemented)
from src.structure_loader import load_zeolite
from src.topology_analyzer import analyze_topology
from src.pore_matcher import match_pores

# Load zeolite structure
structure = load_zeolite('path/to/structure.cif')

# Analyze pore topology
topology = analyze_topology(structure)

# Match against candidate structures
matches = match_pores(topology, candidate_database)

# Visualize results
topology.visualize()
```

#### File Descriptions

- **requirements.txt**: Lists all Python package dependencies with minimum version requirements
- **README.md**: Comprehensive project documentation including setup, usage, and file descriptions

### Development Roadmap

- [ ] Implement topology analysis algorithms
- [ ] Develop pore matching algorithms
- [ ] Create structure loading utilities
- [ ] Build visualization tools
- [ ] Add comprehensive examples
- [ ] Write unit tests
- [ ] Optimize performance for large databases

### Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contact

For questions or collaboration inquiries, please open an issue on GitHub.

---

## 中文

### 项目概述

本项目实现了一种基于拓扑结构的孔道匹配方法，用于快速筛选候选沸石材料。该方法将复杂的孔道结构简化为节点-连接网络，从而实现高效的沸石孔道结构比对和识别。

### 主要特性

- **拓扑网络分析**：将复杂的三维孔道结构转换为简化的节点-连接网络
- **快速筛选**：高效的沸石孔道拓扑比对算法
- **结构匹配**：基于孔道特征识别候选沸石材料
- **可视化工具**：孔道网络和匹配结果的图形化展示

### 环境要求

#### Python 版本
- Python >= 3.8

#### 核心依赖包
- **numpy** (>=1.21.0): 数值计算和数组操作
- **scipy** (>=1.7.0): 科学计算和优化算法
- **pandas** (>=1.3.0): 数据处理和分析
- **networkx** (>=2.6.0): 图和网络分析，用于拓扑表示
- **matplotlib** (>=3.4.0): 数据可视化和绘图
- **ase** (>=3.22.0): 原子模拟环境，用于结构处理
- **pymatgen** (>=2022.0.0): 材料分析和结构处理

#### 其他依赖包
完整的依赖包列表请参见 `requirements.txt` 文件。

### 安装步骤

#### 1. 克隆仓库
```bash
git clone https://github.com/BlueGhosts/Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites.git
cd Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites
```

#### 2. 创建虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate  # Windows 系统: venv\Scripts\activate
```

#### 3. 安装依赖包
```bash
pip install -r requirements.txt
```

### 项目结构

```
Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites/
├── README.md                 # 项目文档
├── requirements.txt          # Python 依赖包列表
├── src/                      # 源代码目录（待实现）
│   ├── topology_analyzer.py  # 拓扑分析模块
│   ├── pore_matcher.py      # 孔道匹配算法
│   ├── structure_loader.py  # 沸石结构加载工具
│   └── visualization.py     # 可视化工具
├── data/                     # 数据目录（待创建）
│   ├── structures/          # 输入的沸石结构文件
│   └── results/             # 分析结果
├── examples/                 # 使用示例（待实现）
│   └── example_screening.py # 筛选流程示例
└── tests/                    # 单元测试（待实现）
```

### 使用方法

#### 基本工作流程

```python
# 使用示例（待实现）
from src.structure_loader import load_zeolite
from src.topology_analyzer import analyze_topology
from src.pore_matcher import match_pores

# 加载沸石结构
structure = load_zeolite('path/to/structure.cif')

# 分析孔道拓扑
topology = analyze_topology(structure)

# 与候选结构进行匹配
matches = match_pores(topology, candidate_database)

# 可视化结果
topology.visualize()
```

#### 文件说明

- **requirements.txt**: 列出所有 Python 依赖包及其最低版本要求
- **README.md**: 完整的项目文档，包括安装、使用方法和文件说明

### 开发路线图

- [ ] 实现拓扑分析算法
- [ ] 开发孔道匹配算法
- [ ] 创建结构加载工具
- [ ] 构建可视化工具
- [ ] 添加完整的使用示例
- [ ] 编写单元测试
- [ ] 优化大型数据库的性能

### 贡献指南

欢迎贡献！请随时提交问题或拉取请求。

### 许可证

本项目采用 MIT 许可证 - 详情请参见 [LICENSE](LICENSE) 文件。

### 联系方式

如有问题或合作需求，请在 GitHub 上提交 issue。
