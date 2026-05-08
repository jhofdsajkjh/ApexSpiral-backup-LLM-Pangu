# 贡献指南

感谢您对 LLM-ΔG-AntiHallucination 的关注！

## 如何贡献

### 报告问题

- 使用 GitHub Issues 报告 Bug
- 描述问题详情和复现步骤
- 提供相关日志和截图

### 提交代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- 使用 Python 3.8+
- 遵循 PEP 8
- 所有新功能必须有测试
- 更新相关文档

### 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_delta_g.py -v

# 生成覆盖率报告
pytest tests/ --cov=. --cov-report=html
```

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/ApexSpiral/LLM-ΔG-AntiHallucination.git
cd LLM-ΔG-AntiHallucination

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行初始化
python run_init.py

# 运行测试
pytest tests/ -v
```

## 提交规范

### Commit 消息格式

```
<type>: <subject>

<body>
```

### Type 类型

- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

### 示例

```
feat: 添加新的自愈策略

- 实现超时自动恢复
- 添加内存清理机制
- 更新测试用例

Closes #123
```

## 问题解答

如有问题，请提交 Issue 或联系维护者。
