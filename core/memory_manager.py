"""
Memory Manager - 双记忆架构集成层

集成 GlobalMemory(M_global) 和 AgentMemory(Mu_agent_mem) 到璇玑帝国Pangu系统

璇玑帝国核心架构 - 2026-05-08
"""
from typing import Dict, Any, Optional, List
import threading
import os

from .dual_memory import GlobalMemory, AgentMemory, DualMemoryManager


# 全局单例记忆管理器
_manager_lock = threading.Lock()
_manager_instance: Optional['MemoryManager'] = None


class MemoryManager:
    """璇玑帝国统一记忆管理器
    
    集成双记忆架构:
    - M_global: 全局共享记忆（公式库/技能模板/最优轨迹）
    - Mu_agent_mem: Agent私有记忆（人格/任务历史/已学技能）
    
    使用示例:
        # 获取单例
        mm = MemoryManager.get_instance()
        
        # 全局操作
        mm.register_formula("ΔG", {"expr": "(C×Λ×Ω)/(H×t)", "desc": "演化增益公式"})
        
        # Agent操作
        mm.log_task("agent_001", {"task": "solidify", "quality": 0.92})
        mm.update_personality("agent_001", {"creativity": 0.85, "caution": 0.6})
    """
    
    _instance = None
    
    def __new__(cls, base_path: str = "/root/.openclaw/workspace/pangu/storage/dual_memory"):
        with _manager_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self, base_path: str = "/root/.openclaw/workspace/pangu/storage/dual_memory"):
        if self._initialized:
            return
        self.base_path = base_path
        self._dual_mgr = DualMemoryManager(base_path)
        self._initialized = True
    
    @classmethod
    def get_instance(cls, base_path: str = "/root/.openclaw/workspace/pangu/storage/dual_memory") -> 'MemoryManager':
        """获取单例实例"""
        return cls(base_path)
    
    # ─────────────────────────────────────────────────────────────
    # M_global 全局共享记忆操作
    # ─────────────────────────────────────────────────────────────
    
    def register_formula(self, name: str, formula_data: Dict[str, Any]) -> None:
        """注册公式到全局公式库"""
        self._dual_mgr.global_memory.add_formula(name, formula_data)
    
    def get_formula(self, name: str) -> Optional[Dict[str, Any]]:
        """获取公式"""
        return self._dual_mgr.global_memory.get_formula(name)
    
    def list_formulas(self) -> List[str]:
        """列出所有公式"""
        return list(self._dual_mgr.global_memory.formula_library.keys())
    
    def register_skill_template(self, name: str, template_data: Dict[str, Any]) -> None:
        """注册技能模板"""
        self._dual_mgr.global_memory.add_skill_template(name, template_data)
    
    def record_trajectory(self, name: str, trajectory_data: Dict[str, Any]) -> None:
        """记录最优轨迹"""
        self._dual_mgr.global_memory.add_optimal_trajectory(name, trajectory_data)
    
    def get_trajectory(self, name: str) -> Optional[Dict[str, Any]]:
        """获取最优轨迹"""
        return self._dual_mgr.global_memory.optimal_trajectories.get(name)
    
    def sync_global(self) -> bool:
        """同步全局记忆到磁盘"""
        return self._dual_mgr.sync_global()
    
    # ─────────────────────────────────────────────────────────────
    # Mu_agent_mem Agent私有记忆操作
    # ─────────────────────────────────────────────────────────────
    
    def get_agent(self, agent_id: str) -> AgentMemory:
        """获取Agent私有记忆"""
        return self._dual_mgr.get_agent_memory(agent_id)
    
    def log_task(self, agent_id: str, task_data: Dict[str, Any]) -> None:
        """记录Agent任务"""
        agent_mem = self.get_agent(agent_id)
        agent_mem.add_task(task_data)
    
    def update_personality(self, agent_id: str, personality_updates: Dict[str, Any]) -> None:
        """更新Agent人格参数"""
        agent_mem = self.get_agent(agent_id)
        agent_mem.update_personality(personality_updates)
    
    def learn_skill(self, agent_id: str, skill_name: str) -> None:
        """标记Agent学会技能"""
        agent_mem = self.get_agent(agent_id)
        agent_mem.learn_skill(skill_name)
    
    def get_agent_skills(self, agent_id: str) -> List[str]:
        """获取Agent已学技能"""
        agent_mem = self.get_agent(agent_id)
        return list(agent_mem.learned_skills)
    
    def get_agent_history(self, agent_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取Agent最近任务历史"""
        agent_mem = self.get_agent(agent_id)
        return agent_mem.task_history[-limit:]
    
    def get_agent_personality(self, agent_id: str) -> Dict[str, Any]:
        """获取Agent人格参数"""
        agent_mem = self.get_agent(agent_id)
        return dict(agent_mem.personality)
    
    # ─────────────────────────────────────────────────────────────
    # 持久化操作
    # ─────────────────────────────────────────────────────────────
    
    def save_all(self) -> Dict[str, bool]:
        """保存所有记忆"""
        return self._dual_mgr.save_all()
    
    def save_agent(self, agent_id: str) -> bool:
        """保存指定Agent记忆"""
        agent_mem = self.get_agent(agent_id)
        return agent_mem.save(self._dual_mgr.agent_path)
    
    def list_agents(self) -> List[str]:
        """列出所有Agent"""
        return self._dual_mgr.list_agents()
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self._dual_mgr.get_stats()
    
    # ─────────────────────────────────────────────────────────────
    # 预置公式初始化（系统启动时调用）
    # ─────────────────────────────────────────────────────────────
    
    def init_core_formulas(self) -> None:
        """初始化核心公式库"""
        core_formulas = {
            "ΔG": {
                "name": "演化增益",
                "expr": "ΔG = (C×Λ×Ω)/(H×t)",
                "params": {
                    "C": {"desc": "复杂度", "range": "R+"},
                    "Λ": {"desc": "演化系数", "range": "[0,1]"},
                    "Ω": {"desc": "收敛度", "range": "[0,1]"},
                    "H": {"desc": "噪声", "range": "[0,1]"},
                    "t": {"desc": "时间", "range": "R+"}
                },
                "desc": "APEX核心演化增益公式"
            },
            "Φ_code": {
                "name": "代码质量",
                "expr": "Φ_code = (E×Ψ×Θ×Γ×Ω×α)/(R×B×C×δ×μ)",
                "params": {
                    "E": {"desc": "执行效率"},
                    "Ψ": {"desc": "逻辑连贯"},
                    "Θ": {"desc": "校验覆盖"},
                    "Γ": {"desc": "任务分解"},
                    "Ω": {"desc": "感知覆盖"},
                    "α": {"desc": "最优系数"}
                },
                "desc": "CodeGenesis代码质量综合评估"
            },
            "Ξ_evol": {
                "name": "进化系数",
                "expr": "Ξ_evol = (C×Λ×Ω)/(H×t)",
                "params": {
                    "C": {"desc": "复杂度"},
                    "Λ": {"desc": "演化系数"},
                    "Ω": {"desc": "收敛度"},
                    "H": {"desc": "噪声"},
                    "t": {"desc": "时间"}
                },
                "desc": "进化能力量化指标"
            },
            "Σ_conv": {
                "name": "收敛判定",
                "expr": "Σ_conv = |Δ_new - Δ_old| < ε",
                "params": {
                    "ε": {"desc": "收敛阈值", "default": 0.001}
                },
                "desc": "判断迭代是否收敛"
            },
            "Ω_purge": {
                "name": "去重净化",
                "expr": "Ω_purge = 1 - (S_repeat/S_total)×σ",
                "params": {
                    "S_repeat": {"desc": "重复片段数"},
                    "S_total": {"desc": "总片段数"},
                    "σ": {"desc": "合并系数"}
                },
                "desc": "代码去重净化率"
            }
        }
        
        for name, formula in core_formulas.items():
            self.register_formula(name, formula)
        
        # 保存
        self.sync_global()
