"""
AgentHook - Auto-Agent主钩子
整合自我检查、自愈、GitHub拉取为统一接口
"""
from typing import Dict, Optional, Callable, List
from datetime import datetime
from auto_agent.self_inspect import SelfInspect
from auto_agent.self_heal import SelfHeal
from auto_agent.github_auto_fetch import GitHubAutoFetch


class AgentHook:
    """
    Auto-Agent主钩子 - 统一协调各子模块

    功能:
    1. 整合自我检查、自愈、GitHub拉取
    2. 统一的生命周期管理
    3. 事件驱动响应
    4. 状态监控
    """

    def __init__(self, github_token: str = None, github_repo: str = None):
        # 初始化子模块
        self.inspector = SelfInspect()
        self.healer = SelfHeal(self.inspector)
        self.github = GitHubAutoFetch(token=github_token, repo=github_repo)

        # 状态
        self.enabled = True
        self.auto_heal = True
        self.auto_fetch = False

        # 钩子
        self.lifecycle_hooks: Dict[str, List[Callable]] = {
            'on_start': [],
            'on_stop': [],
            'on_error': [],
            'on_heal': [],
            'on_fetch': []
        }

        # 注册默认检查
        self.inspector.add_default_checks()

    # ===== 生命周期钩子 =====

    def on_start(self, hook_fn: Callable):
        """注册启动钩子"""
        self.lifecycle_hooks['on_start'].append(hook_fn)

    def on_stop(self, hook_fn: Callable):
        """注册停止钩子"""
        self.lifecycle_hooks['on_stop'].append(hook_fn)

    def on_error(self, hook_fn: Callable):
        """注册错误钩子"""
        self.lifecycle_hooks['on_error'].append(hook_fn)

    def _trigger_hook(self, hook_type: str, data: Dict):
        """触发钩子"""
        for hook in self.lifecycle_hooks.get(hook_type, []):
            try:
                hook(data)
            except Exception as e:
                print(f"钩子执行失败 [{hook_type}]: {e}")

    # ===== 核心功能 =====

    def start(self) -> Dict:
        """
        启动Agent
        """
        # 执行启动钩子
        self._trigger_hook('on_start', {'timestamp': datetime.now().isoformat()})

        # 初始自检
        health = self.inspector.quick_health_check()

        return {
            'status': 'started',
            'health': health,
            'timestamp': datetime.now().isoformat()
        }

    def stop(self):
        """
        停止Agent
        """
        self._trigger_hook('on_stop', {'timestamp': datetime.now().isoformat()})
        return {'status': 'stopped'}

    def run_inspection(self) -> Dict:
        """
        执行完整检查
        """
        return self.inspector.run_all_checks()

    def run_healing(self, problem_type: str = None, context: Dict = None) -> Dict:
        """
        执行自愈

        参数:
            problem_type: 问题类型(可选，不指定则自动诊断)
            context: 问题上下文
        """
        context = context or {}

        # 如果没指定问题类型，从检查结果自动诊断
        if not problem_type:
            report = self.inspector.run_all_checks()
            for result in report['results']:
                if not result['passed']:
                    problem_type = self.healer.diagnose(result)
                    context.update(result)
                    break

        if problem_type:
            result = self.healer.heal(problem_type, context)
            self._trigger_hook('on_heal', result)
            return result

        return {'success': True, 'message': '无问题需要修复'}

    def auto_heal_cycle(self) -> Dict:
        """
        自动修复循环 - 检查并修复所有发现的问题
        """
        if not self.auto_heal:
            return {'message': '自动修复已禁用'}

        return self.healer.auto_heal_from_inspection()

    def fetch_from_github(self, path: str, local_dir: str = ".") -> Dict:
        """
        从GitHub拉取文件
        """
        content = self.github.get_file_content(path)
        if content:
            local_path = self.github.save_file(path, content, local_dir)
            result = {
                'success': True,
                'local_path': local_path,
                'path': path
            }
            self._trigger_hook('on_fetch', result)
            return result

        return {
            'success': False,
            'message': f'拉取失败: {path}'
        }

    def sync_skills_from_github(self, remote_path: str = "skills", local_dir: str = "skills") -> Dict:
        """
        同步技能目录
        """
        result = self.github.sync_directory(remote_path, local_dir)
        if result['synced']:
            self._trigger_hook('on_fetch', result)
        return result

    # ===== 错误处理 =====

    def handle_error(self, error: Exception, context: Dict = None) -> Dict:
        """
        处理错误

        参数:
            error: 异常对象
            context: 错误上下文

        返回:
            处理结果
        """
        error_context = {
            'error': str(error),
            'type': type(error).__name__,
            'context': context or {},
            'timestamp': datetime.now().isoformat()
        }

        self._trigger_hook('on_error', error_context)

        # 尝试自动修复
        if self.auto_heal:
            heal_result = self.run_healing(context=error_context)
            error_context['heal_result'] = heal_result

        return error_context

    # ===== 状态获取 =====

    def get_status(self) -> Dict:
        """
        获取Agent状态
        """
        health = self.inspector.quick_health_check()

        return {
            'enabled': self.enabled,
            'auto_heal': self.auto_heal,
            'auto_fetch': self.auto_fetch,
            'health': health,
            'heal_history': self.healer.get_heal_history(limit=5),
            'fetch_stats': self.github.get_fetch_stats(),
            'system_info': self.inspector.get_system_info(),
            'timestamp': datetime.now().isoformat()
        }

    def enable(self):
        """启用Agent"""
        self.enabled = True

    def disable(self):
        """禁用Agent"""
        self.enabled = False

    def enable_auto_heal(self):
        """启用自动修复"""
        self.auto_heal = True

    def disable_auto_heal(self):
        """禁用自动修复"""
        self.auto_heal = False


# 便捷函数
def create_agent(github_token: str = None, github_repo: str = None) -> AgentHook:
    """创建Agent实例"""
    return AgentHook(github_token=github_token, github_repo=github_repo)


if __name__ == "__main__":
    print("=== AgentHook 启动测试 ===")

    agent = create_agent()

    # 启动
    result = agent.start()
    print(f"启动结果: {result}")

    # 状态
    status = agent.get_status()
    print(f"\n状态:")
    print(f"  健康: {status['health']}")
    print(f"  系统: {status['system_info']['python_version']}")
