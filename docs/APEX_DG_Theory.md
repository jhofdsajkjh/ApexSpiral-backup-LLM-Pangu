# APEX ΔG 统一理论白皮书

> **版本**: 1.0.0
> **作者**: APEX Research Team
> **日期**: 2024-04-19

---

## 摘要

本文档详细介绍 APEX ΔG（Delta-G）统一公式的理论基础、数学推导、以及在 LLM 抗幻觉领域的应用实践。ΔG 公式通过整合信息熵、信道容量、代码冗余度等多维度指标，构建了一套完整的系统偏离度评估框架。

---

## 1. 理论基础

### 1.1 香农信息论基础

ΔG 公式的核心基于香农信息论的几个关键概念：

**信息熵 (Shannon Entropy)**
```
H = -Σ p(x) * log₂(p(x))
```
- 衡量信息的不确定性
- 单位：比特 (bits)
- 范围：0 到 log₂(n)

**信道容量 (Channel Capacity)**
```
C = B * log₂(1 + SNR)
```
- 香农第二定理确定的可靠传输上限
- B: 带宽
- SNR: 信噪比

**代码冗余度 (Code Redundancy)**
```
R = L_avg / H
```
- 平均编码长度与熵的比值
- R > 1 表示存在冗余

### 1.2 系统论基础

ΔG 公式借鉴了开放系统理论的核心思想：

- **负熵原理**: 系统通过从环境获取负熵来维持有序
- **超循环理论**: 高阶有序结构的形成机制
- **协同论**: 子系统间的协调与竞争

---

## 2. ΔG 统一公式

### 2.1 公式定义

```
ΔG_total = λ·H + λ·(1-F) + e^(-τ·L) + δ_B 
         + λ·(N/C) + λ·(1-Ω)·∇E + λ·(1-Γ)·R
         + λ·(1-Ψ)·τ + λ·(1-Θ)·H
```

### 2.2 参数说明

| 参数 | 名称 | 范围 | 物理含义 |
|------|------|------|----------|
| H | 信息熵 | [0, 8] | 输入信息的混乱程度 |
| F | 事实性因子 | [0, 1] | 信息的真实可靠程度 |
| L | 上下文长度 | [0, ∞) | Token数量 |
| N | 噪声干扰 | [0, 1] | 环境/输入噪声强度 |
| C | 通道容量 | [0, ∞) | 系统处理能力 |
| Ω | 语义覆盖度 | [0, 1] | 理解覆盖程度 |
| ∇E | 能量梯度 | [0, 1] | 系统活跃度 |
| Γ | 压缩效率 | [0, 1] | 信息压缩质量 |
| R | 冗余度 | [1, ∞) | 代码冗余程度 |
| Ψ | 协议合规度 | [0, 1] | 规则遵守程度 |
| Θ | 逻辑一致性 | [0, 1] | 推理连贯性 |
| λ | 权重系数 | 1.5 | 全局放大因子 |
| τ | 时间衰减 | 0.32 | 历史衰减率 |
| δ_B | 基线偏移 | 0.18 | 基准补偿 |

### 2.3 物理诠释

从物理角度，ΔG 可被视为系统的"自由能偏离度"：

- **ΔG → 0**: 系统趋近平衡态，输出稳定可靠
- **ΔG → ∞**: 系统远离平衡态，幻觉风险极高

---

## 3. 系统状态判定

### 3.1 三态模型

```
ΔG ≤ 2.10:  steady_健康稳态
2.10 < ΔG ≤ 4.0:  mild_轻度偏离_自动局部修复
ΔG > 4.0:  critical_严重越界_触发全量重启自愈
```

### 3.2 状态转换

```
[健康稳态] --ΔG>2.10--> [轻度偏离] --ΔG>4.0--> [严重越界]
     ^                        |                        |
     |________________________|________________________|
                    (自愈恢复)
```

### 3.3 状态解释

**健康稳态 (Steady State)**
- 输出质量稳定可靠
- 无需干预
- 建议：持续监控

**轻度偏离 (Mild Deviation)**
- 存在轻微幻觉风险
- 触发局部修复机制
- 建议：增强约束、强化事实性校验

