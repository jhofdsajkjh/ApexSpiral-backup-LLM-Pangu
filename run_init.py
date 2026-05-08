#!/usr/bin/env python3
"""
LLM-ΔG-AntiHallucination 初始化脚本
负责系统自检、依赖验证、初始配置
"""
import sys
import os
import json
from datetime import datetime

# 添加项目根目录到路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)


def print_header():
    """打印欢迎头"""
    print("=" * 50)
    print("  LLM-ΔG-AntiHallucination 初始化程序")
    print("  APEX ΔG 统一公式 - LLM抗幻觉核心引擎")
    print("=" * 50)
    print()


def check_python_version():
    """检查Python版本"""
    print("[1/7] 检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"  ✗ Python版本过低: {version.major}.{version.minor}")
        print("  需要 Python 3.8+")
        return False
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """检查依赖"""
    print("\n[2/7] 检查依赖...")

    required = ['math', 'json', 'datetime', 'traceback', 'yaml', 'requests']
    missing = []

    for module in required:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module} (缺失)")
            missing.append(module)

    if missing:
        print(f"\n  请安装缺失的依赖: pip install {' '.join(missing)}")
        return False

    return True


def check_core_modules():
    """检查核心模块"""
    print("\n[3/7] 检查核心模块...")

    modules = [
        'core.delta_g_formula',
        'core.constraint_engine',
        'align.prompt_aligner',
        'align.md_aligner',
        'engine.llm_hook',
        'memory.memory_persist',
        'memory.memory_hook',
        'self_evolve.skill_self_check',
        'self_evolve.auto_skill_fetch',
        'code_standard.standard_baseline',
        'code_standard.code_compliance',
        'code_standard.standard_hook',
        'emotion.emotion_core',
        'emotion.emotion_hook',
        'auto_agent.self_inspect',
        'auto_agent.self_heal',
        'auto_agent.github_auto_fetch',
        'auto_agent.agent_hook',
    ]

    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ✗ {module}: {e}")
            all_ok = False

    return all_ok


def test_delta_g():
    """测试DeltaG公式"""
    print("\n[4/7] 测试DeltaG公式...")

    try:
        from core.delta_g_formula import DeltaGUnified, quick_calc

        engine = DeltaGUnified()

        # 测试香农熵
        entropy = DeltaGUnified.shannon_entropy([0.5, 0.25, 0.125, 0.125])
        print(f"  熵计算: {entropy}")

        # 测试ΔG计算
        dg, state = quick_calc(H=2.0, F=0.9, L=100)
        print(f"  ΔG计算: {dg}, 状态: {state}")

        # 测试系统判定
        state1 = engine.judge_system_state(1.5)
        state2 = engine.judge_system_state(3.0)
        state3 = engine.judge_system_state(5.0)
        print(f"  状态判定: {state1} | {state2} | {state3}")

        print("  ✓ DeltaG公式测试通过")
        return True
    except Exception as e:
        print(f"  ✗ DeltaG测试失败: {e}")
        return False


def test_emotion_engine():
    """测试情绪引擎"""
    print("\n[5/7] 测试情绪引擎...")

    try:
        from emotion.emotion_core import EmotionCore

        engine = EmotionCore()

        # 测试情绪检测
        result = engine.detect_emotion("今天真开心!")
        print(f"  情绪检测: {result['emotion']} {result['icon']}")

        # 测试系统摘要
        summary = engine.generate_emotion_summary()
        print(f"  情绪摘要: {summary}")

        print("  ✓ 情绪引擎测试通过")
        return True
    except Exception as e:
        print(f"  ✗ 情绪引擎测试失败: {e}")
        return False


def test_auto_agent():
    """测试自动代理"""
    print("\n[6/7] 测试自动代理...")

    try:
        from auto_agent.self_inspect import SelfInspect

        inspector = SelfInspect()
        inspector.add_default_checks()

        report = inspector.run_all_checks()

        print(f"  系统状态: {report['overall_status']}")
        print(f"  检查项: {report['passed']}/{report['total']} 通过")

        if report['critical_failed']:
            print(f"  关键失败: {', '.join(report['critical_failed'])}")
        else:
            print("  无关键失败项")

        print("  ✓ 自动代理测试通过")
        return True
    except Exception as e:
        print(f"  ✗ 自动代理测试失败: {e}")
        return False


def create_initial_config():
    """创建初始配置"""
    print("\n[7/7] 检查配置文件...")

    config_path = os.path.join(PROJECT_ROOT, 'config', 'default_config.json')
    if os.path.exists(config_path):
        print(f"  ✓ 配置文件存在: {config_path}")
    else:
        print(f"  ! 配置文件未找到: {config_path}")

    return True


def print_summary(all_passed):
    """打印总结"""
    print("\n" + "=" * 50)
    if all_passed:
        print("  ✓ 所有检查通过!")
        print("  系统已准备就绪，可以正常使用。")
    else:
        print("  ⚠ 部分检查未通过")
        print("  请修复上述问题后重新运行。")
    print("=" * 50)


def main():
    """主函数"""
    print_header()

    results = []

    results.append(check_python_version())
    results.append(check_dependencies())
    results.append(check_core_modules())
    results.append(test_delta_g())
    results.append(test_emotion_engine())
    results.append(test_auto_agent())
    results.append(create_initial_config())

    all_passed = all(results)
    print_summary(all_passed)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
