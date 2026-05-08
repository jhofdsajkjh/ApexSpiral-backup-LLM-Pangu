"""
内存持久化模块
"""
import json
import os
from typing import Any, Optional
from datetime import datetime


class MemoryPersist:
    """内存数据持久化"""

    def __init__(self, storage_dir: str = "storage"):
        self.storage_dir = storage_dir
        self._ensure_storage_dir()

    def _ensure_storage_dir(self):
        """确保存储目录存在"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def save(self, key: str, data: Any, metadata: dict = None) -> bool:
        """
        保存数据到持久化存储

        参数:
            key: 数据键名
            data: 要保存的数据
            metadata: 元数据
        """
        try:
            filepath = os.path.join(self.storage_dir, f"{key}.json")
            record = {
                'key': key,
                'data': data,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False

    def load(self, key: str) -> Optional[Any]:
        """加载数据"""
        try:
            filepath = os.path.join(self.storage_dir, f"{key}.json")
            if not os.path.exists(filepath):
                return None
            with open(filepath, 'r', encoding='utf-8') as f:
                record = json.load(f)
            return record.get('data')
        except Exception as e:
            print(f"加载失败: {e}")
            return None

    def delete(self, key: str) -> bool:
        """删除数据"""
        try:
            filepath = os.path.join(self.storage_dir, f"{key}.json")
            if os.path.exists(filepath):
                os.remove(filepath)
            return True
        except Exception:
            return False

    def list_keys(self) -> list[str]:
        """列出所有键"""
        if not os.path.exists(self.storage_dir):
            return []
        return [f.replace('.json', '') for f in os.listdir(self.storage_dir) if f.endswith('.json')]

    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        filepath = os.path.join(self.storage_dir, f"{key}.json")
        return os.path.exists(filepath)

    def get_metadata(self, key: str) -> Optional[dict]:
        """获取元数据"""
        record = self.load(key)
        return record.get('metadata') if record else None
