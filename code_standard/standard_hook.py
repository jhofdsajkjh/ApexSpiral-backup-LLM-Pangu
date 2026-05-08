"""
代码标准钩子
"""
from typing import Dict, List, Callable
from code_standard.standard_baseline import StandardBaseline
from code_standard.code_compliance import CodeCompliance


class StandardHook:
    """代码标准钩子"""

    def __init__(self):
        self.baseline = StandardBaseline()
        self.compliance = CodeCompliance()
        self.enabled = True
        self.hooks: List[Callable] = []

    def register_hook(self, hook_fn: Callable):
        """注册钩子函数"""
        self.hooks.append(hook_fn)

    def pre_check(self, code: str) -> Dict:
        """
        代码提交前检查
        """
        results = {
            'baseline': self.baseline.validate_source(code),
            'compliance': self.compliance.check_all(code)
        }

        # 执行自定义钩子
        for hook in self.hooks:
            results = hook(results, stage='pre')

        return results

    def post_check(self, code: str, baseline_results: Dict) -> Dict:
        """
        代码提交后检查
        """
        # 执行自定义钩子
        for hook in self.hooks:
            baseline_results = hook(baseline_results, stage='post')

        return baseline_results

    def auto_fix(self, code: str) -> str:
        """
        自动修复简单问题
        """
        # 修复行尾空格
        code = '\n'.join(line.rstrip() for line in code.split('\n'))

        # 修复制表符
        code = code.replace('\t', '    ')

        return code

    def is_compliant(self, code: str) -> bool:
        """判断代码是否合规"""
        result = self.compliance.check_all(code)
        return result['passed'] and result['total_issues'] == 0

    def get_report(self, code: str) -> Dict:
        """
        生成完整报告
        """
        baseline_result = self.baseline.validate_source(code)
        compliance_result = self.compliance.check_all(code)

        return {
            'baseline': baseline_result,
            'compliance': compliance_result,
            'overall_score': self.compliance.get_compliance_score(code),
            'passed': baseline_result['valid'] and compliance_result['passed']
        }
