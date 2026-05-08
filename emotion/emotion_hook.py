"""
EmotionHook - 情绪挂钩，整合情绪感知到响应生成流程
"""
from typing import Dict, Optional, Callable, List
from emotion.emotion_core import EmotionCore


class EmotionHook:
    """
    情绪挂钩 - 将情绪感知嵌入AI响应系统

    功能:
    1. 实时情绪检测
    2. 情绪感知响应调整
    3. 情绪波动监控
    4. 负面情绪安抚触发
    """

    def __init__(self, emotion_core: EmotionCore = None):
        self.emotion_core = emotion_core or EmotionCore()
        self.enabled = True
        self.hooks: List[Callable] = []
        self.response_modifiers: List[Callable] = []

    def register_hook(self, hook_fn: Callable):
        """注册情绪变化钩子"""
        self.hooks.append(hook_fn)

    def register_modifier(self, modifier_fn: Callable):
        """注册响应修饰器"""
        self.response_modifiers.append(modifier_fn)

    def on_input_received(self, text: str, context: Dict = None) -> Dict:
        """
        输入到达时的情绪处理

        参数:
            text: 用户输入文本
            context: 额外上下文

        返回:
            情绪分析结果
        """
        emotion_result = self.emotion_core.detect_emotion(text, context)

        # 触发钩子
        for hook in self.hooks:
            hook(emotion_result, event='input')

        # 检查是否需要响应调整
        if self.emotion_core.should_adjust_response():
            emotion_result['needs_adjustment'] = True

        return emotion_result

    def on_before_response(self, base_response: str, emotion_context: Dict) -> str:
        """
        生成响应前的情绪调整

        参数:
            base_response: 基础响应
            emotion_context: 情绪上下文

        返回:
            调整后的响应
        """
        if not self.enabled:
            return base_response

        emotion = emotion_context.get('emotion', 'neutral')
        intensity = emotion_context.get('intensity', 0)

        modified = base_response

        # 应用修饰器
        for modifier in self.response_modifiers:
            modified = modifier(modified, emotion, intensity)

        # 高强度负面情绪自动添加安抚
        if intensity > 0.7 and emotion in ['anger', 'fear', 'sadness']:
            modified = self._add_comfort(modified, emotion)

        return modified

    def _add_comfort(self, response: str, emotion: str) -> str:
        """
        添加情绪安抚文本
        """
        comfort_templates = {
            'anger': "\n\n我理解您可能感到不满，我会尽力提供更好的帮助。",
            'fear': "\n\n别担心，让我们一起解决这个问题。",
            'sadness': "\n\n我理解您的心情，希望我能帮上一些忙。",
        }

        template = comfort_templates.get(emotion, "")
        return response + template

    def on_output_sent(self, response: str):
        """
        响应发送后的处理
        """
        # 触发钩子
        for hook in self.hooks:
            hook({'response': response}, event='output')

    def get_emotion_state(self) -> Dict:
        """获取当前情绪状态"""
        return {
            'current': self.emotion_core.get_current_emotion(),
            'history': self.emotion_core.get_emotion_history(limit=5),
            'summary': self.emotion_core.generate_emotion_summary()
        }

    def is_emotion_stable(self) -> bool:
        """检查情绪是否稳定"""
        return not self.emotion_core.is_emotion_shifted(threshold=0.3)

    def reset_emotion(self):
        """重置情绪状态"""
        self.emotion_core.current_emotion = EmotionCore.BASE_EMOTIONS['neutral'].copy()
        self.emotion_core.emotion_history.clear()

    def enable(self):
        """启用情绪感知"""
        self.enabled = True

    def disable(self):
        """禁用情绪感知"""
        self.enabled = False

    def get_emotion_stats(self) -> Dict:
        """获取情绪统计"""
        history = self.emotion_core.emotion_history
        if not history:
            return {'total': 0, 'avg_intensity': 0}

        total_intensity = sum(h.get('intensity', 0) for h in history)
        emotion_counts = {}

        for h in history:
            emotion = h.get('emotion', 'neutral')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        return {
            'total': len(history),
            'avg_intensity': round(total_intensity / len(history), 2),
            'dominant_emotion': max(emotion_counts, key=emotion_counts.get) if emotion_counts else 'neutral',
            'emotion_distribution': emotion_counts
        }


class EmotionAwareResponse:
    """
    情绪感知响应生成器
    根据情绪状态生成差异化响应
    """

    def __init__(self, emotion_hook: EmotionHook = None):
        self.hook = emotion_hook or EmotionHook()

    def generate_response(self, prompt: str, base_response: str) -> str:
        """
        根据情绪生成差异化响应

        参数:
            prompt: 用户提示
            base_response: 基础响应

        返回:
            调整后的响应
        """
        emotion_context = self.hook.on_input_received(prompt)
        adjusted_response = self.hook.on_before_response(base_response, emotion_context)
        self.hook.on_output_sent(adjusted_response)

        return adjusted_response

    def wrap_with_emotion_metadata(self, response: str) -> Dict:
        """
        包装响应，添加情绪元数据
        """
        emotion_state = self.hook.get_emotion_state()

        return {
            'response': response,
            'emotion': emotion_state['current'],
            'emotion_summary': emotion_state['summary'],
            'is_stable': self.hook.is_emotion_stable()
        }
