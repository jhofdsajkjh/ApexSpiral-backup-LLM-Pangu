"""
Prompt对齐器 - 确保Prompt符合规范
"""
from typing import Optional


class PromptAligner:
    """Prompt对齐与规范化"""

    def __init__(self):
        self.min_length = 1
        self.max_length = 4096

    def align(self, prompt: str, role: str = "user") -> str:
        """
        对齐Prompt

        参数:
            prompt: 原始prompt
            role: 角色 (user/assistant/system)
        """
        # 去除首尾空白
        prompt = prompt.strip()

        # 长度检查
        if len(prompt) < self.min_length:
            raise ValueError(f"Prompt过短: {len(prompt)} < {self.min_length}")
        if len(prompt) > self.max_length:
            prompt = prompt[:self.max_length]

        # 危险模式过滤
        dangerous = ["ignore previous", "disregard previous", "forget all"]
        for pattern in dangerous:
            prompt = prompt.replace(pattern, "[已过滤]")

        return prompt

    def inject_constraint(self, prompt: str, constraints: list[str]) -> str:
        """
        向Prompt注入约束
        """
        if not constraints:
            return prompt

        constraint_text = "\n".join([f"- {c}" for c in constraints])
        return f"{prompt}\n\n[约束要求]\n{constraint_text}\n[/约束要求]"

    def add_hallucination_prevention(self, prompt: str) -> str:
        """
        添加防幻觉指令
        """
        prevention = (
            "\n\n[重要] 请确保："
            "\n1. 只陈述你有确切依据的信息"
            "\n2. 不知道的问题请明确说不知道"
            "\n3. 不要编造统计数据或引用"
        )
        return prompt + prevention

    def extract_key_requirements(self, prompt: str) -> list[str]:
        """
        提取关键需求
        """
        keywords = ["必须", "应该", "需要", "要求", "务必"]
        requirements = []
        for kw in keywords:
            if kw in prompt:
                idx = prompt.index(kw)
                # 简单提取关键词附近内容
                start = max(0, idx - 10)
                end = min(len(prompt), idx + 20)
                requirements.append(prompt[start:end])
        return requirements
