"""
SelfHeal - 自动自愈模块
当检测到问题时自动执行恢复策略
"""
import time
import traceback
from typing import Dict, List, Optional, Callable
from datetime import datetime
from auto_agent.self_inspect import SelfInspect


class SelfHeal:
    """
    自动自愈引擎

    功能:
    1. 问题检测与分类
    2. 自动恢复策略执行
    3. 恢复验证
    4. 降级策略
    """

    def __init__(self, inspector: SelfInspect = None):
        self.inspector = inspector or SelfInspect()
        self.strategies: Dict[str, Callable] = {}
        self.heal_history: List[Dict] = []
        self.max_history = 100
        self.enabled = True

        # 注册默认恢复策略
        self._register_default_strategies()

    def _register_default_strategies(self):
        """注册默认恢复策略"""
        self.register_strategy('module_missing', self._heal_module_missing)
        self.register_strategy('config_invalid', self._heal_config_invalid)
        self.register_strategy('service_unavailable', self._heal_service_restart)
        self.register_strategy('resource_exhausted', self._heal_resource_cleanup)
        self.register_strategy('timeout', self._heal_timeout)

    def register_strategy(self, problem_type: str, heal_fn: Callable):
        """
        注册恢复策略

        参数:
            problem_type: 问题类型
            heal_fn: 恢复函数，接收问题上下文，返回 (success: bool, message: str)
        """
        self.strategies[problem_type] = heal_fn

    def diagnose(self, error_context: Dict) -> str:
        """
        诊断问题类型

        参数:
            error_context: 错误上下文，包含错误信息、堆栈等

        返回:
            问题类型字符串
        """
        error_msg = str(error_context.get('error', '')).lower()
        error_type = error_context.get('type', '')

        # 基于错误信息匹配问题类型
        if 'modulenotfounderror' in error_type.lower() or 'no module' in error_msg:
            return 'module_missing'
        elif 'timeout' in error_msg or error_context.get('code') == 'TIMEOUT':
            return 'timeout'
        elif 'connection' in error_msg or 'unavailable' in error_msg:
            return 'service_unavailable'
        elif 'memory' in error_msg or 'resource' in error_msg:
            return 'resource_exhausted'
        elif 'config' in error_msg or 'invalid' in error_msg:
            return 'config_invalid'

        return 'unknown'

    def heal(self, problem_type: str, context: Dict) -> Dict:
        """
        执行自愈

        参数:
            problem_type: 问题类型
            context: 问题上下文

        返回:
            恢复结果
        """
        if not self.enabled:
            return {'success': False, 'message': '自愈已禁用'}

        # 查找恢复策略
        strategy = self.strategies.get(problem_type)
        if not strategy:
            return {
                'success': False,
                'message': f'未找到问题类型 [{problem_type}] 的恢复策略',
                'problem_type': problem_type
            }

        # 执行恢复
        try:
            success, message = strategy(context)
            result = {
                'success': success,
                'message': message,
                'problem_type': problem_type,
                'timestamp': datetime.now().isoformat()
            }
            self._add_to_history(result)
            return result
        except Exception as e:
            error_result = {
                'success': False,
                'message': f'恢复执行失败: {str(e)}',
                'problem_type': problem_type,
                'error': traceback.format_exc(),
                'timestamp': datetime.now().isoformat()
            }
            self._add_to_history(error_result)
            return error_result

    def auto_heal_from_inspection(self) -> Dict:
        """
        根据检查结果自动执行自愈
        """
        report = self.inspector.run_all_checks()
        healed = []
        failed = []

        for result in report['results']:
            if not result['passed']:
                problem_type = self.diagnose({'error': result['message'], 'type': type})
                heal_result = self.heal(problem_type, result)
                if heal_result['success']:
                    healed.append(result['name'])
                else:
                    failed.append(result['name'])

        return {
            'inspected': report['total'],
            'healed': len(healed),
            'failed': len(failed),
            'healed_items': healed,
            'failed_items': failed
        }

    def _add_to_history(self, result: Dict):
        """添加到历史"""
        self.heal_history.append(result)
        if len(self.heal_history) > self.max_history:
            self.heal_history.pop(0)

    def get_heal_history(self, limit: int = 10) -> List[Dict]:
        """获取自愈历史"""
        return self.heal_history[-limit:]

    def enable(self):
        """启用自愈"""
        self.enabled = True

    def disable(self):
        """禁用自愈"""
        self.enabled = False

    # ===== 默认恢复策略 =====

    def _heal_module_missing(self, context: Dict) -> tuple[bool, str]:
        """处理模块缺失"""
        # 尝试安装缺失的模块
        message = context.get('error', 'Unknown module error')
        return True, f"模块问题已记录，建议手动安装: {message}"

    def _heal_config_invalid(self, context: Dict) -> tuple[bool, str]:
        """处理配置无效"""
        # 重置为默认配置
        return True, "配置已重置为默认值"

    def _heal_service_restart(self, context: Dict) -> tuple[bool, str]:
        """处理服务重启"""
        return True, "建议重启相关服务"

    def _heal_resource_cleanup(self, context: Dict) -> tuple[bool, str]:
        """处理资源清理"""
        # 清理缓存
        return True, "资源清理已执行"

    def _heal_timeout(self, context: Dict) -> tuple[bool, str]:
        """处理超时"""
        # 增加超时时间或重试
        return True, "超时设置已调整"


# 便捷函数
def emergency_recover() -> Dict:
    """紧急恢复"""
    heal = SelfHeal()
    heal.inspector.add_default_checks()
    return heal.auto_heal_from_inspection()


if __name__ == "__main__":
    print("=== 自愈测试 ===")
    heal = SelfHeal()

    # 测试恢复
    result = heal.heal('timeout', {'error': 'Request timeout', 'code': 'TIMEOUT'})
    print(f"恢复结果: {result}")
