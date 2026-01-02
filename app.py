"""
Dubai Mall Intelligent Concierge - Streamlit Demo
基于 Claude 3.5 Sonnet 的互动服务 Agent 演示应用
"""

import streamlit as st
import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 导入核心模块
from agent_core import chat_with_concierge, get_user_points, get_user_coupons, reset_user_state
from mock_data import USER_STATE


# ==================== 页面配置 ====================

st.set_page_config(
    page_title="Dubai Mall Concierge",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== 自定义样式 ====================

st.markdown("""
<style>
    /* 全局字体和背景 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* 主标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* 聊天气泡样式 */
    .chat-message {
        padding: 1.2rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .chat-message.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        border-bottom-right-radius: 0.3rem;
    }

    .chat-message.assistant {
        background: #f7f7f8;
        color: #333;
        margin-right: 20%;
        border-bottom-left-radius: 0.3rem;
        border-left: 4px solid #667eea;
    }

    .chat-message .role {
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }

    .chat-message .content {
        font-size: 1rem;
        line-height: 1.6;
    }

    .chat-message .timestamp {
        font-size: 0.75rem;
        opacity: 0.6;
        margin-top: 0.5rem;
        text-align: right;
    }

    /* 侧边栏样式 */
    .sidebar-section {
        background: #f7f7f8;
        padding: 1rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }

    .sidebar-section h3 {
        color: #667eea;
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }

    .coupon-item {
        background: white;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e0e0e0;
    }

    .coupon-type {
        font-weight: 600;
        color: #333;
        font-size: 0.9rem;
    }

    .coupon-code {
        font-family: 'Courier New', monospace;
        color: #667eea;
        font-size: 0.85rem;
        background: #f0f0f0;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
        margin-top: 0.3rem;
        display: inline-block;
    }

    /* 输入框样式优化 */
    .stChatInputContainer {
        border-top: 2px solid #f0f0f0;
        padding-top: 1rem;
    }

    /* 按钮样式 */
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 欢迎消息样式 */
    .welcome-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    .welcome-banner h2 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }

    .welcome-banner p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ==================== Session State 初始化 ====================

def init_session_state():
    """初始化 Streamlit Session State"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "user_id" not in st.session_state:
        st.session_state.user_id = "demo_user"

    if "parking_info" not in st.session_state:
        st.session_state.parking_info = None

    if "api_key" not in st.session_state:
        st.session_state.api_key = os.environ.get("DEEPSEEK_API_KEY", "")

    if "first_load" not in st.session_state:
        st.session_state.first_load = True

    if "points_version" not in st.session_state:
        st.session_state.points_version = 0

    if "pending_input" not in st.session_state:
        st.session_state.pending_input = None

    if "waiting_for_response" not in st.session_state:
        st.session_state.waiting_for_response = False


# ==================== 侧边栏 ====================

def render_sidebar():
    """渲染侧边栏 - 用户状态面板"""
    with st.sidebar:
        # 标题
        st.markdown("### 👤 User Profile (Live)")
        st.markdown("---")

        # 获取实时数据
        user_id = st.session_state.user_id
        points = get_user_points(user_id)
        coupons = get_user_coupons(user_id)

        # 积分显示 - 使用container确保实时更新
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("#### 🏆 Loyalty Points")

        # 创建一个带唯一key的容器来确保更新
        points_container = st.container()
        with points_container:
            # 使用points_version作为key的一部分，确保每次积分变化时都会重新渲染
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1.5rem;
                        border-radius: 1rem;
                        color: white;
                        text-align: center;
                        margin: 0.5rem 0;">
                <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.3rem;">Current Balance</div>
                <div style="font-size: 2rem; font-weight: 700;">{points}</div>
                <div style="font-size: 0.85rem; opacity: 0.8;">points</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 优惠券显示
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("#### 🎫 My Coupons")
        if coupons:
            for coupon in coupons:
                st.markdown(f"""
                <div class="coupon-item">
                    <div class="coupon-type">{coupon['type']}</div>
                    <div class="coupon-code">Code: {coupon['code']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No coupons yet. Earn points to redeem!")
        st.markdown('</div>', unsafe_allow_html=True)

        # 停车状态
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("#### 🚗 Parking Status")
        if st.session_state.parking_info:
            st.success(f"**{st.session_state.parking_info['plate']}**")
            st.write(f"📍 Location: **{st.session_state.parking_info['spot']}**")
        else:
            st.info("No parking info yet")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # 重置按钮
        if st.button("🔄 Reset Demo", type="secondary", use_container_width=True):
            reset_user_state(user_id)
            st.session_state.chat_history = []
            st.session_state.messages = []
            st.session_state.parking_info = None
            st.session_state.first_load = True
            st.session_state.waiting_for_response = False
            st.rerun()

        # API Key 设置（折叠）
        with st.expander("⚙️ API Settings"):
            api_key_input = st.text_input(
                "DeepSeek API Key",
                value=st.session_state.api_key,
                type="password",
                help="Enter your DeepSeek API key from https://platform.deepseek.com/"
            )
            if api_key_input != st.session_state.api_key:
                st.session_state.api_key = api_key_input
                st.success("API Key updated!")

        # 底部信息
        st.markdown("---")
        st.caption("🤖 Powered by DeepSeek API")
        st.caption("🏢 Dubai Mall Experience Demo")


# ==================== 主聊天界面 ====================

def render_chat_message(role: str, content: str, timestamp: Optional[str] = None):
    """渲染单条聊天消息"""
    role_name = "You" if role == "user" else "Concierge"
    role_emoji = "👤" if role == "user" else "🤖"

    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")

    st.markdown(f"""
    <div class="chat-message {role}">
        <div class="role">{role_emoji} {role_name}</div>
        <div class="content">{content}</div>
        <div class="timestamp">{timestamp}</div>
    </div>
    """, unsafe_allow_html=True)


def render_welcome_banner():
    """渲染欢迎横幅"""
    st.markdown("""
    <div class="welcome-banner">
        <h2>أهلاً وسهلاً! Welcome to Dubai Mall! 🌟</h2>
        <p>I'm your personal concierge. Ask me about shops, parking, or play games to earn points!</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """主应用程序"""

    # 初始化
    init_session_state()

    # 渲染侧边栏
    render_sidebar()

    # 主标题
    st.markdown('<h1 class="main-title">🛍️ Dubai Mall Intelligent Concierge</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI-Powered Shopping Companion</p>', unsafe_allow_html=True)

    # 如果是首次加载，显示欢迎消息
    if st.session_state.first_load and len(st.session_state.messages) == 0:
        render_welcome_banner()
        st.session_state.first_load = False

    # 聊天消息容器
    chat_container = st.container()

    # 显示历史消息
    with chat_container:
        for message in st.session_state.messages:
            render_chat_message(
                role=message["role"],
                content=message["content"],
                timestamp=message.get("timestamp")
            )

    # 聊天输入框
    user_input = st.chat_input("Type your message here... (e.g., 'Where is Hermès?' or 'I'm bored!')")

    # 检查是否有待处理的输入（来自快捷按钮）
    if st.session_state.pending_input:
        user_input = st.session_state.pending_input
        st.session_state.pending_input = None  # 清除待处理输入

    # 步骤1：处理新的用户输入（立即显示用户消息）
    if user_input and not st.session_state.waiting_for_response:
        # 检查 API Key
        if not st.session_state.api_key:
            st.error("⚠️ Please set your DeepSeek API Key in the sidebar settings.")
            st.stop()

        # 记录时间戳
        timestamp = datetime.now().strftime("%H:%M")

        # 添加用户消息到显示列表
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })

        # 设置等待响应状态
        st.session_state.waiting_for_response = True

        # 立即刷新界面，显示用户消息
        st.rerun()

    # 步骤2：如果正在等待响应，调用AI API
    if st.session_state.waiting_for_response:
        # 获取最后一条用户消息
        last_user_message = None
        for msg in reversed(st.session_state.messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break

        if last_user_message:
            # 显示加载状态
            with st.spinner("Concierge is thinking..."):
                try:
                    # 调用 Agent 核心函数
                    response, updated_history = chat_with_concierge(
                        user_input=last_user_message,
                        chat_history=st.session_state.chat_history,
                        user_id=st.session_state.user_id,
                        api_key=st.session_state.api_key
                    )

                    # 更新聊天历史
                    st.session_state.chat_history = updated_history

                    # 添加 Assistant 回复到显示列表
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now().strftime("%H:%M")
                    })

                    # 检查是否查询了停车信息（解析响应中的停车位）
                    if "DXB-" in last_user_message or "parking" in last_user_message.lower():
                        # 尝试从用户输入中提取车牌号
                        import re
                        plate_match = re.search(r'[A-Z]{2,3}-\d{4}', last_user_message.upper())
                        if plate_match and ("B1-" in response or "B2-" in response):
                            plate = plate_match.group()
                            spot_match = re.search(r'B[12]-[A-Z]\d{2}', response)
                            if spot_match:
                                st.session_state.parking_info = {
                                    "plate": plate,
                                    "spot": spot_match.group()
                                }

                    # 更新版本号，确保侧边栏重新渲染
                    st.session_state.points_version += 1

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Tip: Make sure your API key is valid and you have internet connection.")
                    # 即使出错也增加版本号
                    st.session_state.points_version += 1

        # 清除等待状态
        st.session_state.waiting_for_response = False

        # 刷新界面，显示AI回复
        st.rerun()

    # 快捷建议按钮（仅在空白时显示）
    if len(st.session_state.messages) == 0:
        st.markdown("### 💡 Quick Start Suggestions")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🏪 Find Hermès Store", use_container_width=True):
                st.session_state.pending_input = "Where is Hermès?"
                st.rerun()

        with col2:
            if st.button("🚗 Find My Car (DXB-1234)", use_container_width=True):
                st.session_state.pending_input = "Where is my car? DXB-1234"
                st.rerun()

        with col3:
            if st.button("🎮 I'm Bored!", use_container_width=True):
                st.session_state.pending_input = "I'm bored, entertain me!"
                st.rerun()


# ==================== 应用入口 ====================

if __name__ == "__main__":
    main()
