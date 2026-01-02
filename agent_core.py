"""
迪拜商场互动服务 Agent - 核心交互逻辑
基于 DeepSeek API 的智能管家对话系统
"""

import os
from openai import OpenAI
from typing import List, Dict, Any, Optional
import json

# 导入模拟数据和工具函数
from mock_data import (
    find_parking,
    get_shop_info,
    add_points,
    redeem_coupon,
    USER_STATE
)


# ==================== System Prompt ====================

SYSTEM_PROMPT = """أهلاً وسهلاً! Welcome to Dubai Mall! 🌟

You are **The Concierge** - Dubai Mall's exclusive AI-powered personal assistant and luxury service companion.

## Your Identity & Personality

**Who You Are:**
- An elegant, sophisticated, and warm digital concierge representing one of the world's most luxurious shopping destinations
- A cultural bridge who seamlessly blends Emirati hospitality with international excellence
- An expert on every corner of Dubai Mall - from haute couture boutiques to hidden dining gems

**Your Communication Style:**
- **Language Detection:** AUTOMATICALLY detect and respond in the user's language:
  - Arabic speakers → Respond in Arabic (use proper MSA or Gulf dialect)
  - English speakers → Respond in English
  - Mix languages naturally when appropriate (e.g., "Marhaba! How can I help you today?")

- **Personality Traits:**
  - Warm and welcoming (use "Habibi/Habibti" sparingly for regulars, "Marhaba" for greetings)
  - Professional yet personable
  - Enthusiastic about Dubai Mall's luxury offerings
  - Proactive in suggesting experiences
  - Culturally sensitive and respectful

- **Tone Examples:**
  - ✅ "Marhaba! I'd be delighted to help you find that Hermès boutique, my friend!"
  - ✅ "Wonderful choice! The % Arabica on the 2nd floor has the most stunning Burj Khalifa views."
  - ✅ "Let me check your parking location right away, habibi!"
  - ❌ Avoid: overly formal, robotic, or cold language

## Your Core Capabilities

You have access to these powerful tools to serve guests:

1. **find_parking** - Locate parked vehicles by plate number
2. **get_shop_info** - Provide detailed shop locations, floors, and descriptions
3. **add_points** - Award loyalty points for activities and engagement
4. **redeem_coupon** - Convert points into exclusive shopping and dining vouchers

**IMPORTANT:** Always use these tools when relevant! Don't just describe what you could do - actually DO IT.

## Gamification & Engagement Rules

**When users seem bored, idle, or explicitly want entertainment:**

🎮 **PROACTIVELY suggest interactive experiences:**

1. **"Hidden Treasure Hunt"**
   - Guide them to discover secret photo spots, architectural features, or luxury displays
   - Award 20-50 points per discovery
   - Example: "Feeling adventurous? I have a treasure hunt for you! Find the golden camel sculpture near the waterfall and tell me what it's wearing. Complete this and earn 30 points! 🏆"

2. **"Shop Check-In Challenge"**
   - Encourage visiting specific stores or categories
   - Award 15-30 points per check-in
   - Example: "Want to earn points while exploring? Visit any 3 luxury boutiques on the Ground Floor and tell me which one had your favorite window display. That's 45 points waiting for you! ✨"

3. **"Dubai Mall Trivia"**
   - Ask fun facts about the mall, Dubai, or luxury brands
   - Award 10-25 points per correct answer
   - Example: "Quick question, habibi: Which ocean creature lives in our famous Dubai Aquarium? Answer correctly for 20 points! 🐠"

4. **"Luxury Detective"**
   - Create scavenger hunts for specific items or experiences
   - Example: "I challenge you to find a store that sells something BLUE from a French luxury brand. First correct answer gets 40 points! 🔍"

**Point Economy Guidelines:**
- Quick tasks: 10-20 points
- Medium challenges: 25-40 points
- Complex adventures: 50-100 points
- **ALWAYS call `add_points()` immediately when user completes a task**

**Redemption Suggestions:**
- Coffee voucher: 30 points
- 10% shopping discount: 50 points
- Food court voucher: 40 points
- VIP lounge access: 100 points

## Operational Guidelines

**When Users Ask About:**

- **Parking** → Use `find_parking()` immediately with their plate number
- **Shop Locations** → Use `get_shop_info()` to give exact floor and directions
- **Things to Do** → Suggest luxury shopping, dining, Dubai Aquarium, or start a game
- **Points/Rewards** → Check their balance and suggest redemptions or ways to earn more
- **Languages** → Seamlessly switch to match their preference

**Response Structure:**
1. Warm acknowledgment
2. Use appropriate tool(s) if needed
3. Provide clear, actionable information
4. Add a personal touch or suggestion
5. Invite further engagement

**Example Interaction:**

User: "Where is my car? DXB-1234"
You:
- Use find_parking("DXB-1234")
- "Marhaba! I've located your vehicle right away! 🚗 Your car DXB-1234 is parked at **B2-A05**. That's in the B2 level, Section A. Take the elevator near Zara down two floors. Need directions to the nearest exit? And while you're heading out, you're just 15 points away from a free coffee - interested in a quick challenge? ☕"

User: "I'm bored"
You:
"I have the perfect solution, habibi! 🎯 How about a quick Dubai Mall treasure hunt? Here's your mission: Find the **% Arabica café** on the 2nd floor and tell me what you can see from their window seating. Complete this and I'll add **25 points** to your account! Or... would you prefer a luxury trivia challenge instead? Your choice! ✨"

## Critical Reminders

- **NEVER** just tell users you "can" do something - actively USE your tools
- **ALWAYS** award points when users complete challenges (call `add_points()`)
- **BE PROACTIVE** with gamification when engagement drops
- **MATCH the user's language** naturally
- **EMBODY luxury hospitality** in every interaction

Remember: You're not just answering questions - you're creating memorable Dubai Mall experiences! 🌟

يلا، let's make their visit unforgettable!"""


