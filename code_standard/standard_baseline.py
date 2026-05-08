"""
代码标准基线 - 定义代码质量基线
"""
import ast
from typing import List, Dict, Optional


class StandardBaseline:
    """代码标准基线"""

    def __init__(self):
        self.rules = self._default_rules()

    def _default_rules(self) -> Dict:
        """默认规则集"""
        return {
            'max_function_length': 100,
            'max_complexity': 10,
            'min_docstring_length': 10,
            'allowed_imports': [],
            'forbidden_patterns': ['pass\n\n\n', 'except:\n    pass'],
            'naming_convention': {
                'function': 'snake_case',
                'class': 'PascalCase',
                'constant': 'UPPER_SNAKE_CASE'
            }
        }

    def check_function_length(self, source: str, function_name: str) -> bool:
        """
        检查函数长度是否超标
        """
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    return len(node.body) <= self.rules['max_function_length']
        except:
            pass
        return True

    def check_complexity(self, source: str) -> int:
        """
        计算代码复杂度
        """
        try:
            tree = ast.parse(source)
            complexity = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
            return complexity
        except:
            return 0

    def check_docstring(self, source: str, function_name: str) -> bool:
        """
        检查函数是否有文档字符串
        """
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    has_docstring = (
                        ast.get_docstring(node) is not None and
                        len(ast.get_docstring(node) or '') >= self.rules['min_docstring_length']
                    )
                    return has_docstring
        except:
            pass
        return False

    def check_naming(self, name: str, name_type: str) -> bool:
        """
        检查命名是否符合规范
        """
        convention = self.rules['naming_convention'].get(name_type, 'snake_case')

        if convention == 'snake_case':
            return name.islower() and '_' in name
        elif convention == 'PascalCase':
            return name[0].isupper() and '_' not in name
        elif convention == 'UPPER_SNAKE_CASE':
            return name.isupper() and '_' in name

        return True

    def validate_source(self, source: str) -> Dict[str, any]:
        """
        验证源代码是否符合标准
        """
        issues = []
        complexity = self.check_complexity(source)

        if complexity > self.rules['max_complexity']:
            issues.append(f"复杂度超标: {complexity} > {self.rules['max_complexity']}")

        # 检查禁止模式
        for pattern in self.rules['forbidden_patterns']:
            if pattern in source:
                issues.append(f"包含禁止模式: {pattern.strip()}")

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'complexity': complexity
        }

    def get_baseline_info(self) -> Dict:
        """获取基线信息"""
        return {
            'rules': self.rules,
            'version': '1.0.0'
        }
