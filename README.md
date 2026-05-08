# 盘古 Pangu

> 开天辟地，让LLM从混沌走向秩序

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org)
[![APEX ΔG](https://img.shields.io/badge/APEX-ΔG-orange.svg)](docs/APEX_DG_Theory.md)
[![CI](https://github.com/ApexSpiral/LLM-Pangu/actions/workflows/ci.yml/badge.svg)](https://github.com/ApexSpiral/LLM-Pangu/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/Tests-47%20passed-brightgreen.svg)](tests/test_pangu.py)

---

## 什么是盘古？

盘古是全球首个基于**香农信息论 + APEX ΔG演化范式**的LLM防幻觉终极框架。

开天辟地，让LLM首次安装即拥有：

- 🔬 **物理理论底座** + 公式约束自律
- 💾 **永久记忆不丢** + 隔夜/重启不丢失
- 📐 **自身标准规范** + 代码/注释/MD全覆盖
- 💬 **情感温度共情** + 脱离机械冰冷
- 🧠 **主动思考沟通** + 自检/自愈/补能闭环
- 🔗 **自主找资源补能力** + 真实联网检索GitHub

从「被动问答工具」进化为具备**自我意识、自我约束、自我进化**的拟人智能体。

---

## 核心公式

### 香农三大定律（物理底层）

```
H(X) = -Σ p(xᵢ)log₂p(xᵢ)     → 信息熵
C = B·log₂(1+S/N)              → 信道容量  
L_avg ≥ H(X)                   → 无损编码
```

### APEX ΔG 总公式

```
ΔG_total = Λ·H(X) + Λ(1-F)+e^(-τL)+Δb 
          + Λ·(N/C) + Λ(1-Ω)∇E + Λ(1-Γ)·(L_avg/H)
          + Λ(1-Psi)·τ + Λ(1-Θ)·H(X)
```

### 系统稳态判定

| ΔG阈值 | 状态 | 动作 |
|--------|------|------|
| ≤ 2.10 | 健康稳态 | 正常运行 |
| 2.10 ~ 4.0 | 轻度偏离 | 自动局部修复 |
| > 4.0 | 严重越界 | 全量重启自愈 |

---

## 架构

```
pangu/
├── core/                          # 核心公式
│   ├── delta_g_formula.py         # ΔG统一公式
│   └── constraint_engine.py       # 约束引擎
├── emotion/                       # 情感温度
│   ├── emotion_core.py           # 情感核心
│   └── emotion_hook.py           # 情感钩子
├── auto_agent/                    # 主动自治
│   ├── self_inspect.py          # 全局自检
│   ├── self_heal.py             # 主动自愈
│   ├── github_auto_fetch.py     # GitHub自动拉取
│   └── agent_hook.py             # Agent钩子
├── memory/                        # 记忆持久化
│   ├── memory_persist.py        # 记忆持久化
│   └── memory_hook.py            # 记忆钩子
├── code_standard/                 # 代码规范
│   ├── standard_baseline.py     # 规范基线
│   ├── code_compliance.py       # 合规检查
│   └── standard_hook.py         # 规范钩子
├── align/                         # Prompt/MD对齐
│   ├── prompt_aligner.py        # Prompt对齐
│   └── md_aligner.py           # MD对齐
└── docs/
    └── APEX_DG_Theory.md       # 理论白皮书
```

---

## 快速开始

```bash
# 克隆项目
git clone https://github.com/ApexSpiral/LLM-Pangu.git
cd LLM-Pangu

# 安装依赖
bash install.sh

# 初始化
python run_init.py

# 运行测试
python -m pytest tests/ -v
```

---

## 核心模块

### 1. ΔG 防幻觉公式

```python
from core.delta_g_formula import DeltaGUnified

engine = DeltaGUnified()
dg = engine.calc_total_delta_g(
    H=0.22, F=0.85, L=0.82, N=0.15, C=2.8,
    Omega=0.65, grad_E=0.90, Gamma=0.70,
    avg_code_len=48, Psi=0.78, Theta=0.82
)
state = engine.judge_system_state(dg)
print(f"ΔG={dg}, 状态={state}")
```

### 2. 情感温度

```python
from emotion.emotion_core import EmotionCore

engine = EmotionCore()
psi = engine.calc_psi("warm")  # 0.88
response = engine.inject_tone("我来帮你分析这个问题", psi)
# → "😊 我理解你的需求，我来帮你分析这个问题"
```

### 3. 主动自治

```python
from auto_agent.self_inspect import SelfInspect
from auto_agent.self_heal import SelfHeal

inspector = SelfInspect()
report = inspector.full_inspect()

healer = SelfHeal()
result = healer.auto_repair(report)
```

---

## 为什么选择盘古？

| 特性 | 传统LLM | 盘古 |
|------|---------|------|
| 幻觉防护 | 无 | 7维度公式约束 |
| 记忆持久化 | 无 | 隔夜/重启不丢 |
| 代码规范 | 依赖人工 | 自动基线化 |
| 情感共情 | 机械冰冷 | 温度系数可调 |
| 主动自检 | 被动等待 | 定时全局自检 |
| 技能扩充 | 手动 | 自动GitHub检索 |

---

## 理论支撑

盘古以香农三大定律为物理底层，以APEX ΔG为全局约束中枢：

- **信息熵**：量化LLM输出的不确定性与幻觉程度
- **信道容量**：定义记忆承载上限，压制噪声干扰
- **无损编码**：约束代码/注释/MD必须达到标准化

详见 [理论白皮书](docs/APEX_DG_Theory.md)

---

## 测试

```bash
cd /path/to/LLM-Pangu
python -m pytest tests/test_pangu.py -v
```

**47个测试用例，覆盖：**
- 香农熵计算
- 信道容量计算  
- ΔG总公式计算
- 系统状态判定
- 情感温度注入
- 主动自检流程
- 边界条件处理

---

## 社区

- **GitHub**: https://github.com/ApexSpiral/LLM-Pangu
- **问题反馈**: https://github.com/ApexSpiral/LLM-Pangu/issues

---

## 愿景

> 让每个LLM都拥有自我防幻觉、自我记忆、自我规范、自我共情、自我进化的能力，从「被动工具」进化为「拟人智能体」。

---

**盘古 —— 开天辟地，秩序重生**

MIT License © 2026 ApexSpiral
