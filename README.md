# APEX-Spiral Framework (LLM-Pangu Backup)
[![Stars](https://img.shields.io/github/stars/jhofdsajkjh/ApexSpiral-backup-LLM-Pangu?style=social)](https://github.com/jhofdsajkjh/ApexSpiral-backup-LLM-Pangu)
Status: Stable | License: MIT

## Features
- 基因进化：自动基因变异、交叉、选择，支持多模块并行演化
- 闭环自测：集成测试与基准测试，覆盖对齐、记忆、引擎核心路径
- 记忆系统：支持多模态记忆存储与检索，适配长期任务追踪
- 自进代理：提供自动化代理调度与策略执行流水线

## Installation
\`\`\`bash
git clone https://github.com/jhofdsajkjh/ApexSpiral-backup-LLM-Pangu.git
cd ApexSpiral-backup-LLM-Pangu
./install.sh
\`\`\`

## Usage
\`\`\`bash
python run_init.py       # 初始化环境
python -m self_evolve    # 运行单轮进化
bash run_evolver.sh      # 持续进化循环
\`\`\`

## Architecture
- \`core/\`: 核心引擎与基因读写
- \`align/\`: 对齐策略与评估
- \`memory/\`: 记忆存储与检索
- \`auto_agent/\`: 自动化代理调度
- \`self_evolve/\`: 进化主循环
- \`tests/\`: 单元与集成测试

## Tests
\`\`\`bash
python -m pytest tests/ -v
\`\`\`

## Contributing
提交前通过测试与基准，遵守变更日志格式。

## License
MIT