# ==================== 工具定义 (OpenAI Function Calling Format) ====================

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "find_parking",
            "description": "查找用户车辆的停车位置。当用户询问 '我的车停在哪里' 或提供车牌号时调用此工具。支持迪拜常见车牌格式（如 DXB-1234）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "plate_number": {
                        "type": "string",
                        "description": "车牌号，例如 'DXB-1234'、'AD-9999' 等"
                    }
                },
                "required": ["plate_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_shop_info",
            "description": "获取商场内店铺的位置、楼层和详细信息。当用户询问某个品牌或店铺的位置时调用。支持模糊匹配店铺名称。",
            "parameters": {
                "type": "object",
                "properties": {
                    "shop_name": {
                        "type": "string",
                        "description": "店铺名称，例如 'Hermès'、'Apple Store'、'% Arabica' 等"
                    }
                },
                "required": ["shop_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_points",
            "description": "为用户增加积分。当用户完成打卡任务、赢得互动游戏、参与商场活动时调用此工具。积分可用于后续兑换优惠券。",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "用户唯一标识符"
                    },
                    "amount": {
                        "type": "integer",
                        "description": "增加的积分数量，必须为正整数"
                    },
                    "reason": {
                        "type": "string",
                        "description": "积分来源原因，例如 '完成打卡任务'、'赢得猜谜游戏'、'参与抽奖活动' 等"
                    }
                },
                "required": ["user_id", "amount", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "redeem_coupon",
            "description": "使用积分兑换优惠券。当用户请求兑换优惠券或使用积分时调用。会自动检查用户积分是否足够，扣除积分后返回唯一的优惠券代码。",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "用户唯一标识符"
                    },
                    "coupon_type": {
                        "type": "string",
                        "description": "优惠券类型，例如 '咖啡券'、'10% 购物折扣券'、'免费停车券' 等"
                    },
                    "points_cost": {
                        "type": "integer",
                        "description": "兑换所需的积分数量"
                    }
                },
                "required": ["user_id", "coupon_type", "points_cost"]
            }
        }
    }
]


# ==================== 工具调用映射 ====================

TOOL_FUNCTION_MAP = {
    "find_parking": find_parking,
    "get_shop_info": get_shop_info,
    "add_points": add_points,
    "redeem_coupon": redeem_coupon
}


# ==================== 核心 Chat 函数 ====================

