"""
自动技能拉取模块
"""
import os
import json
import requests
from typing import Optional, Dict, List
from datetime import datetime


class AutoSkillFetch:
    """自动从远程源拉取技能"""

    def __init__(self, config_path: str = None):
        self.sources: List[Dict] = []
        self.local_skills_dir = "skills"
        self._ensure_skills_dir()

        if config_path and os.path.exists(config_path):
            self._load_config(config_path)

    def _ensure_skills_dir(self):
        """确保技能目录存在"""
        if not os.path.exists(self.local_skills_dir):
            os.makedirs(self.local_skills_dir)

    def _load_config(self, config_path: str):
        """加载配置"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.sources = config.get('skill_sources', [])

    def add_source(self, name: str, url: str, type: str = "github"):
        """
        添加技能源

        参数:
            name: 源名称
            url: 源URL
            type: 源类型 (github/file/raw)
        """
        self.sources.append({
            'name': name,
            'url': url,
            'type': type,
            'added_at': datetime.now().isoformat()
        })

    def fetch_skill(self, skill_name: str, source_url: str) -> Optional[str]:
        """
        从指定源拉取技能

        返回:
            技能文件路径，失败返回None
        """
        try:
            response = requests.get(source_url, timeout=30)
            if response.status_code == 200:
                local_path = os.path.join(self.local_skills_dir, f"{skill_name}.py")
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                return local_path
        except Exception as e:
            print(f"拉取失败: {e}")
        return None

    def fetch_from_github(self, repo: str, skill_path: str, branch: str = "main") -> Optional[str]:
        """
        从GitHub拉取技能
        """
        raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{skill_path}"
        skill_name = os.path.basename(skill_path).replace('.py', '')
        return self.fetch_skill(skill_name, raw_url)

    def sync_all(self) -> Dict[str, bool]:
        """
        同步所有技能源
        """
        results = {}
        for source in self.sources:
            if source['type'] == 'github':
                # GitHub源处理
                results[source['name']] = False
            elif source['type'] == 'file':
                # 本地文件源处理
                results[source['name']] = False
            elif source['type'] == 'raw':
                # 原始URL源处理
                skill_name = os.path.basename(source['url']).replace('.py', '')
                result = self.fetch_skill(skill_name, source['url'])
                results[source['name']] = result is not None
        return results

    def list_local_skills(self) -> List[str]:
        """列出本地技能"""
        if not os.path.exists(self.local_skills_dir):
            return []
        return [f.replace('.py', '') for f in os.listdir(self.local_skills_dir) if f.endswith('.py')]

    def remove_skill(self, skill_name: str) -> bool:
        """删除本地技能"""
        filepath = os.path.join(self.local_skills_dir, f"{skill_name}.py")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
