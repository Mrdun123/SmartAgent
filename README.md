# 🛍️ Dubai Mall Intelligent Concierge

一个基于 **DeepSeek API** 的互动服务 Agent Demo，展示 AI 在商场场景中的游戏化应用。

## ✨ 功能特性

### 🎯 核心功能
- **🚗 智能停车查询** - 输入车牌号即可查找停车位
- **🏪 店铺导航** - 查询品牌位置、楼层和详细介绍
- **🎮 游戏化互动** - 4 种互动玩法（寻宝、打卡、问答、侦探）
- **🏆 积分系统** - 完成任务赢取积分
- **🎫 优惠券兑换** - 使用积分兑换咖啡券、折扣券等

### 🌍 智能特性
- **多语言支持** - 自动检测阿拉伯语/英语
- **文化适配** - 使用 "Marhaba"、"Habibi" 等本地化词汇
- **实时反馈** - 积分和优惠券状态实时更新
- **沉浸式体验** - 奢华、专业的对话风格

## 📁 项目结构

```
SmartAgent/
├── app.py              # Streamlit Web 前端
├── agent_core.py       # Claude Agent 核心交互逻辑
├── mock_data.py        # 模拟数据库和工具函数
├── requirements.txt    # Python 依赖包
└── README.md           # 项目说明文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置 API Key

获取你的 [DeepSeek API Key](https://platform.deepseek.com/)，然后设置环境变量：

**Windows (CMD):**
```cmd
set DEEPSEEK_API_KEY=sk-xxxxx
```

**Windows (PowerShell):**
```powershell
$env:DEEPSEEK_API_KEY="sk-xxxxx"
```

**Mac/Linux:**
```bash
export DEEPSEEK_API_KEY='sk-xxxxx'
```

或者在应用内通过侧边栏设置。更多配置方式请查看 [DEEPSEEK_SETUP.md](DEEPSEEK_SETUP.md)。

### 3. 运行 Demo

**启动 Web 应用：**
```bash
streamlit run app.py
```

**或直接测试 Agent 核心：**
```bash
python agent_core.py
```

浏览器会自动打开 `http://localhost:8501`

## 🎮 使用指南

### 快速示例对话

#### 📍 查询店铺位置
```
👤 You: Where is Hermès?
🤖 Concierge: Marhaba! Hermès is located on the Ground Floor, Zone A,
              near Main Entrance. 法国顶级奢侈品牌，提供手袋、丝巾、配饰等经典产品。
```

#### 🚗 查找停车位
```
👤 You: Where is my car? DXB-1234
🤖 Concierge: I've located your vehicle right away! 🚗 Your car DXB-1234
              is parked at B2-A05. That's in the B2 level, Section A.
```

#### 🎯 触发游戏化
```
👤 You: I'm bored
🤖 Concierge: I have the perfect solution, habibi! 🎯 How about a quick
              Dubai Mall treasure hunt? Find the % Arabica café on the
              2nd floor and tell me what you can see from their window.
              Complete this and I'll add 25 points to your account! ✨
```

#### 🏆 赚取积分
```
👤 You: I found it! I can see the Burj Khalifa!
🤖 Concierge: Excellent work! 🎉 *Awards 25 points*
              Your current balance: 25 points
```

#### 🎫 兑换优惠券
```
👤 You: I want to redeem a coffee voucher
🤖 Concierge: Wonderful choice! *Deducts 30 points*
              Your coffee voucher code is: A7B9C2D1
              Remaining points: 20
```

### 🎮 4 种游戏化玩法

1. **Hidden Treasure Hunt** (寻宝游戏)
   - 奖励：20-50 积分
   - 示例："找到金色骆驼雕塑并告诉我它在穿什么"

2. **Shop Check-In Challenge** (店铺打卡)
   - 奖励：15-30 积分
   - 示例："访问 3 个奢侈品店并分享你最喜欢的橱窗"

3. **Dubai Mall Trivia** (知识问答)
   - 奖励：10-25 积分
   - 示例："Dubai Aquarium 里住着什么海洋生物？"

4. **Luxury Detective** (奢侈品侦探)
   - 奖励：40+ 积分
   - 示例："找到一家出售蓝色法国奢侈品的店铺"

### 🎯 积分兑换指南

| 优惠券类型 | 所需积分 |
|-----------|---------|
| 咖啡券 | 30 分 |
| 餐饮券 | 40 分 |
| 10% 购物折扣券 | 50 分 |
| VIP 休息室访问 | 100 分 |

## 🧪 测试功能

### 测试模拟数据
```bash
python mock_data.py
```

### 测试 Agent 核心（命令行模式）
```bash
python agent_core.py
```

**特殊命令：**
- `quit` - 退出对话
- `reset` - 重置用户状态和对话历史
- `status` - 查看当前积分和优惠券

## 📊 侧边栏功能

Web 应用的侧边栏实时显示：

- **🏆 Loyalty Points** - 当前积分余额（大字体展示）
- **🎫 My Coupons** - 已兑换的优惠券列表（带代码）
- **🚗 Parking Status** - 停车位信息（查询后显示）
- **🔄 Reset Demo** - 一键重置所有状态

## 🛠️ 技术栈

- **AI Framework:** DeepSeek API (via OpenAI SDK)
- **Model:** deepseek-chat
- **Web Framework:** Streamlit
- **Language:** Python 3.8+
- **Architecture:** Tool-calling Agent with multi-turn conversation

## 📝 开发说明

### 添加新店铺
编辑 `mock_data.py` 中的 `SHOPS` 字典：

```python
SHOPS = {
    "New Store": {
        "name": "New Store",
        "floor": "1st Floor",
        "category": "Fashion",
        "description": "店铺描述",
        "location": "1st Floor, Zone X"
    }
}
```

### 添加新工具
1. 在 `mock_data.py` 中定义函数
2. 添加到 `TOOL_DEFINITIONS`
3. 在 `agent_core.py` 的 `TOOL_FUNCTION_MAP` 中注册

### 自定义 System Prompt
编辑 `agent_core.py` 中的 `SYSTEM_PROMPT` 变量以调整：
- Agent 性格
- 游戏化规则
- 语言风格
- 积分奖励机制

## 🎨 界面特性

- **现代化设计** - 渐变色、圆角、阴影动画
- **响应式布局** - 自适应桌面和移动设备
- **实时更新** - 工具调用后自动刷新侧边栏
- **聊天气泡** - ChatGPT 风格的对话界面
- **迪拜主题** - 紫罗兰渐变配色（奢华感）

## 🌟 Demo 亮点

1. **完整的工具调用流程** - 展示 Claude Tool Use 能力
2. **多轮对话管理** - 保持上下文连贯性
3. **实时状态同步** - Session State 管理
4. **调试友好** - 清晰的 DEBUG 日志输出
5. **生产级架构** - 可扩展的模块化设计

## 📞 联系方式

如有问题或建议，欢迎提出 Issue！

---

**🤖 Powered by DeepSeek API | 🏢 Dubai Mall Experience Demo**