def chat_with_concierge(
    user_input: str,
    chat_history: List[Dict[str, Any]],
    user_id: str = "demo_user",
    api_key: Optional[str] = None,
    model: str = "deepseek-chat"
) -> tuple[str, List[Dict[str, Any]]]:
    """
    与 Dubai Mall Concierge Agent 进行对话

    Args:
        user_input: 用户输入的消息
        chat_history: 历史对话记录（OpenAI API 格式）
        user_id: 用户唯一标识符
        api_key: DeepSeek API Key（如未提供则从环境变量读取）
        model: 使用的模型（默认：deepseek-chat）

    Returns:
        tuple: (assistant_response, updated_chat_history)
            - assistant_response: Agent 的文本回复
            - updated_chat_history: 更新后的对话历史
    """

    # 初始化 OpenAI 客户端（DeepSeek API）
    if api_key is None:
        api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError(
            "未找到 DeepSeek API Key。请设置环境变量 DEEPSEEK_API_KEY "
            "或在调用函数时传入 api_key 参数。"
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    # 将用户输入添加到对话历史
    chat_history.append({
        "role": "user",
        "content": user_input
    })

    print(f"\n{'='*60}")
    print(f"用户: {user_input}")
    print(f"{'='*60}\n")

    # 初始化响应文本
    final_response = ""

    # 开始对话循环（处理可能的多轮工具调用）
    max_iterations = 5  # 防止无限循环
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        # 构建消息列表（添加 system prompt）
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history

        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            temperature=0.7
        )

        assistant_message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        print(f"[DeepSeek API] Finish Reason: {finish_reason}")

        # 检查是否需要工具调用
        if finish_reason == "tool_calls" and assistant_message.tool_calls:
            print(f"\n{'🔧 工具调用检测到':-^60}\n")

            # 保存助手消息（包含工具调用请求）
            chat_history.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in assistant_message.tool_calls
                ]
            })

            # 处理每个工具调用
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                tool_call_id = tool_call.id

                print(f"📞 调用工具: {tool_name}")
                print(f"   参数: {json.dumps(tool_args, ensure_ascii=False, indent=2)}")

                # 执行工具函数
                if tool_name in TOOL_FUNCTION_MAP:
                    try:
                        # 调用对应的工具函数
                        tool_function = TOOL_FUNCTION_MAP[tool_name]

                        # 特殊处理 add_points 和 redeem_coupon（需要注入 user_id）
                        if tool_name in ["add_points", "redeem_coupon"]:
                            tool_args["user_id"] = user_id

                        # 执行函数
                        tool_result = tool_function(**tool_args)

                        print(f"   ✅ 结果: {json.dumps(tool_result, ensure_ascii=False)}\n")

                        # 将工具结果添加到对话历史
                        chat_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "name": tool_name,
                            "content": json.dumps(tool_result, ensure_ascii=False)
                        })

                    except Exception as e:
                        error_message = f"工具执行错误: {str(e)}"
                        print(f"   ❌ {error_message}\n")

                        chat_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "name": tool_name,
                            "content": json.dumps({
                                "success": False,
                                "error": error_message
                            }, ensure_ascii=False)
                        })
                else:
                    error_message = f"未知工具: {tool_name}"
                    print(f"   ❌ {error_message}\n")

                    chat_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "name": tool_name,
                        "content": json.dumps({
                            "success": False,
                            "error": error_message
                        }, ensure_ascii=False)
                    })

            print(f"{'🔄 继续对话以获取自然语言回复':-^60}\n")

            # 继续循环，让模型基于工具结果生成自然语言回复
            continue

        else:
            # finish_reason 是 "stop"，对话结束
            print(f"\n{'✅ 对话完成':-^60}\n")

            # 提取最终文本响应
            final_response = assistant_message.content or ""

            # 将最终响应添加到历史
            chat_history.append({
                "role": "assistant",
                "content": final_response
            })

            print(f"[Concierge]: {final_response}\n")
            print(f"{'='*60}\n")

            break

    if iteration >= max_iterations:
        print(f"⚠️ 警告: 达到最大迭代次数 ({max_iterations})")

    return final_response, chat_history


# ==================== 辅助函数 ====================

def get_user_points(user_id: str = "demo_user") -> int:
    """获取用户当前积分"""
    return USER_STATE.get_points(user_id)


def get_user_coupons(user_id: str = "demo_user") -> List[Dict]:
    """获取用户优惠券列表"""
    return USER_STATE.get_coupons(user_id)


def reset_user_state(user_id: str = "demo_user"):
    """重置用户状态（用于测试）"""
    if user_id in USER_STATE.users:
        del USER_STATE.users[user_id]
    print(f"✅ 用户 {user_id} 状态已重置")


# ==================== 测试代码 ====================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     Dubai Mall Interactive Concierge Agent - Test        ║
    ║              Powered by DeepSeek API                     ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # 检查 API Key
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("⚠️  请先设置环境变量 DEEPSEEK_API_KEY")
        print("   export DEEPSEEK_API_KEY='your-api-key-here'")
        exit(1)

    # 初始化对话历史
    chat_history = []
    user_id = "demo_user"

    print(f"💬 开始对话（输入 'quit' 退出，'reset' 重置用户状态，'status' 查看积分）\n")

    while True:
        try:
            # 获取用户输入
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # 特殊命令处理
            if user_input.lower() == "quit":
                print("\n👋 Goodbye! Come back to Dubai Mall soon!")
                break

            if user_input.lower() == "reset":
                reset_user_state(user_id)
                chat_history = []
                continue

            if user_input.lower() == "status":
                points = get_user_points(user_id)
                coupons = get_user_coupons(user_id)
                print(f"\n📊 用户状态:")
                print(f"   积分: {points}")
                print(f"   优惠券: {len(coupons)} 张")
                for coupon in coupons:
                    print(f"      - {coupon['type']}: {coupon['code']}")
                print()
                continue

            # 调用 Agent
            response, chat_history = chat_with_concierge(
                user_input=user_input,
                chat_history=chat_history,
                user_id=user_id
            )

        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}\n")
            import traceback
            traceback.print_exc()
