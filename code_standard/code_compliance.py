"""
代码合规性检查器
"""
import re
from typing import List, Dict, Tuple


class CodeCompliance:
    """代码合规性检查器"""

    def __init__(self):
        self.rules = self._init_rules()

    def _init_rules(self) -> Dict:
        """初始化规则"""
        return {
            'security': [
                (r'system\(|exec\(|eval\(', '危险函数使用'),
                (r'os\.system|subprocess', '系统命令调用需审查'),
                (r'password\s*=|secret\s*=', '敏感信息需加密存储'),
            ],
            'style': [
                (r'\t', '使用空格而非制表符'),
                (r'\r\n', '使用Unix换行符'),
                (r'\s+$', '行尾多余空格'),
            ],
            'safety': [
                (r'pickle\.load', 'pickle可能存在安全风险'),
                (r'yaml\.load.*Loader=None', 'yaml.load需指定Loader'),
                (r'SQL', 'SQL注入风险检查'),
            ]
        }

    def check_security(self, code: str) -> List[Dict]:
        """安全检查"""
        issues = []
        for pattern, message in self.rules['security']:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                issues.append({
                    'type': 'security',
                    'message': message,
                    'line': line_num,
                    'pattern': match.group()
                })
        return issues

    def check_style(self, code: str) -> List[Dict]:
        """样式检查"""
        issues = []
        for pattern, message in self.rules['style']:
            matches = re.finditer(pattern, code)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                issues.append({
                    'type': 'style',
                    'message': message,
                    'line': line_num,
                    'pattern': match.group()
                })
        return issues

    def check_safety(self, code: str) -> List[Dict]:
        """安全检查(额外)"""
        issues = []
        for pattern, message in self.rules['safety']:
            matches = re.finditer(pattern, code)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                issues.append({
                    'type': 'safety',
                    'message': message,
                    'line': line_num,
                    'pattern': match.group()
                })
        return issues

    def check_all(self, code: str) -> Dict:
        """执行所有检查"""
        security_issues = self.check_security(code)
        style_issues = self.check_style(code)
        safety_issues = self.check_safety(code)

        all_issues = security_issues + style_issues + safety_issues

        return {
            'passed': len(all_issues) == 0,
            'total_issues': len(all_issues),
            'security_issues': len(security_issues),
            'style_issues': len(style_issues),
            'safety_issues': len(safety_issues),
            'issues': all_issues
        }

    def add_rule(self, rule_type: str, pattern: str, message: str):
        """添加自定义规则"""
        if rule_type in self.rules:
            self.rules[rule_type].append((pattern, message))
        else:
            self.rules[rule_type] = [(pattern, message)]

    def get_compliance_score(self, code: str) -> float:
        """
        计算合规性得分 (0-100)
        """
        result = self.check_all(code)
        total_checks = sum(len(issues) for issues in self.rules.values())
        if total_checks == 0:
            return 100.0

        passed_checks = total_checks - result['total_issues']
        return round(passed_checks / total_checks * 100, 2)
