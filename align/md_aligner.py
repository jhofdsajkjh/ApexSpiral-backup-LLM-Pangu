"""
MD对齐器 - Markdown格式规范化
"""
import re


class MDAligner:
    """Markdown格式对齐器"""

    def __init__(self):
        self.max_heading_level = 6
        self.allowed_code_langs = ['python', 'javascript', 'java', 'c', 'cpp', 'go', 'rust', 'bash', 'sql']

    def align(self, text: str) -> str:
        """
        对齐Markdown格式
        """
        # 规范化标题层级
        text = self._normalize_headings(text)

        # 规范化代码块
        text = self._normalize_code_blocks(text)

        # 规范化链接
        text = self._normalize_links(text)

        # 移除危险的HTML
        text = self._sanitize_html(text)

        return text

    def _normalize_headings(self, text: str) -> str:
        """
        规范化标题层级
        """
        lines = text.split('\n')
        result = []
        for line in lines:
            if line.startswith('#'):
                # 计算标题级别
                level = len(line) - len(line.lstrip('#'))
                if level > self.max_heading_level:
                    level = self.max_heading_level
                    line = '#' * level + line.lstrip('#')
                result.append(line)
            else:
                result.append(line)
        return '\n'.join(result)

    def _normalize_code_blocks(self, text: str) -> str:
        """
        规范化代码块
        """
        # 确保代码块有语言标识
        pattern = r'```(\w*)'
        matches = re.finditer(pattern, text)
        for match in matches:
            lang = match.group(1)
            if not lang or lang not in self.allowed_code_langs:
                text = text.replace(f'```{lang}', '```')
        return text

    def _normalize_links(self, text: str) -> str:
        """
        规范化链接格式
        """
        # 确保链接格式正确
        pattern = r'\[([^\]]+)\]\(([^\)]*)\)'
        def fix_link(m):
            text_link = m.group(1)
            url = m.group(2)
            if not url:
                return text_link
            return m.group(0)
        return re.sub(pattern, fix_link, text)

    def _sanitize_html(self, text: str) -> str:
        """
        移除危险HTML标签
        """
        dangerous = ['<script>', '</script>', '<iframe>', '</iframe>',
                     '<?php', '?>', '<%', '%>']
        for tag in dangerous:
            text = text.replace(tag, '')
        return text

    def extract_code_blocks(self, text: str) -> list[tuple[str, str]]:
        """
        提取代码块
        返回: [(语言, 代码内容), ...]
        """
        pattern = r'```(\w*)\n(.*?)```'
        matches = re.finditer(pattern, text, re.DOTALL)
        return [(m.group(1), m.group(2)) for m in matches]

    def count_tokens_estimate(self, text: str) -> int:
        """
        简单Token估算 (中文约2字符/token, 英文约4字符/token)
        """
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        other_chars = len(text) - chinese_chars
        return int(chinese_chars / 2 + other_chars / 4)
