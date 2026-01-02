# 🚀 快速启动指南

## 3 步开始你的 Demo

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 2️⃣ 设置 API Key

前往 [DeepSeek Platform](https://platform.deepseek.com/) 获取 API Key，然后：

**Windows:**
```cmd
set DEEPSEEK_API_KEY=sk-xxxxx
```

**Mac/Linux:**
```bash
export DEEPSEEK_API_KEY='sk-xxxxx'
```

💡 详细配置说明请查看 [DEEPSEEK_SETUP.md](DEEPSEEK_SETUP.md)

### 3️⃣ 运行 Demo

**方式 1: 使用启动脚本（推荐）**

Windows:
```cmd
run_demo.bat
```

Mac/Linux:
```bash
./run_demo.sh
```

**方式 2: 直接运行**
```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501` 🎉

---

## 🎮 快速测试对话

启动后，尝试以下对话：

### 示例 1: 查询店铺
```
Where is Hermès?
```
✅ **期望:** Agent 调用 `get_shop_info` 工具，返回楼层和位置

---

### 示例 2: 查找停车位
```
Where is my car? DXB-1234
```
✅ **期望:** Agent 调用 `find_parking` 工具，显示停车位 `B2-A05`

---

### 示例 3: 触发游戏化
```
I'm bored!
```
✅ **期望:** Agent 主动提出寻宝游戏或知识问答，承诺积分奖励

---

### 示例 4: 完成任务赚积分
```
👤 You: I'm bored
🤖 Concierge: [提出寻宝任务...]

👤 You: I found it! It's near the fountain!
🤖 Concierge: [调用 add_points，奖励 30 分]
```
✅ **期望:** 侧边栏积分从 0 → 30（实时更新）

---

### 示例 5: 兑换优惠券
```
I want to redeem a coffee voucher
```
✅ **期望:**
- Agent 调用 `redeem_coupon`
- 扣除 30 积分
- 返回优惠券代码（如 `A7B9C2D1`）
- 侧边栏显示新优惠券

---

## 📊 实时观察侧边栏

在对话过程中，观察右侧边栏的变化：

- **🏆 Loyalty Points** - 完成任务后即时增加
- **🎫 My Coupons** - 兑换后立即显示
- **🚗 Parking Status** - 查询后显示车位信息

---

## 🔧 故障排查

### ❌ "未找到 API Key"
**解决:** 在侧边栏 "⚙️ API Settings" 中输入你的 Anthropic API Key

### ❌ "ModuleNotFoundError"
**解决:**
```bash
pip install -r requirements.txt
```

### ❌ "端口已被占用"
**解决:**
```bash
streamlit run app.py --server.port 8502
```

---

## 🎯 进阶玩法

### 测试命令行模式
```bash
python agent_core.py
```

**特殊命令:**
- `status` - 查看当前积分和优惠券
- `reset` - 重置用户状态
- `quit` - 退出

### 测试模拟数据
```bash
python mock_data.py
```

查看所有工具函数的调用示例和 DEBUG 输出

---

## 📝 自定义 Demo

### 修改店铺数据
编辑 `mock_data.py` 中的 `SHOPS` 字典

### 调整积分规则
编辑 `agent_core.py` 中的 `SYSTEM_PROMPT`

### 更改 UI 主题
编辑 `app.py` 中的 CSS 样式（渐变色、字体等）

---

## 🌟 Demo 演示技巧

**推荐演示流程（5 分钟）：**

1. **开场** (30s) - 展示欢迎界面和侧边栏
2. **查询功能** (1min) - 查找店铺 + 停车位
3. **游戏化互动** (2min) - 触发寻宝游戏，完成任务赚积分
4. **实时反馈** (1min) - 观察侧边栏积分增加
5. **优惠券兑换** (30s) - 使用积分兑换优惠券
6. **多语言展示** (可选) - 用阿拉伯语或英语对话

**演示话术示例：**
> "这是一个基于 Claude 3.5 Sonnet 的商场智能管家。它不仅能回答问题，还能主动引导用户参与游戏化互动。看，当我说 'I'm bored' 时，它会立即提出寻宝任务并承诺积分奖励。完成任务后，积分会实时显示在侧边栏，用户可以随时兑换优惠券。这展示了 AI Agent 的工具调用、多轮对话和状态管理能力。"

---

**🎉 准备好了吗？运行 `streamlit run app.py` 开始体验！**
