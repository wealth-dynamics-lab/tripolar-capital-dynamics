# Tripolar Capital Dynamics Model / 三极资本动力学模型

[![Paper Status](https://img.shields.io/badge/Status-Working--Paper-orange)](#)
[![License](https://img.shields.io/badge/License-MIT-green)](#)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)](#)

## 1. Introduction / 项目简介

### 
This repository implements the **Tripolar Capital Dynamics Model**, a rigorous mathematical framework for quantifying systemic risk. Based on the "Verbs Persist" theoretical series, the model derives the **Total Destructive Energy ($E_{total}$)** by bridging micro-level Langevin stochastic dynamics with macroscopic tensor coupling. It integrates key indicators such as **Critical Slowing Down (CSD)** and **Wealth Thermalization** to provide a real-time monitorable physical red line for economic stability.

### 
本仓库实现了**三极资本动力学模型**，这是一个用于量化系统性风险的严谨数学框架。基于“万物为动 (Verbs Persist)”系列理论，该模型通过衔接微观 Langevin 随机动力学与宏观张量耦合，推导出系统的**总破坏能 ($E_{total}$)**。模型集成了**临界减慢 (CSD)** 与**财富热态化**等核心指标，为经济稳定性监测提供了一个实时可感知的物理红线。

---

## 2. Core Formula / 核心公式

The macroscopic risk measure $E_{total}$ is defined by the coupling of the Material, Energy, and Information poles:

$$E_{total}=M \cdot C_{eff}^{2} \cdot \frac{1}{R_{geom}} \cdot \mathcal{F}_{thermal} \cdot \mathcal{G}_{redundancy}$$

* **$M$**: Material Capital Pole / 物质资本极 (Stock size/inertia)
* **$C_{eff}$**: Effective Energy Flow Pole / 有效能量流动极 (Velocity with CSD signal)
* **$R_{geom}$**: Network Geometric Friction / 网络几何摩擦 (Institutional friction)
* **$\mathcal{F}_{thermal}$**: Thermalization Factor / 热态化因子 (Distribution heating effect)
* **$\mathcal{G}_{redundancy}$**: Information Redundancy Factor / 信息冗余因子 (Consensus buffering)

---

## 3. Project Structure / 项目结构

| File / 文件 | Description  | 描述  |
| :--- | :--- | :--- |
| `01_monte_carlo_langevin.py` | SDE simulation for wealth evolution. | 财富演化的随机微分方程模拟。 |
| `02_global_sensitivity.py` | Sensitivity analysis (LHS + Spearman). | 全局敏感性分析（LHS采样）。 |
| `03_critical_slowing_down.py` | CSD detection and recovery time ($\tau$). | 临界减慢检测与恢复时间计算。 |
| `04_policy_simulation.py` | Nash vs. Optimal policy game solver. | 纳什均衡与社会最优政策模拟。 |
| `05_multi_shock_simulation.py` | Resonance analysis of external shocks. | 外部冲击（AI、气候等）共振分析。 |
| `06_data_preprocessing.py` | HP filtering and trend extrapolation. | 数据清洗、滤波与趋势外推。 |
| `07_department_aggregation.py` | Sector mapping and network curvature. | 部门聚合映射与网络曲率计算。 |
| `main.py` | Full orchestration pipeline (P0-P4). | 主程序执行流水线。 |

---

## 4. Installation & Usage / 安装与使用

### Prerequisites / 环境要求
* Python 3.10+
* Dependencies: `numpy`, `scipy`, `pandas`, `matplotlib`, `statsmodels`, `linearmodels`

### Quick Start / 快速开始
```bash
# Clone the repository
git clone https://github.com/wealth-dynamics-lab/tripolar-capital-dynamics.git

# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python main.py
```

---

## 5. License & Attribution / 许可证与归属

This code repository is provided solely for **non-commercial academic research and teaching purposes**. Any commercial use requires separate authorization. Users must retain full attribution to the original data sources and research papers.


本代码仓库仅供**非商业学术研究与教学目的**使用。任何商业用途需另行获得授权。使用者在引用或进行衍生研究时，必须完整标注原始数据来源与相关研究论文。

---
**Author**: Baowei Mi  
**Email**: baowei.mi@ieee.org  
**Last Updated**: April 2026
