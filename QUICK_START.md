# 快速开始指南 / Quick Start Guide

本指南帮助您快速开始使用本项目。

This guide helps you quickly get started with this project.

---

## 目录 / Table of Contents

1. [环境准备 / Environment Setup](#环境准备--environment-setup)
2. [安装步骤 / Installation Steps](#安装步骤--installation-steps)
3. [基本使用 / Basic Usage](#基本使用--basic-usage)
4. [常见问题 / FAQ](#常见问题--faq)

---

## 环境准备 / Environment Setup

### 系统要求 / System Requirements

- **操作系统 / OS**: Linux, macOS, 或 / or Windows 10+
- **Python 版本 / Python Version**: 3.8 或更高 / or higher
- **内存 / RAM**: 至少 8GB / At least 8GB
- **磁盘空间 / Disk Space**: 至少 5GB / At least 5GB

### 检查 Python 版本 / Check Python Version

```bash
python --version
# 或 / or
python3 --version
```

如果版本低于 3.8，请先升级 Python。
If version is below 3.8, please upgrade Python first.

---

## 安装步骤 / Installation Steps

### 步骤 1: 克隆仓库 / Step 1: Clone Repository

```bash
git clone https://github.com/BlueGhosts/Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites.git
cd Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites
```

### 步骤 2: 创建虚拟环境（推荐）/ Step 2: Create Virtual Environment (Recommended)

#### Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 步骤 3: 安装依赖 / Step 3: Install Dependencies

#### 方法 A: 使用 requirements.txt / Method A: Using requirements.txt
```bash
pip install -r requirements.txt
```

#### 方法 B: 安装为包 / Method B: Install as Package
```bash
pip install -e .
```

### 步骤 4: 验证安装 / Step 4: Verify Installation

```bash
python -c "import numpy, scipy, pandas, networkx, matplotlib; print('所有依赖安装成功！/ All dependencies installed successfully!')"
```

---

## 基本使用 / Basic Usage

### 示例 1: 加载沸石结构 / Example 1: Load Zeolite Structure

```python
# 注意：以下代码为示例，实际功能待实现
# Note: The following code is an example, actual functionality to be implemented

from src.structure_loader import load_zeolite

# 加载 CIF 格式的沸石结构
structure = load_zeolite('data/structures/example.cif')
print(f"加载的结构: {structure.name}")
print(f"原子数量: {len(structure.atoms)}")
```

### 示例 2: 分析拓扑结构 / Example 2: Analyze Topology

```python
from src.topology_analyzer import analyze_topology

# 分析孔道拓扑
topology = analyze_topology(structure)
print(f"节点数: {topology.num_nodes}")
print(f"连接数: {topology.num_edges}")
```

### 示例 3: 匹配孔道 / Example 3: Match Pores

```python
from src.pore_matcher import match_pores

# 与数据库中的结构进行匹配
matches = match_pores(topology, database_path='data/zeolite_database')
print(f"找到 {len(matches)} 个匹配结构")

# 显示最佳匹配
for i, match in enumerate(matches[:5], 1):
    print(f"{i}. {match.name} - 相似度: {match.similarity:.2f}")
```

### 示例 4: 可视化结果 / Example 4: Visualize Results

```python
from src.visualization import visualize_topology

# 可视化拓扑网络
visualize_topology(topology, save_path='results/topology_network.png')
print("拓扑网络图已保存")
```

---

## 文件结构 / File Structure

```
项目根目录 / Project Root
├── README.md                  # 主要文档 / Main documentation
├── requirements.txt           # 依赖列表 / Dependencies list
├── setup.py                   # 安装配置 / Installation config
├── LICENSE                    # 许可证 / License
├── CHANGELOG.md              # 变更日志 / Change log
├── CONTRIBUTING.md           # 贡献指南 / Contributing guide
├── FILE_DESCRIPTIONS.md      # 文件说明 / File descriptions
├── QUICK_START.md            # 本文件 / This file
│
├── src/                      # 源代码 / Source code (待实现 / to be implemented)
│   ├── __init__.py
│   ├── topology_analyzer.py
│   ├── pore_matcher.py
│   ├── structure_loader.py
│   └── visualization.py
│
├── data/                     # 数据目录 / Data directory (待创建 / to be created)
│   ├── structures/           # 输入结构 / Input structures
│   └── results/              # 结果输出 / Results output
│
├── examples/                 # 示例代码 / Examples (待创建 / to be created)
│   └── example_workflow.py
│
└── tests/                    # 测试代码 / Tests (待创建 / to be created)
    └── test_topology.py
```

---

## 常见问题 / FAQ

### Q1: 安装依赖时出现错误怎么办？/ What to do if dependency installation fails?

**A**: 
1. 确保 Python 版本 >= 3.8 / Ensure Python version >= 3.8
2. 尝试升级 pip: `pip install --upgrade pip`
3. 如果某个包安装失败，可以单独安装：/ If a specific package fails, install it separately:
   ```bash
   pip install numpy scipy pandas
   ```
4. 在 Windows 上，某些包可能需要 Visual C++ 构建工具 / On Windows, some packages may require Visual C++ build tools

### Q2: 如何更新项目到最新版本？/ How to update the project to the latest version?

**A**:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Q3: 虚拟环境有什么作用？/ What is the purpose of a virtual environment?

**A**:
虚拟环境可以隔离项目依赖，避免与系统中其他 Python 项目冲突。
Virtual environments isolate project dependencies to avoid conflicts with other Python projects.

### Q4: 项目支持哪些沸石结构文件格式？/ What zeolite structure file formats are supported?

**A**:
计划支持以下格式（待实现）：
Planned support for the following formats (to be implemented):
- CIF (Crystallographic Information File)
- PDB (Protein Data Bank)
- XYZ (XYZ coordinate format)
- POSCAR (VASP format)

### Q5: 如何贡献代码？/ How to contribute code?

**A**:
请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 文件了解详细的贡献指南。
Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### Q6: 在哪里报告问题？/ Where to report issues?

**A**:
请在 GitHub 上创建 issue: 
Please create an issue on GitHub:
https://github.com/BlueGhosts/Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites/issues

---

## 下一步 / Next Steps

1. **阅读完整文档 / Read Full Documentation**: 查看 [README.md](README.md) 了解更多细节 / Check [README.md](README.md) for more details
2. **查看示例 / Check Examples**: 浏览 `examples/` 目录中的示例代码 / Browse example code in `examples/` directory
3. **参与开发 / Join Development**: 阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献 / Read [CONTRIBUTING.md](CONTRIBUTING.md) to learn how to contribute
4. **提供反馈 / Provide Feedback**: 在 GitHub 上提交问题或建议 / Submit issues or suggestions on GitHub

---

## 获取帮助 / Get Help

- **文档 / Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/BlueGhosts/Topology-Based-Pore-Matching-for-Rapid-Screening-of-Candidate-Zeolites/issues)
- **Email**: 58764089+BlueGhosts@users.noreply.github.com

---

## 许可证 / License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

**祝使用愉快！/ Happy coding!** 🎉