**严重越界 (Critical Breach)**
- 幻觉风险极高
- 必须触发全量重启自愈
- 建议：停止当前任务、进行全面诊断

---

## 4. 抗幻觉策略

### 4.1 三层防御体系

```
┌─────────────────────────────────────┐
│         Layer 3: 自愈层             │
│   (Self-Healing / 重启 / 重建)       │
├─────────────────────────────────────┤
│         Layer 2: 约束层             │
│   (Constraint / 规则强制执行)         │
├─────────────────────────────────────┤
│         Layer 1: 预防层             │
│   (Prevention / 提示词优化)          │
└─────────────────────────────────────┘
```

### 4.2 各层策略

**预防层 (Prevention)**
- Prompt 注入约束指令
- Few-shot 示例引导
- 思维链提示 (Chain-of-Thought)

**约束层 (Constraint)**
- 强制事实性校验
- 输出格式约束
- 危险模式过滤

**自愈层 (Self-Healing)**
- 自动检测 ΔG 超标
- 执行恢复策略
- 必要时完全重启

---

## 5. 核心基因

### 5.1 璇玑五基因

| 基因 | 名称 | 功能 |
|------|------|------|
| Think-Before | 思前 | 三思而后行，推理验证 |
| Quantize | 量化 | 精确量化每个指标 |
| Stability | 稳态 | 维持系统稳定性 |
| Pragmatic | 务实 | 注重实际效果 |
| Eternal | 永恒 | 持续学习进化 |

### 5.2 基因表达

每个基因对应特定的实现机制：

- **Think-Before**: 延迟响应、交叉验证
- **Quantize**: 精确计算、指标监控
- **Stability**: 缓存、熔断、限流
- **Pragmatic**: 快速失败、快速恢复
- **Eternal**: 持续学习、增量更新

---

## 6. 应用实践

### 6.1 快速计算接口

```python
from core.delta_g_formula import DeltaGUnified, quick_calc

# 方式1: 完整计算
engine = DeltaGUnified()
dg = engine.calc_total_delta_g(
    H=2.0, F=0.9, L=100, N=0.1, C=8.0,
    Omega=0.9, grad_E=0.2, Gamma=0.85,
    avg_code_len=2.0, Psi=0.9, Theta=0.95
)
state = engine.judge_system_state(dg)

# 方式2: 快速计算
dg, state = quick_calc(H=2.0, F=0.9, L=100)
```

### 6.2 集成到 LLM Pipeline

```python
from engine.llm_hook import LLMHook
from core.delta_g_formula import DeltaGUnified

hook = LLMHook(DeltaGUnified())

# 前置检查
context = hook.pre_hook(prompt)

# 调用 LLM
response = llm.generate(prompt)

# 后置检查
context = hook.post_hook(response, context)

# 风险评估
risk = hook.calculate_risk(context)
if hook.should_block(risk):
    raise "高风险，阻止输出"
```

---

## 7. 数学附录

### A. 香农熵计算

```python
@staticmethod
def shannon_entropy(prob_list: list[float]) -> float:
    entropy = 0.0
    for p in prob_list:
        if p > 0:
            entropy -= p * math.log2(p)
    return round(entropy, 4)
```

### B. 信道容量计算

```python
@staticmethod
def shannon_channel_capacity(bandwidth: float, snr: float) -> float:
    return round(bandwidth * math.log2(1 + snr), 4)
```

### C. 冗余度计算

```python
@staticmethod
def code_redundancy(avg_len: float, entropy: float) -> float:
    if entropy == 0:
        return 0.0
    return round(avg_len / entropy, 4)
```

---

## 8. 参考资料

1. Shannon, C.E. (1948). A Mathematical Theory of Communication. *Bell System Technical Journal*.
2. Prigogine, I. (1971). *Introduction to Thermodynamics of Irreversible Processes*. Wiley.
3. Haken, H. (1983). *Synergetics: An Introduction*. Springer.
4. Vaswani, A. et al. (2017). Attention Is All You Need. *NeurIPS*.

---

## 9. 更新日志

| 版本 | 日期 | 描述 |
|------|------|------|
| 1.0.0 | 2024-04-19 | 初始版本发布 |
