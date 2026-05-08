"""
双记忆架构
M_global: 公式库/技能模板/最优轨迹（全员共享）
Mu_agent_mem: 各Agent独立人格/任务历史（隔离存储）

璇玑帝国核心架构 - 2026-05-08
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
import json
import os
import threading
from pathlib import Path


@dataclass
class GlobalMemory:
    """全局共享记忆 - 所有Agent共享
    
    M_global: 公式库/技能模板/最优轨迹（全员共享）
    存储在共享路径，所有Agent可读可写
    """
    formula_library: Dict[str, Any] = field(default_factory=dict)  # 公式库
    skill_templates: Dict[str, Any] = field(default_factory=dict)  # 技能模板
    optimal_trajectories: Dict[str, Any] = field(default_factory=dict)  # 最优轨迹
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    
    def save(self, path: str) -> bool:
        """保存全局记忆到文件"""
        with self._lock:
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                data = {
                    'formula_library': self.formula_library,
                    'skill_templates': self.skill_templates,
                    'optimal_trajectories': self.optimal_trajectories,
                    '_version': '1.0',
                    '_updated': self._timestamp()
                }
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return True
            except Exception as e:
                print(f"[DualMemory] Global save error: {e}")
                return False
    
    @classmethod
    def load(cls, path: str) -> 'GlobalMemory':
        """从文件加载全局记忆"""
        if not os.path.exists(path):
            return cls()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            instance = cls(
                formula_library=data.get('formula_library', {}),
                skill_templates=data.get('skill_templates', {}),
                optimal_trajectories=data.get('optimal_trajectories', {})
            )
            return instance
        except Exception as e:
            print(f"[DualMemory] Global load error: {e}")
            return cls()
    
    def add_formula(self, key: str, formula: Dict[str, Any]) -> None:
        """添加公式到库"""
        with self._lock:
            self.formula_library[key] = formula
    
    def get_formula(self, key: str) -> Optional[Dict[str, Any]]:
        """获取公式"""
        return self.formula_library.get(key)
    
    def add_skill_template(self, key: str, template: Dict[str, Any]) -> None:
        """添加技能模板"""
        with self._lock:
            self.skill_templates[key] = template
    
    def add_optimal_trajectory(self, key: str, trajectory: Dict[str, Any]) -> None:
        """记录最优轨迹"""
        with self._lock:
            self.optimal_trajectories[key] = trajectory
    
    @staticmethod
    def _timestamp() -> str:
        from datetime import datetime
        return datetime.now().isoformat()


@dataclass
class AgentMemory:
    """Agent私有记忆 - 隔离存储
    
    Mu_agent_mem: 各Agent独立人格/任务历史（隔离存储）
    每个Agent独立存储，人格参数和任务历史互不干扰
    """
    agent_id: str
    personality: Dict[str, Any] = field(default_factory=dict)  # 人格参数
    task_history: List[Dict[str, Any]] = field(default_factory=list)  # 任务历史
    learned_skills: List[str] = field(default_factory=list)  # 已学技能
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    
    def __post_init__(self):
        if not self.agent_id:
            raise ValueError("agent_id cannot be empty")
    
    def save(self, path: str) -> bool:
        """保存Agent私有记忆"""
        with self._lock:
            try:
                os.makedirs(path, exist_ok=True)
                file_path = os.path.join(path, f"{self.agent_id}_memory.json")
                data = {
                    'agent_id': self.agent_id,
                    'personality': self.personality,
                    'task_history': self.task_history,
                    'learned_skills': self.learned_skills,
                    '_version': '1.0',
                    '_updated': self._timestamp()
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return True
            except Exception as e:
                print(f"[DualMemory] Agent save error: {e}")
                return False
    
    @classmethod
    def load(cls, agent_id: str, path: str) -> Optional['AgentMemory']:
        """从文件加载Agent记忆"""
        file_path = os.path.join(path, f"{agent_id}_memory.json")
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(
                agent_id=data['agent_id'],
                personality=data.get('personality', {}),
                task_history=data.get('task_history', []),
                learned_skills=data.get('learned_skills', [])
            )
        except Exception as e:
            print(f"[DualMemory] Agent load error: {e}")
            return None
    
    def add_task(self, task: Dict[str, Any]) -> None:
        """添加任务到历史"""
        with self._lock:
            self.task_history.append({
                **task,
                '_timestamp': self._timestamp()
            })
            # 保留最近100条任务
            if len(self.task_history) > 100:
                self.task_history = self.task_history[-100:]
    
    def learn_skill(self, skill_name: str) -> None:
        """标记学会新技能"""
        with self._lock:
            if skill_name not in self.learned_skills:
                self.learned_skills.append(skill_name)
    
    def update_personality(self, updates: Dict[str, Any]) -> None:
        """更新人格参数"""
        with self._lock:
            self.personality.update(updates)
    
    @staticmethod
    def _timestamp() -> str:
        from datetime import datetime
        return datetime.now().isoformat()


class DualMemoryManager:
    """双记忆管理器 - 统一管理M_global和Mu_agent_mem
    
    使用示例:
        manager = DualMemoryManager("/data/memory")
        
        # 全局操作
        manager.global_add_formula("delta_g", {"formula": "ΔG = (C×Λ×Ω)/(H×t)"})
        
        # Agent操作
        agent_mem = manager.get_agent_memory("agent_001")
        agent_mem.add_task({"task": "优化代码", "score": 0.95})
        agent_mem.save()
    """
    
    def __init__(self, base_path: str = "/root/.openclaw/workspace/pangu/storage/dual_memory"):
        self.base_path = base_path
        self.global_path = os.path.join(base_path, "global", "shared_memory.json")
        self.agent_path = os.path.join(base_path, "agents")
        
        # 缓存
        self._global_cache: Optional[GlobalMemory] = None
        self._agent_cache: Dict[str, AgentMemory] = {}
        
        # 确保目录存在
        os.makedirs(os.path.dirname(self.global_path), exist_ok=True)
        os.makedirs(self.agent_path, exist_ok=True)
    
    @property
    def global_memory(self) -> GlobalMemory:
        """获取全局共享记忆（懒加载+缓存）"""
        if self._global_cache is None:
            self._global_cache = GlobalMemory.load(self.global_path)
        return self._global_cache
    
    def get_agent_memory(self, agent_id: str) -> AgentMemory:
        """获取Agent私有记忆（懒加载+缓存）"""
        if agent_id not in self._agent_cache:
            loaded = AgentMemory.load(agent_id, self.agent_path)
            if loaded:
                self._agent_cache[agent_id] = loaded
            else:
                self._agent_cache[agent_id] = AgentMemory(agent_id=agent_id)
        return self._agent_cache[agent_id]
    
    def save_all(self) -> Dict[str, bool]:
        """保存所有记忆"""
        results = {
            'global': self.global_memory.save(self.global_path)
        }
        
        for agent_id, agent_mem in self._agent_cache.items():
            results[f'agent_{agent_id}'] = agent_mem.save(self.agent_path)
        
        return results
    
    def sync_global(self) -> bool:
        """同步全局记忆到磁盘"""
        return self.global_memory.save(self.global_path)
    
    def list_agents(self) -> List[str]:
        """列出所有Agent ID"""
        if not os.path.exists(self.agent_path):
            return []
        files = os.listdir(self.agent_path)
        return [f.replace('_memory.json', '') for f in files if f.endswith('_memory.json')]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        return {
            'global': {
                'formula_count': len(self.global_memory.formula_library),
                'skill_template_count': len(self.global_memory.skill_templates),
                'trajectory_count': len(self.global_memory.optimal_trajectories)
            },
            'agents': {
                'cached': len(self._agent_cache),
                'total_files': len(self.list_agents())
            }
        }
