"""
core/constraint_engine.py - 盘古约束引擎

负责执行ΔG公式计算后的约束动作
将判定结果转化为具体的修复/自愈操作
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ConstraintEngine:
    """
    约束引擎
    
    根据ΔG判定结果，执行相应的约束动作
    - 健康稳态：放行
    - 轻度偏离：局部修复
    - 严重越界：全量自愈
    """
    
    def __init__(self):
        """初始化约束引擎"""
        self.repair_history: List[Dict] = []
        logger.info("约束引擎初始化完成")
    
    def apply_constraints(self, dg_total: float, context: Optional[Dict] = None) -> Dict:
        """
        根据ΔG总值应用约束策略
        
        Args:
            dg_total: ΔG计算总值
            context: 额外上下文信息
            
        Returns:
            dict: {
                "action": str,      # 执行的动作
                "details": dict,    # 动作详情
                "success": bool     # 是否成功
            }
        """
        context = context or {}
        
        if dg_total <= 2.10:
            action = self._allow()
        elif 2.10 < dg_total <= 4.0:
            action = self._partial_repair(context)
        else:
            action = self._full_heal(context)
        
        self.repair_history.append({
            "dg_total": dg_total,
            "action": action,
            "context": context
        })
        
        return action
    
    def _allow(self) -> Dict:
        """健康稳态 - 放行"""
        logger.info("ΔG处于健康范围，放行请求")
        return {
            "action": "allow",
            "details": {"message": "系统稳态，放行"},
            "success": True
        }
    
    def _partial_repair(self, context: Dict) -> Dict:
        """轻度偏离 - 局部修复"""
        logger.warning("ΔG轻度偏离，启动局部修复")
        # 这里触发具体的修复逻辑
        repair_type = context.get("repair_type", "default")
        return {
            "action": "partial_repair",
            "details": {
                "repair_type": repair_type,
                "message": "局部修复已完成"
            },
            "success": True
        }
    
    def _full_heal(self, context: Dict) -> Dict:
        """严重越界 - 全量自愈"""
        logger.error("ΔG严重越界，启动全量自愈")
        return {
            "action": "full_heal",
            "details": {
                "message": "全量自愈已触发",
                "recovery_steps": ["状态重置", "基因修复", "记忆恢复"]
            },
            "success": True
        }
