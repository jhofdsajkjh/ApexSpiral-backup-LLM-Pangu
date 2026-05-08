"""
LLM Hook - 拦截LLM调用进行ΔG检测
"""
from typing import Optional, Callable, Any
from core.delta_g_formula import DeltaGUnified


class LLMHook:
    """LLM调用拦截器"""

    def __init__(self, delta_g: DeltaGUnified = None):
        self.delta_g = delta_g or DeltaGUnified()
        self.hooks = []
        self.enabled = True

    def register_hook(self, hook_fn: Callable):
        """注册前置/后置钩子"""
        self.hooks.append(hook_fn)

    def pre_hook(self, prompt: str, **kwargs) -> dict:
        """
        前置钩子 - Prompt发送前调用
        返回上下文信息
        """
        context = {
            'prompt': prompt,
            'prompt_length': len(prompt),
            'timestamp': self._get_timestamp()
        }
        context.update(kwargs)

        for hook in self.hooks:
            context = hook(context, stage='pre')

        return context

    def post_hook(self, response: str, context: dict) -> dict:
        """
        后置钩子 - 响应返回后调用
        """
        context['response'] = response
        context['response_length'] = len(response)

        for hook in self.hooks:
            context = hook(context, stage='post')

        return context

    def calculate_risk(self, context: dict) -> float:
        """
        计算当前调用的风险指数
        """
        # 简单风险评估
        risk = 0.0

        # Prompt长度风险
        if context.get('prompt_length', 0) > 3000:
            risk += 0.2

        # 响应长度异常
        response_len = context.get('response_length', 0)
        if response_len == 0:
            risk += 0.3
        elif response_len > 8000:
            risk += 0.1

        return min(risk, 1.0)

    def should_block(self, risk: float, threshold: float = 0.7) -> bool:
        """
        判断是否应阻止本次调用
        """
        return risk > threshold and not self.enabled

    def enable(self):
        """启用Hook"""
        self.enabled = True

    def disable(self):
        """禁用Hook"""
        self.enabled = False

    def _get_timestamp(self) -> float:
        """获取当前时间戳"""
        import time
        return time.time()


class HookChain:
    """钩子链管理器"""

    def __init__(self):
        self.hooks = []

    def add(self, hook: Callable, priority: int = 0):
        """添加钩子(带优先级)"""
        self.hooks.append((priority, hook))
        self.hooks.sort(key=lambda x: x[0])

    def execute(self, context: dict, stage: str) -> dict:
        """执行钩子链"""
        for priority, hook in self.hooks:
            context = hook(context, stage=stage)
        return context
