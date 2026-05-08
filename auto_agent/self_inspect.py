"""
SelfInspect - 自我检查模块
自动检查系统状态、健康度、配置完整性
"""
import sys
import json
import traceback
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class SelfInspect:
    """
    自我检查器 - APEX自检核心

    功能:
    1. 系统健康检查
    2. 模块完整性验证
    3. 依赖检查
    4. 配置验证
    """

    def __init__(self):
        self.checks = []
        self.last_check_time: Optional[datetime] = None
        self.check_interval = timedelta(minutes=5)

    def register_check(self, name: str, check_fn: callable, critical: bool = False):
        """
        注册检查项

        参数:
            name: 检查名称
            check_fn: 检查函数，返回 (passed: bool, message: str)
            critical: 是否为关键检查
        """
        self.checks.append({
            'name': name,
            'fn': check_fn,
            'critical': critical
        })

    def run_check(self, check: Dict) -> Dict:
        """
        运行单个检查
        """
        try:
            passed, message = check['fn']()
            return {
                'name': check['name'],
                'passed': passed,
                'message': message,
                'critical': check['critical'],
                'timestamp': datetime.now().isoformat(),
                'error': None
            }
        except Exception as e:
            return {
                'name': check['name'],
                'passed': False,
                'message': f"检查执行失败: {str(e)}",
                'critical': check['critical'],
                'timestamp': datetime.now().isoformat(),
                'error': traceback.format_exc()
            }

    def run_all_checks(self) -> Dict:
        """
        运行所有检查

        返回:
            完整检查报告
        """
        self.last_check_time = datetime.now()

        results = []
        critical_failed = []
        total_passed = 0

        for check in self.checks:
            result = self.run_check(check)
            results.append(result)
            if result['passed']:
                total_passed += 1
            elif result['critical']:
                critical_failed.append(result['name'])

        return {
            'timestamp': datetime.now().isoformat(),
            'total': len(self.checks),
            'passed': total_passed,
            'failed': len(self.checks) - total_passed,
            'critical_failed': critical_failed,
            'overall_status': 'healthy' if not critical_failed else 'critical',
            'results': results
        }

    def quick_health_check(self) -> tuple[bool, str]:
        """
        快速健康检查

        返回:
            (是否健康, 状态消息)
        """
        # 检查是否到了检查时间
        if self.last_check_time:
            if datetime.now() - self.last_check_time < self.check_interval:
                return True, "上次检查正常"

        # 运行关键检查
        critical_checks = [c for c in self.checks if c['critical']]
        if not critical_checks:
            return True, "无关键检查项"

        for check in critical_checks:
            result = self.run_check(check)
            if not result['passed']:
                return False, f"关键检查失败: {result['message']}"

        return True, "健康"

    def add_default_checks(self):
        """添加默认检查项"""
        # Python版本检查
        self.register_check(
            'python_version',
            lambda: (sys.version_info >= (3, 8), f"Python {sys.version_info.major}.{sys.version_info.minor}"),
            critical=True
        )

        # 必需模块检查
        required_modules = ['math', 'json', 'datetime', 'traceback']
        self.register_check(
            'required_modules',
            lambda: self._check_modules(required_modules),
            critical=True
        )

    def _check_modules(self, modules: List[str]) -> tuple[bool, str]:
        """检查必需模块"""
        missing = []
        for mod in modules:
            try:
                __import__(mod)
            except ImportError:
                missing.append(mod)

        if missing:
            return False, f"缺少模块: {', '.join(missing)}"
        return True, "所有必需模块可用"

    def get_system_info(self) -> Dict:
        """获取系统信息"""
        return {
            'python_version': sys.version,
            'platform': sys.platform,
            'last_check': self.last_check_time.isoformat() if self.last_check_time else None,
            'registered_checks': len(self.checks),
            'timestamp': datetime.now().isoformat()
        }

    def export_report(self, filepath: str):
        """导出检查报告到文件"""
        report = self.run_all_checks()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return filepath


# 便捷函数
def quick_inspect() -> Dict:
    """快速自检"""
    inspector = SelfInspect()
    inspector.add_default_checks()
    return inspector.run_all_checks()


if __name__ == "__main__":
    inspector = SelfInspect()
    inspector.add_default_checks()

    print("=== 系统自检 ===")
    report = inspector.run_all_checks()

    print(f"\n状态: {report['overall_status']}")
    print(f"通过: {report['passed']}/{report['total']}")

    if report['critical_failed']:
        print(f"\n关键失败: {', '.join(report['critical_failed'])}")

    print("\n详细信息:")
    for r in report['results']:
        status = "✓" if r['passed'] else "✗"
        print(f"  {status} {r['name']}: {r['message']}")
