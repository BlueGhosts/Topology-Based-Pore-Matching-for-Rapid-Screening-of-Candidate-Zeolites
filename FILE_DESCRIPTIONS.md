# 文件功能说明 / File Descriptions

本文档详细说明了项目中每个文件的功能和用途。

This document provides detailed descriptions of each file's functionality and purpose in the project.

---

## 核心配置文件 / Core Configuration Files

### README.md
**功能 / Function**: 项目主文档 / Main project documentation
**说明 / Description**: 
- 提供项目概述、安装指南和使用说明
- 包含中英文双语文档
- 列出所有依赖项和环境要求
- Provides project overview, installation guide, and usage instructions
- Contains bilingual documentation (Chinese and English)
- Lists all dependencies and environment requirements

### requirements.txt
**功能 / Function**: Python 依赖包清单 / Python dependencies list
**说明 / Description**:
- 列出项目所需的所有 Python 包及其版本
- 用于 `pip install -r requirements.txt` 安装依赖
- 包含科学计算、结构处理、图论分析等核心库
- Lists all required Python packages with version specifications
- Used with `pip install -r requirements.txt` for dependency installation
- Includes core libraries for scientific computing, structure handling, and graph analysis

**主要依赖 / Key Dependencies**:
- `numpy>=1.21.0`: 数值计算 / Numerical computing
- `scipy>=1.7.0`: 科学计算 / Scientific computing
- `pandas>=1.3.0`: 数据处理 / Data manipulation
- `networkx>=2.6.0`: 图论分析 / Graph analysis
- `matplotlib>=3.4.0`: 数据可视化 / Data visualization
- `ase>=3.22.0`: 结构处理 / Structure handling
- `pymatgen>=2022.0.0`: 材料分析 / Materials analysis

### setup.py
**功能 / Function**: Python 包安装配置 / Python package installation configuration
**说明 / Description**:
- 定义包的元数据和安装配置
- 支持 `pip install -e .` 开发模式安装
- 配置包的分类、依赖和额外开发工具
- Defines package metadata and installation configuration
- Supports `pip install -e .` for development mode installation
- Configures package classification, dependencies, and extra dev tools

### .gitignore
**功能 / Function**: Git 忽略文件配置 / Git ignore configuration
**说明 / Description**:
- 指定不需要纳入版本控制的文件和目录
- 包含 Python 编译文件、虚拟环境、临时文件等
- 避免提交构建产物和 IDE 配置文件
- Specifies files and directories to exclude from version control
- Includes Python compiled files, virtual environments, temporary files, etc.
- Prevents committing build artifacts and IDE configuration files

---

## 文档文件 / Documentation Files

### LICENSE
**功能 / Function**: 开源许可证 / Open source license
**说明 / Description**:
- MIT 许可证文本
- 定义软件使用、修改和分发的权利和限制
- 保护作者权益同时允许自由使用
- MIT License text
- Defines rights and restrictions for software use, modification, and distribution
- Protects author's rights while allowing free usage

### CONTRIBUTING.md
**功能 / Function**: 贡献者指南 / Contributor guidelines
**说明 / Description**:
- 说明如何为项目做贡献
- 包含代码规范、测试要求和提交流程
- 提供中英文双语指南
- Explains how to contribute to the project
- Includes code standards, testing requirements, and submission process
- Provides bilingual guidelines (Chinese and English)

### CHANGELOG.md
**功能 / Function**: 版本变更记录 / Version change log
**说明 / Description**:
- 记录项目的版本历史和重要变更
- 遵循 Keep a Changelog 格式
- 帮助用户了解不同版本之间的差异
- Records project version history and significant changes
- Follows Keep a Changelog format
- Helps users understand differences between versions

---

## 项目结构说明 / Project Structure Description

### 计划中的目录 / Planned Directories

