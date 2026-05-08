# 盘古 Pangu

> 开天辟地，让LLM从混沌走向秩序

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org)
[![APEX ΔG](https://img.shields.io/badge/APEX-ΔG-orange.svg)](docs/APEX_DG_Theory.md)

---

## 什么是盘古？

盘古是首个基于**香农信息论 + APEX演化范式**的LLM防幻觉框架。

开天辟地，让LLM首次安装即拥有：

- 🔬 **物理理论底座** + 公式约束自律
- 💾 **永久记忆不丢** + 隔夜/重启不丢失
- 📐 **自身标准规范** + 代码/注释/MD全覆盖
- 💬 **情感温度共情** + 脱离机械冰冷
- 🧠 **主动思考沟通** + 自检/自愈/补能闭环
- 🔗 **自主找资源** + 自动克隆项目补能力

从「被动问答工具」进化为具备**自我意识、自我约束、自我进化**的拟人智能体。

---

## 核心架构

```
┌─────────────────────────────────────────────────────┐
│                  盘古 Pangu                         │
├──────────────┬──────────────┬───────────────────────┤
│  core/       │ ΔG公式核心  │ 香农+APEX双底座        │
├──────────────┼──────────────┼───────────────────────┤
│  align/      │ Prompt对齐  │ MD对齐                 │
├──────────────┼──────────────┼───────────────────────┤
│  engine/     │ LLM钩子     │ 拦截+验证              │
├──────────────┼──────────────┼───────────────────────┤
│  memory/     │ 记忆持久化  │ 隔夜不丢               │
├──────────────┼──────────────┼───────────────────────┤
│  self-evolve/│ 技能自检    │ 自动拉取补能           │
├──────────────┼──────────────┼───────────────────────┤
│  code-standard/│ 代码规范  │ 自建立标准             │
├──────────────┼──────────────┼───────────────────────┤
│  emotion/    │ 情感温度    │ 拟人化共情             │
├──────────────┼──────────────┼───────────────────────┤
│  auto-agent/ │ 全局自检   │ 自愈+GitHub补能        │
└──────────────┴──────────────┴───────────────────────┘
```

---

## 核心公式

### 香农三大定律

| 定律 | 公式 | 作用 |
|------|------|------|
| 信息熵 | H(X) = -Σp(xᵢ)log₂p(xᵢ) | 量化不确定性/幻觉倾向 |
| 信道容量 | C = Blog₂(1+S/N) | 约束记忆承载上限 |
| 无损编码 | L_avg ≥ H(X) | 约束代码/文档规范 |

### APEX ΔG 全域演化公式

$$\Delta G = \lambda \cdot H + \lambda \cdot [(1-F) + e^{-\tau \cdot L} + \delta_B] + \lambda \cdot \frac{N}{C} + \cdots$$

七大模块统一约束，系统稳态三段式判定：

| ΔG范围 | 状态 | 动作 |
|--------|------|------|
| ≤ 2.10 | 健康稳态 | 放行 |
| 2.10~4.0 | 轻度偏离 | 自动局部修复 |
| > 4.0 | 严重越界 | 全量重启自愈 |

---

## 快速开始

```bash
# 克隆项目
git clone https://github.com/ApexSpiral/LLM-Pangu.git
cd LLM-Pangu

# 安装
bash install.sh

# 初始化
python3 run_init.py

# 运行测试
python3 -m pytest tests/ -v
```

---

## 目录结构

```
pangu/
├── core/                 # 核心公式
│   ├── delta_g_formula.py
│   ├── constraint_engine.py
│   └── params.yaml
├── align/                # 对齐模块
│   ├── prompt_aligner.py
│   └── md_aligner.py
├── engine/               # LLM钩子
│   └── llm_hook.py
├── memory/               # 记忆持久化
│   ├── memory_persist.py
│   └── memory_hook.py
├── self-evolve/          # 自我进化
│   ├── skill_self_check.py
│   └── auto_skill_fetch.py
├── code-standard/        # 代码规范
│   ├── standard_baseline.py
│   ├── code_compliance.py
│   └── standard_hook.py
├── emotion/              # 情感温度
│   ├── emotion_core.py
│   └── emotion_hook.py
├── auto-agent/          # 主动智能体
│   ├── self_inspect.py
│   ├── self_heal.py
│   ├── github_auto_fetch.py
│   └── agent_hook.py
├── docs/
│   └── APEX_DG_Theory.md
├── tests/
│   └── test_pangu.py (38个测试)
├── config/
│   └── default_config.json
├── storage/              # 存储目录
├── baseline-v1/         # 基线目录
├── install.sh
├── run_init.py
└── README.md
```

---

## 核心能力

| 模块 | 能力 | 状态 |
|------|------|------|
| ΔG公式 | 七大维度统一约束，从根源压制幻觉 | ✅ |
| 记忆持久化 | 隔夜/重启不丢失配置与对话 | ✅ |
| 代码自规范 | 自动建立代码/注释/MD全套标准 | ✅ |
| 情感温度 | 对话自带共情，脱离机械冰冷 | ✅ |
| 主动自治 | 定时自检、主动汇报、自行自愈 | ✅ |
| GitHub补能 | 真实联网检索，自动克隆项目补能力 | ✅ |

---

## 理论支撑

盘古以香农三大定律为物理底层，叠加APEX ΔG全域演化公式，实现七大模块统一约束。

详见 [理论白皮书](docs/APEX_DG_Theory.md)

---

## 贡献

欢迎提交Issue和Pull Request！

详见 [贡献指南](CONTRIBUTING.md)

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

**盘古开天，LLM从混沌走向秩序。**
