# 🚀 DeepSeek API 配置指南

本项目已从 Anthropic Claude API 迁移到 **DeepSeek API**。DeepSeek API 兼容 OpenAI 格式，提供高性价比的大模型服务。

---

## 📝 获取 DeepSeek API Key

### 1. 注册账号
访问 [DeepSeek 开放平台](https://platform.deepseek.com/)

### 2. 创建 API Key
1. 登录后进入 **API Keys** 页面
2. 点击 **Create API Key**
3. 复制生成的 API Key（格式：`sk-xxxxxxxxxxxxxxxx`）

### 3. 充值（可选）
- DeepSeek 提供新用户免费额度
- 如需更多配额，可在平台充值

---

## ⚙️ 配置 API Key

### 方式 1：环境变量（推荐）

**Windows CMD:**
```cmd
set DEEPSEEK_API_KEY=sk-your-api-key-here
```

**Windows PowerShell:**
```powershell
$env:DEEPSEEK_API_KEY="sk-your-api-key-here"
```

**Mac/Linux:**
```bash
export DEEPSEEK_API_KEY='sk-your-api-key-here'
```

### 方式 2：在应用内设置
1. 启动应用：`streamlit run app.py`
2. 在侧边栏找到 **⚙️ API Settings**
3. 输入你的 DeepSeek API Key
4. 点击外部区域保存

### 方式 3：使用 .env 文件
```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件
# DEEPSEEK_API_KEY=sk-your-api-key-here
```

---

## 🔧 技术细节

### API 端点
```
https://api.deepseek.com
```

### 模型名称
```
deepseek-chat
```

### 兼容性
- 使用 OpenAI SDK (`openai>=1.0.0`)
- 支持 Function Calling（工具调用）
- 完全兼容本项目的所有功能

### 代码示例
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-key-here",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```

---

## ✅ 验证配置

### 方法 1：运行测试脚本
```bash
cd E:\MyGitcode\SmartAgent
python agent_core.py
```

如果配置正确，会看到：
```
╔══════════════════════════════════════════════════════════╗
║     Dubai Mall Interactive Concierge Agent - Test        ║
║              Powered by DeepSeek API                     ║
╚══════════════════════════════════════════════════════════╝

💬 开始对话（输入 'quit' 退出）
```

### 方法 2：运行 Web 应用
```bash
streamlit run app.py
```

访问 http://localhost:8501，在聊天框输入：
```
Where is Hermès?
```

如果看到 Agent 调用工具并返回结果，说明配置成功！

---

## 🆚 与 Claude API 的主要区别

| 特性 | Claude API | DeepSeek API |
|------|-----------|--------------|
| SDK | anthropic | openai |
| Base URL | https://api.anthropic.com | https://api.deepseek.com |
| 模型名称 | claude-3-5-sonnet-20241022 | deepseek-chat |
| 工具调用格式 | Anthropic format | OpenAI function calling |
| 消息格式 | `role: assistant` + `content` | `role: assistant` + `content` |
| 环境变量 | ANTHROPIC_API_KEY | DEEPSEEK_API_KEY |

---

## 💰 价格对比（仅供参考）

**DeepSeek API 通常更具性价比：**
- 输入：~¥0.001 / 1K tokens
- 输出：~¥0.002 / 1K tokens

*具体价格请查看 [DeepSeek 定价页面](https://platform.deepseek.com/)*

---

## ❓ 常见问题

### Q1: 为什么改用 DeepSeek API？
A: DeepSeek API 提供高性价比的服务，同时兼容 OpenAI 格式，易于集成。

### Q2: 原有的 Anthropic API Key 还能用吗？
A: 不能。本项目已完全迁移到 DeepSeek API，需要使用 DeepSeek 的 API Key。

### Q3: 如何切换回 Claude API？
A: 可以查看 Git 历史记录，恢复到迁移前的版本。

### Q4: DeepSeek 支持哪些功能？
A: 支持本项目的所有功能，包括：
- 多轮对话
- Function Calling（工具调用）
- 流式输出（可选）
- 系统提示词

### Q5: API 调用失败怎么办？
A: 检查以下几点：
1. API Key 是否正确设置
2. 账户余额是否充足
3. 网络连接是否正常
4. 查看终端的错误日志

---

## 🔗 相关链接

- [DeepSeek 官网](https://www.deepseek.com/)
- [DeepSeek 开放平台](https://platform.deepseek.com/)
- [API 文档](https://platform.deepseek.com/docs)
- [OpenAI SDK 文档](https://github.com/openai/openai-python)

---

## 📞 技术支持

如遇到问题，请：
1. 查看终端错误日志
2. 确认 API Key 配置正确
3. 检查 DeepSeek 平台账户状态
4. 提交 Issue 到项目仓库

---

**🎉 祝你使用愉快！**