#### src/
**功能 / Function**: 源代码目录 / Source code directory
**说明 / Description**:
- 存放项目的核心 Python 代码
- 将包含以下模块（待实现）：
  - `topology_analyzer.py`: 拓扑分析算法
  - `pore_matcher.py`: 孔道匹配算法
  - `structure_loader.py`: 结构加载工具
  - `visualization.py`: 可视化工具
- Contains core Python code of the project
- Will include the following modules (to be implemented):
  - `topology_analyzer.py`: Topology analysis algorithms
  - `pore_matcher.py`: Pore matching algorithms
  - `structure_loader.py`: Structure loading utilities
  - `visualization.py`: Visualization tools

#### data/
**功能 / Function**: 数据目录 / Data directory
**说明 / Description**:
- 存放输入数据和输出结果
- 子目录（待创建）：
  - `structures/`: 输入的沸石结构文件（CIF、PDB 等）
  - `results/`: 分析结果和输出文件
- Stores input data and output results
- Subdirectories (to be created):
  - `structures/`: Input zeolite structure files (CIF, PDB, etc.)
  - `results/`: Analysis results and output files

#### examples/
**功能 / Function**: 示例代码目录 / Example code directory
**说明 / Description**:
- 提供使用示例和教程
- 帮助用户快速上手项目
- 包含完整的工作流程演示
- Provides usage examples and tutorials
- Helps users get started quickly
- Contains complete workflow demonstrations

#### tests/
**功能 / Function**: 测试代码目录 / Test code directory
**说明 / Description**:
- 存放单元测试和集成测试
- 确保代码质量和功能正确性
- 使用 pytest 框架（推荐）
- Contains unit tests and integration tests
- Ensures code quality and functionality
- Uses pytest framework (recommended)

---

## 文件依赖关系 / File Dependencies

```
setup.py
├── requirements.txt (读取依赖 / reads dependencies)
└── README.md (读取描述 / reads description)

README.md
├── LICENSE (引用 / references)
├── CONTRIBUTING.md (引用 / references)
└── requirements.txt (说明 / describes)

.gitignore
└── 保护所有文件 / protects all files
```

---

## 使用流程 / Usage Workflow

1. **安装 / Installation**
   ```bash
   pip install -r requirements.txt
   # 或 / or
   pip install -e .
   ```

2. **开发 / Development**
   - 参考 CONTRIBUTING.md
   - 遵循代码规范
   - 编写测试用例
   - Refer to CONTRIBUTING.md
   - Follow code standards
   - Write test cases

3. **版本管理 / Version Control**
   - 使用 .gitignore 排除不需要的文件
   - 更新 CHANGELOG.md 记录变更
   - 遵循语义化版本号
   - Use .gitignore to exclude unnecessary files
   - Update CHANGELOG.md to record changes
   - Follow semantic versioning

---

## 环境版本信息 / Environment Version Information

### Python 版本 / Python Version
- **最低要求 / Minimum**: Python 3.8
- **推荐版本 / Recommended**: Python 3.9 或更高 / or higher
- **测试版本 / Tested on**: Python 3.8, 3.9, 3.10, 3.11

### 操作系统兼容性 / OS Compatibility
- Linux (Ubuntu 18.04+, CentOS 7+)
- macOS (10.14+)
- Windows (10+)

### 硬件建议 / Hardware Recommendations
- **CPU**: 多核处理器（推荐 4 核或以上）/ Multi-core processor (4+ cores recommended)
- **内存 / RAM**: 8GB 最低，16GB 推荐 / 8GB minimum, 16GB recommended
- **存储 / Storage**: 至少 5GB 可用空间 / At least 5GB free space
- **GPU**: 可选，用于加速计算 / Optional, for accelerated computing

---

## 更新日志 / Update Log

- **2026-02-04**: 创建初始文档结构 / Initial documentation structure created
- **2026-02-04**: 添加完整的项目配置文件 / Complete project configuration files added
- **2026-02-04**: 创建本文件说明文档 / Created this file description document
