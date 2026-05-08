"""
内存钩子 - 与主系统内存交互
"""
from typing import Optional, Dict, Any, List
from memory.memory_persist import MemoryPersist


class MemoryHook:
    """内存钩子管理器"""

    def __init__(self, persist: MemoryPersist = None):
        self.persist = persist or MemoryPersist()
        self.cache: Dict[str, Any] = {}
        self.max_cache_size = 100

    def remember(self, key: str, value: Any, persist: bool = True) -> bool:
        """
        记住关键信息

        参数:
            key: 键名
            value: 值
            persist: 是否持久化
        """
        # 更新缓存
        self.cache[key] = value
        if len(self.cache) > self.max_cache_size:
            # 移除最老的缓存
            oldest = next(iter(self.cache))
            del self.cache[oldest]

        # 持久化
        if persist:
            return self.persist.save(key, value)
        return True

    def recall(self, key: str, use_cache: bool = True) -> Optional[Any]:
        """
        回忆信息
        """
        # 优先从缓存读取
        if use_cache and key in self.cache:
            return self.cache[key]

        # 从持久化读取
        data = self.persist.load(key)
        if data:
            self.cache[key] = data
        return data

    def forget(self, key: str, persist: bool = True) -> bool:
        """
        遗忘信息
        """
        # 从缓存移除
        if key in self.cache:
            del self.cache[key]

        # 从持久化删除
        if persist:
            return self.persist.delete(key)
        return True

    def update_memory(self, key: str, value: Any, merge: bool = True) -> bool:
        """
        更新记忆

        参数:
            key: 键名
            value: 新值
            merge: 是否与旧值合并
        """
        if merge and not merge:
            return self.remember(key, value)

        old_value = self.recall(key) or {}
        if isinstance(old_value, dict) and isinstance(value, dict):
            old_value.update(value)
            value = old_value

        return self.remember(key, value)

    def get_context(self, keys: List[str]) -> Dict[str, Any]:
        """
        获取多个键的上下文
        """
        context = {}
        for key in keys:
            value = self.recall(key)
            if value is not None:
                context[key] = value
        return context

    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()

    def get_all_keys(self) -> List[str]:
        """获取所有键名"""
        persist_keys = self.persist.list_keys()
        cache_keys = list(self.cache.keys())
        return list(set(persist_keys + cache_keys))
