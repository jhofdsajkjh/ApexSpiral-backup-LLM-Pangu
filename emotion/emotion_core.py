"""
EmotionCore - 情绪核心引擎
负责检测、追踪和响应用户情绪状态
"""
import math
from typing import Dict, Optional, List
from datetime import datetime


class EmotionCore:
    """情绪核心引擎 - APEX情绪感知层"""

    # 情绪维度定义
    EMOTION_DIMENSIONS = ['valence', 'arousal', 'dominance']

    # 基础情绪类型
    BASE_EMOTIONS = {
        'joy': {'vector': [0.9, 0.7, 0.8], 'icon': '😊'},
        'sadness': {'vector': [0.2, 0.4, 0.3], 'icon': '😢'},
        'anger': {'vector': [0.1, 0.9, 0.7], 'icon': '😠'},
        'fear': {'vector': [0.15, 0.85, 0.2], 'icon': '😨'},
        'surprise': {'vector': [0.7, 0.8, 0.5], 'icon': '😮'},
        'disgust': {'vector': [0.1, 0.6, 0.4], 'icon': '😒'},
        'neutral': {'vector': [0.5, 0.5, 0.5], 'icon': '😐'},
    }

    def __init__(self):
        self.current_emotion: Dict = self.BASE_EMOTIONS['neutral'].copy()
        self.emotion_history: List[Dict] = []
        self.max_history = 100
        self.intensity_threshold = 0.6

    def detect_emotion(self, text: str, context: Dict = None) -> Dict:
        """
        从文本中检测情绪

        参数:
            text: 输入文本
            context: 额外上下文信息

        返回:
            情绪分析结果，包含主情绪、强度和子情绪
        """
        text_lower = text.lower()

        # 关键词情绪映射
        emotion_keywords = {
            'joy': ['开心', '高兴', '快乐', '棒', '太好了', 'good', 'great', 'happy', 'joy', 'wonderful', '太好了', '完美', '赞'],
            'sadness': ['难过', '伤心', '悲伤', '失落', '沮丧', 'sad', 'unhappy', 'depressed', '难过', '可惜'],
            'anger': ['生气', '愤怒', '恼火', '讨厌', '烦', 'angry', 'mad', 'hate', 'furious', '可恶'],
            'fear': ['害怕', '担心', '紧张', '恐惧', '不安', 'fear', 'scared', 'worried', 'anxious', '慌'],
            'surprise': ['惊讶', '意外', '震惊', '没想到', 'surprise', 'amazing', 'shocked', '惊讶'],
            'disgust': ['恶心', '讨厌', '厌恶', '反感', 'disgust', 'gross', '讨厌', '嫌弃'],
        }

        scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[emotion] = min(score / len(keywords), 1.0)

        if not scores:
            return self._build_response('neutral', 0.3)

        # 找最高分情绪
        primary = max(scores, key=scores.get)
        intensity = scores[primary]

        return self._build_response(primary, intensity)

    def _build_response(self, emotion: str, intensity: float) -> Dict:
        """构建情绪响应"""
        response = {
            'emotion': emotion,
            'intensity': intensity,
            'icon': self.BASE_EMOTIONS.get(emotion, {}).get('icon', '😐'),
            'vector': self.BASE_EMOTIONS.get(emotion, {}).get('vector', [0.5, 0.5, 0.5]),
            'timestamp': datetime.now().isoformat()
        }

        # 更新当前情绪
        if intensity >= self.intensity_threshold:
            self.current_emotion = response.copy()
            self._add_to_history(response)

        return response

    def _add_to_history(self, emotion_data: Dict):
        """添加到历史记录"""
        self.emotion_history.append(emotion_data)
        if len(self.emotion_history) > self.max_history:
            self.emotion_history.pop(0)

    def get_current_emotion(self) -> Dict:
        """获取当前情绪状态"""
        return self.current_emotion.copy()

    def get_emotion_history(self, limit: int = 10) -> List[Dict]:
        """获取情绪历史"""
        return self.emotion_history[-limit:]

    def calculate_emotion_distance(self, e1: Dict, e2: Dict) -> float:
        """
        计算两个情绪向量之间的欧几里得距离
        """
        v1 = e1.get('vector', [0.5, 0.5, 0.5])
        v2 = e2.get('vector', [0.5, 0.5, 0.5])

        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))
        return round(distance, 4)

    def is_emotion_shifted(self, threshold: float = 0.3) -> bool:
        """
        检测情绪是否发生显著变化
        """
        if len(self.emotion_history) < 2:
            return False

        recent = self.emotion_history[-1]
        previous = self.emotion_history[-2]

        distance = self.calculate_emotion_distance(recent, previous)
        return distance > threshold

    def should_adjust_response(self) -> bool:
        """
        判断是否需要调整响应策略
        """
        current_intensity = self.current_emotion.get('intensity', 0)

        # 高强度负面情绪需要调整
        if current_intensity > 0.8:
            emotion = self.current_emotion.get('emotion', 'neutral')
            if emotion in ['anger', 'fear', 'sadness']:
                return True

        return False

    def generate_emotion_summary(self) -> str:
        """生成情绪摘要"""
        if not self.emotion_history:
            return "暂无情绪记录"

        recent = self.emotion_history[-1]
        emotion = recent['emotion']
        intensity = recent['intensity']

        if intensity < 0.3:
            return f"当前情绪平稳 ({emotion})"
        elif intensity < 0.6:
            return f"情绪略有波动 ({emotion})"
        else:
            return f"情绪波动明显 ({emotion}, 强度: {intensity:.1%})"


if __name__ == "__main__":
    engine = EmotionCore()

    test_texts = [
        "今天太开心了！",
        "这个问题让我很担心",
        "简直是在开玩笑！",
        "无所谓，随便吧",
    ]

    for text in test_texts:
        result = engine.detect_emotion(text)
        print(f"文本: {text}")
        print(f"情绪: {result['emotion']} {result['icon']}, 强度: {result['intensity']:.2f}")
        print()
