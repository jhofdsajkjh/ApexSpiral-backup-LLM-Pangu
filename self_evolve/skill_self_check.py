"""
技能自检模块 - 自动检查和更新技能
"""
import os
import json
import hashlib
from typing import Dict, List, Optional
from datetime import datetime


class SkillSelfCheck:
    """技能自检器"""

    def __init__(self, skill_dir: str = "skills"):
        self.skill_dir = skill_dir
        self.manifest_path = os.path.join(skill_dir, "manifest.json")
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> dict:
        """加载技能清单"""
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_manifest(self):
        """保存技能清单"""
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, ensure_ascii=False, indent=2)

    def register_skill(self, skill_name: str, skill_path: str, version: str = "1.0.0") -> bool:
        """
        注册技能
        """
        self.manifest[skill_name] = {
            'path': skill_path,
            'version': version,
            'registered_at': datetime.now().isoformat(),
            'status': 'active'
        }
        self._save_manifest()
        return True

    def unregister_skill(self, skill_name: str) -> bool:
        """
        注销技能
        """
        if skill_name in self.manifest:
            del self.manifest[skill_name]
            self._save_manifest()
            return True
        return False

    def check_skill_integrity(self, skill_name: str) -> Dict[str, any]:
        """
        检查技能完整性
        """
        if skill_name not in self.manifest:
            return {'valid': False, 'reason': 'Skill not registered'}

        skill_info = self.manifest[skill_name]
        skill_path = skill_info['path']

        if not os.path.exists(skill_path):
            return {'valid': False, 'reason': 'Skill file not found'}

        # 计算文件哈希
        file_hash = self._calculate_file_hash(skill_path)

        return {
            'valid': True,
            'hash': file_hash,
            'size': os.path.getsize(skill_path),
            'last_modified': datetime.fromtimestamp(os.path.getmtime(skill_path)).isoformat()
        }

    def _calculate_file_hash(self, filepath: str) -> str:
        """计算文件哈希"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def list_skills(self) -> List[str]:
        """列出所有技能"""
        return list(self.manifest.keys())

    def get_skill_info(self, skill_name: str) -> Optional[dict]:
        """获取技能信息"""
        return self.manifest.get(skill_name)

    def validate_all(self) -> Dict[str, bool]:
        """验证所有技能"""
        results = {}
        for skill_name in self.manifest:
            result = self.check_skill_integrity(skill_name)
            results[skill_name] = result['valid']
        return results
