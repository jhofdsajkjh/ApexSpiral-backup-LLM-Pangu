# LLM-ΔG-AntiHallucination

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)
![CI](https://github.com/ApexSpiral/LLM-ΔG-AntiHallucination/workflows/CI/badge.svg)

> **APEX ΔG 统一公式 - LLM 抗幻觉核心引擎**

## 核心特性

- **ΔG 统一公式**: 整合信息熵、信道容量、代码冗余度等指标，量化系统偏离度
- **三态判定**: 自动判定系统状态（健康稳态/轻度偏离/严重越界）
- **三层防御**: 预防层 → 约束层 → 自愈层
- **情绪感知**: 内置情绪引擎，感知用户情绪并调整响应
- **自动自愈**: 问题检测与自动恢复机制

## 快速开始

### 安装

```bash
pip install pyyaml requests
python run_init.py
```

或使用安装脚本:

```bash
chmod +x install.sh
./install.sh
```

### 基本使用

```python
from core.delta_g_formula import DeltaGUnified, quick_calc

# 方式1: 快速计算
dg, state = quick_calc(H=2.0, F=0.9, L=100)
print(f"ΔG={dg}, 状态={state}")

# 方式2: 完整计算
engine = DeltaGUnified()
dg = engine.calc_total_delta_g(
    H=2.0, F=0.9, L=100, N=0.1, C=8.0,
    Omega=0.9, grad_E=0.2, Gamma=0.85,
    avg_code_len=2.0, Psi=0.9, Theta=0.95
)
state = engine.judge_system_state(dg)
```

### 运行测试

```bash
pytest tests/ -v
```

## 目录结构

```
LLM-ΔG-AntiHallucination/
├── core/                  # 核心模块
│   ├── delta_g_formula.py # ΔG统一公式
│   ├── constraint_engine.py
│   └── params.yaml
├── align/                 # 对齐模块
│   ├── prompt_aligner.py
│   └── md_aligner.py
├── engine/                # 引擎模块
│   └── llm_hook.py
├── memory/                # 内存模块
│   ├── memory_persist.py
│   └── memory_hook.py
├── self-evolve/           # 自进化模块
│   ├── skill_self_check.py
│   └── auto_skill_fetch.py
├── code-standard/         # 代码标准模块
│   ├── standard_baseline.py
│   ├── code_compliance.py
│   └── standard_hook.py
├── emotion/               # 情绪模块
│   ├── emotion_core.py
│   └── emotion_hook.py
├── auto-agent/            # 自动代理模块
│   ├── self_inspect.py
│   ├── self_heal.py
│   ├── github_auto_fetch.py
│   └── agent_hook.py
├── config/                # 配置
├── docs/                  # 文档
│   └── APEX_DG_Theory.md
├── tests/                 # 测试
└── examples/             # 示例
```

## ΔG 公式

### 参数说明

| 参数 | 名称 | 范围 | 说明 |
|------|------|------|------|
| H | 信息熵 | [0, 8] | 信息混乱程度 |
| F | 事实性因子 | [0, 1] | 信息真实度 |
| L | 上下文长度 | [0, ∞) | Token数量 |
| N | 噪声干扰 | [0, 1] | 环境噪声 |
| C | 通道容量 | [0, ∞) | 处理能力 |
| Ω | 语义覆盖度 | [0, 1] | 理解覆盖 |
| ∇E | 能量梯度 | [0, 1] | 系统活跃度 |
| Γ | 压缩效率 | [0, 1] | 压缩质量 |
| Ψ | 协议合规度 | [0, 1] | 规则遵守 |
| Θ | 逻辑一致性 | [0, 1] | 推理连贯性 |

### 系统状态阈值

```
ΔG ≤ 2.10:  健康稳态
2.10 < ΔG ≤ 4.0:  轻度偏离 → 自动局部修复
ΔG > 4.0:  严重越界 → 触发全量重启自愈
```

## 璇玑五基因

| 基因 | 名称 | 功能 |
|------|------|------|
| Think-Before | 思前 | 三思而后行 |
| Quantize | 量化 | 精确量化指标 |
| Stability | 稳态 | 维持稳定 |
| Pragmatic | 务实 | 注重实效 |
| Eternal | 永恒 | 持续进化 |

## 贡献

欢迎提交 Issue 和 Pull Request!

参见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License - 参见 [LICENSE](LICENSE)
