"""
GitHubAutoFetch - GitHub自动拉取模块
从GitHub自动拉取最新代码、技能和配置
"""
import os
import json
import base64
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class GitHubAutoFetch:
    """
    GitHub自动拉取器

    功能:
    1. 从指定仓库拉取文件
    2. 同步最新技能
    3. 自动更新配置
    4. 版本检查
    """

    def __init__(self, token: str = None, repo: str = None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.default_repo = repo
        self.api_base = "https://api.github.com"
        self.raw_base = "https://raw.githubusercontent.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

        self.fetch_history: List[Dict] = []
        self.last_fetch_time: Optional[datetime] = None

    def get_repo_info(self, repo: str = None) -> Dict:
        """
        获取仓库信息
        """
        repo = repo or self.default_repo
        if not repo:
            return {'error': 'No repository specified'}

        url = f"{self.api_base}/repos/{repo}"
        response = requests.get(url, headers=self.headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                'name': data.get('name'),
                'full_name': data.get('full_name'),
                'description': data.get('description'),
                'default_branch': data.get('default_branch'),
                'stars': data.get('stargazers_count'),
                'updated_at': data.get('updated_at')
            }
        return {'error': f'Request failed: {response.status_code}'}

    def get_file_content(self, path: str, repo: str = None, branch: str = "main") -> Optional[bytes]:
        """
        获取文件内容

        参数:
            path: 文件路径
            repo: 仓库名 (owner/repo)
            branch: 分支名

        返回:
            文件内容(bytes)
        """
        repo = repo or self.default_repo
        if not repo:
            return None

        url = f"{self.api_base}/repos/{repo}/contents/{path}"
        params = {'ref': branch}

        response = requests.get(url, headers=self.headers, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if data.get('encoding') == 'base64':
                content = base64.b64decode(data['content'])
                self._record_fetch(path, True)
                return content

        self._record_fetch(path, False)
        return None

    def get_file_text(self, path: str, repo: str = None, branch: str = "main", encoding: str = 'utf-8') -> Optional[str]:
        """
        获取文件文本内容
        """
        content = self.get_file_content(path, repo, branch)
        if content:
            return content.decode(encoding, errors='replace')
        return None

    def save_file(self, path: str, content: bytes, local_dir: str = ".") -> str:
        """
        保存文件到本地

        参数:
            path: 原文件路径
            content: 文件内容
            local_dir: 本地目录

        返回:
            本地文件路径
        """
        # 创建目录
        local_path = os.path.join(local_dir, path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        with open(local_path, 'wb') as f:
            f.write(content)

        return local_path

    def list_directory(self, path: str = "", repo: str = None, branch: str = "main") -> List[Dict]:
        """
        列出目录内容
        """
        repo = repo or self.default_repo
        if not repo:
            return []

        url = f"{self.api_base}/repos/{repo}/contents/{path}"
        params = {'ref': branch}

        response = requests.get(url, headers=self.headers, params=params, timeout=30)

        if response.status_code == 200:
            items = response.json()
            return [{
                'name': item.get('name'),
                'type': item.get('type'),
                'path': item.get('path'),
                'size': item.get('size', 0)
            } for item in items]
        return []

    def get_latest_commit(self, repo: str = None, branch: str = "main") -> Dict:
        """
        获取最新提交信息
        """
        repo = repo or self.default_repo
        if not repo:
            return {}

        url = f"{self.api_base}/repos/{repo}/commits/{branch}"
        response = requests.get(url, headers=self.headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                'sha': data.get('sha'),
                'message': data.get('commit', {}).get('message'),
                'author': data.get('commit', {}).get('author', {}).get('name'),
                'date': data.get('commit', {}).get('author', {}).get('date')
            }
        return {}

    def sync_directory(self, remote_path: str, local_dir: str, repo: str = None, branch: str = "main") -> Dict:
        """
        同步整个目录
        """
        files = self.list_directory(remote_path, repo, branch)
        synced = []
        failed = []

        for file_info in files:
            if file_info['type'] == 'file':
                content = self.get_file_content(file_info['path'], repo, branch)
                if content:
                    local_path = self.save_file(file_info['path'], content, local_dir)
                    synced.append(file_info['path'])
                else:
                    failed.append(file_info['path'])
            elif file_info['type'] == 'dir':
                # 递归同步子目录
                sub_result = self.sync_directory(file_info['path'], local_dir, repo, branch)
                synced.extend(sub_result['synced'])
                failed.extend(sub_result['failed'])

        return {
            'synced': synced,
            'failed': failed,
            'total': len(files)
        }

    def _record_fetch(self, path: str, success: bool):
        """记录拉取历史"""
        self.fetch_history.append({
            'path': path,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
        self.last_fetch_time = datetime.now()

        # 限制历史长度
        if len(self.fetch_history) > 100:
            self.fetch_history = self.fetch_history[-100:]

    def get_fetch_stats(self) -> Dict:
        """获取拉取统计"""
        total = len(self.fetch_history)
        success = sum(1 for h in self.fetch_history if h['success'])
        return {
            'total_fetches': total,
            'successful': success,
            'failed': total - success,
            'success_rate': round(success / total * 100, 2) if total > 0 else 0,
            'last_fetch': self.last_fetch_time.isoformat() if self.last_fetch_time else None
        }


# 便捷函数
def quick_fetch(repo: str, path: str, token: str = None) -> Optional[str]:
    """
    快速拉取文件

    示例:
        content = quick_fetch("user/repo", "README.md")
    """
    fetcher = GitHubAutoFetch(token=token, repo=repo)
    return fetcher.get_file_text(path)


if __name__ == "__main__":
    print("=== GitHub自动拉取测试 ===")

    # 示例用法
    fetcher = GitHubAutoFetch()

    if fetcher.default_repo:
        info = fetcher.get_repo_info()
        print(f"仓库信息: {info}")

        latest = fetcher.get_latest_commit()
        print(f"最新提交: {latest}")
    else:
        print("未配置默认仓库，测试跳过")
