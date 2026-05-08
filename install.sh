#!/bin/bash
# LLM-ΔG-AntiHallucination 安装脚本

set -e

echo "========================================"
echo "LLM-ΔG-AntiHallucination 安装程序"
echo "========================================"

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "检测到 Python 版本: $python_version"

# 安装依赖
echo ""
echo "[1/3] 安装 Python 依赖..."
pip install pyyaml requests --quiet

# 验证安装
echo ""
echo "[2/3] 验证安装..."
python3 -c "import yaml; import requests; print('依赖验证通过')"

# 运行初始化
echo ""
echo "[3/3] 运行初始化检查..."
python3 run_init.py

echo ""
echo "========================================"
echo "安装完成!"
echo "========================================"
echo ""
echo "使用方法:"
echo "  python run_init.py          # 运行初始化"
echo "  pytest tests/ -v            # 运行测试"
echo "  python -c 'from core.delta_g_formula import *; print(quick_calc(2.0, 0.9, 100))'"
echo ""
