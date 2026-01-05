# Pinocchio 学习资料

本仓库包含 Pinocchio 刚体动力学库的学习文档、API 参考和对比资料。

## 📚 文档内容

### 1. Pinocchio C++ 库论文（中文版）

- **文件**: `The Pinocchio C++ library.tex`
- **描述**: Pinocchio 库的原始论文的中文翻译版本，包含完整的 LaTeX 源码
- **内容**:
  - Pinocchio 框架介绍
  - 主要特性说明
  - 性能优化原理
  - 使用教程
  - 性能测试结果

### 2. Pinocchio 速查表

- **文件**: `pinocchio_cheat_sheet.tex`
- **描述**: Pinocchio Python API 的完整速查表
- **内容**:
  - 快速开始指南
  - 空间量操作（SE3, Motion, Force, Inertia）
  - 模型和数据管理
  - 运动学和动力学 API
  - 碰撞检测
  - 质心和能量计算
  - 回归器和接触动力学
  - 可视化工具

### 3. Pinocchio vs MuJoCo API 对比

- **文件**: `pinocchio_vs_mujoco_api.tex`
- **描述**: 详细对比 Pinocchio 和 MuJoCo 两个库的 API 设计和使用方式
- **内容**:
  - 基础 API 对比
  - 运动学 API 对比
  - 动力学 API 对比
  - 解析导数功能（Pinocchio 独有）
  - 碰撞检测对比
  - 可视化对比
  - 完整代码示例

### 4. 解析导数详解

- **文件**: `analytical_derivatives_explanation.tex`
- **描述**: 深入解释解析导数的概念、原理和应用
- **内容**:
  - 解析导数 vs 数值导数
  - 数学原理
  - 在机器人学中的应用
  - 性能对比
  - Pinocchio 中的实现

### 5. Pinocchio vs MuJoCo 对比（Markdown）

- **文件**: `pinocchio_vs_mujoco_comparison.md`
- **描述**: 两个库的功能定位和使用场景对比

## 🚀 快速开始

### 编译 LaTeX 文档

所有 `.tex` 文件都可以使用 XeLaTeX 或 pdfLaTeX 编译：

```bash
# 使用 XeLaTeX（推荐，支持中文）
xelatex filename.tex

# 或使用 pdfLaTeX
pdflatex filename.tex
```

### 查看 PDF

仓库中已包含编译好的 PDF 文件，可以直接查看。

## 📖 使用建议

1. **学习 Pinocchio**: 从 `pinocchio_cheat_sheet.tex` 开始，了解基本 API
2. **理解原理**: 阅读 `The Pinocchio C++ library.tex` 了解框架设计
3. **选择库**: 参考 `pinocchio_vs_mujoco_api.tex` 了解两个库的差异
4. **深入理解**: 阅读 `analytical_derivatives_explanation.tex` 理解解析导数

## 🔗 相关资源

- [Pinocchio 官方文档](https://stack-of-tasks.github.io/pinocchio/)
- [Pinocchio GitHub](https://github.com/stack-of-tasks/pinocchio)
- [MuJoCo 官方文档](https://mujoco.readthedocs.io/)

## 📝 文件说明

| 文件 | 类型 | 说明 |
|------|------|------|
| `*.tex` | LaTeX 源码 | 可编译生成 PDF |
| `*.pdf` | PDF 文档 | 编译后的文档 |
| `*.txt` | 文本文件 | 从 PDF 提取的文本 |
| `*.py` | Python 脚本 | 转换工具 |
| `*.md` | Markdown | 说明文档 |

## 🛠️ 工具脚本

- `convert_to_latex.py`: 将 PDF 转换的 TXT 文件转换为中文 LaTeX 格式

## 📄 许可证

本仓库中的文档基于原始论文和官方文档整理，仅供学习参考使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这些文档！

---

**注意**: 本仓库专注于 Pinocchio 库的学习资料，不包含 Pinocchio 库本身的源代码。

