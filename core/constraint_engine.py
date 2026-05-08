"""
约束引擎 - 负责强制执行各类约束规则
"""
import yaml
from typing import Any


class ConstraintEngine:
    """约束执行引擎"""

    def __init__(self, config_path: str = None):
        self.config = {}
        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str):
        """加载约束配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def check_prompt_constraint(self, prompt: str) -> tuple[bool, str]:
        """
        检查Prompt约束
        返回: (是否通过, 原因)
        """
        # 长度约束
        max_length = self.config.get('prompt', {}).get('max_length', 4096)
        if len(prompt) > max_length:
            return False, f"Prompt长度超限: {len(prompt)} > {max_length}"

        # 危险内容检测
        forbidden = self.config.get('prompt', {}).get('forbidden_patterns', [])
        for pattern in forbidden:
            if pattern.lower() in prompt.lower():
                return False, f"包含禁止内容: {pattern}"

        return True, "通过"

    def check_response_constraint(self, response: str) -> tuple[bool, str]:
        """
        检查Response约束
        """
        max_length = self.config.get('response', {}).get('max_length', 8192)
        if len(response) > max_length:
            return False, f"Response长度超限: {len(response)} > {max_length}"

        return True, "通过"

    def check_factuality(self, claim: str, facts: list[str]) -> float:
        """
        简单事实性检查
        返回: 0-1的事实性得分
        """
        if not facts:
            return 0.5

        claim_lower = claim.lower()
        matches = sum(1 for fact in facts if fact.lower() in claim_lower)
        return matches / len(facts)

    def enforce_context_window(self, context: list, max_tokens: int) -> list:
        """
        强制上下文窗口限制
        """
        if len(context) <= max_tokens:
            return context

        # 保留最近上下文
        return context[-max_tokens:]

    def apply_constraint(self, text: str, constraint_type: str) -> str:
        """
        应用指定类型的约束
        """
        if constraint_type == "safe_output":
            # 安全输出约束
            text = text.replace("<script>", "").replace("</script>", "")
            text = text.replace("<?php", "").replace("?>", "")
        elif constraint_type == "length_limit":
            max_len = self.config.get('response', {}).get('max_length', 8192)
            if len(text) > max_len:
                text = text[:max_len] + "\n[输出已截断]"
        elif constraint_type == "no_hallucination":
            # 简单幻觉检测
            placeholders = ["[TODO]", "[FIXME]", "[placeholder]", "undefined", "null"]
            for ph in placeholders:
                text = text.replace(ph, "[已过滤占位符]")

        return text
