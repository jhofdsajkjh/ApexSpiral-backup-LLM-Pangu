# LLM-ΔG-AntiHallucination

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)
![CI](https://github.com/ApexSpiral/LLM-ΔG-AntiHallucination/workflows/CI/badge.svg)

> **APEX ΔG Unified Formula - LLM Anti-Hallucination Core Engine**

## Features

- **ΔG Unified Formula**: Integrates information entropy, channel capacity, code redundancy for system deviation quantification
- **Three-State Detection**: Automatic state detection (healthy/mild deviation/critical breach)
- **Three-Layer Defense**: Prevention → Constraint → Self-Healing
- **Emotion Sensing**: Built-in emotion engine for user mood detection and response adjustment
- **Auto-Healing**: Automatic problem detection and recovery mechanism

## Quick Start

### Installation

```bash
pip install pyyaml requests
python run_init.py
```

Or use the installer:

```bash
chmod +x install.sh
./install.sh
```

### Basic Usage

```python
from core.delta_g_formula import DeltaGUnified, quick_calc

# Quick calculation
dg, state = quick_calc(H=2.0, F=0.9, L=100)
print(f"ΔG={dg}, State={state}")

# Full calculation
engine = DeltaGUnified()
dg = engine.calc_total_delta_g(
    H=2.0, F=0.9, L=100, N=0.1, C=8.0,
    Omega=0.9, grad_E=0.2, Gamma=0.85,
    avg_code_len=2.0, Psi=0.9, Theta=0.95
)
state = engine.judge_system_state(dg)
```

### Run Tests

```bash
pytest tests/ -v
```

## Project Structure

```
LLM-ΔG-AntiHallucination/
├── core/                  # Core module
│   ├── delta_g_formula.py # ΔG unified formula
│   ├── constraint_engine.py
│   └── params.yaml
├── align/                 # Alignment module
├── engine/                # Engine module
├── memory/                # Memory module
├── self-evolve/           # Self-evolution module
├── code-standard/         # Code standards module
├── emotion/               # Emotion module
├── auto-agent/            # Auto-agent module
├── config/                # Configuration
├── docs/                  # Documentation
│   └── APEX_DG_Theory.md
├── tests/                 # Tests
└── examples/             # Examples
```

## ΔG Formula

### Parameters

| Param | Name | Range | Description |
|-------|------|-------|-------------|
| H | Information Entropy | [0, 8] | Information disorder |
| F | Factuality Factor | [0, 1] | Information truthfulness |
| L | Context Length | [0, ∞) | Token count |
| N | Noise Interference | [0, 1] | Environmental noise |
| C | Channel Capacity | [0, ∞) | Processing capability |
| Ω | Semantic Coverage | [0, 1] | Understanding coverage |
| ∇E | Energy Gradient | [0, 1] | System activity |
| Γ | Compression Efficiency | [0, 1] | Compression quality |
| Ψ | Protocol Compliance | [0, 1] | Rule adherence |
| Θ | Logical Consistency | [0, 1] | Reasoning coherence |

### System State Thresholds

```
ΔG ≤ 2.10:  Healthy Steady State
2.10 < ΔG ≤ 4.0:  Mild Deviation → Auto Local Repair
ΔG > 4.0:  Critical Breach → Full Restart Self-Healing
```

## Contributing

Issues and Pull Requests are welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - See [LICENSE](LICENSE)
