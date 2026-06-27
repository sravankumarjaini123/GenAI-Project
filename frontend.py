import streamlit as st
import requests

st.set_page_config(
    page_title="Generative AI Chatbot",
    page_icon="✨",
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Base ── */
    #MainMenu, footer, header { visibility: hidden; }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 7rem;
        max-width: 800px;
    }

    /* ── Header banner ── */
    .chat-header {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
    }
    .chat-header .logo {
        font-size: 48px;
        margin-bottom: 0.4rem;
        filter: drop-shadow(0 0 20px rgba(139,92,246,0.6));
    }
    .chat-header h1 {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .chat-header p {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 0.4rem;
    }

    /* ── Suggestion cards (welcome screen) ── */
    .suggestion-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin: 1.5rem 0;
    }
    .suggestion-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 14px 16px;
        cursor: pointer;
        transition: all 0.2s ease;
        backdrop-filter: blur(10px);
    }
    .suggestion-card:hover {
        background: rgba(139,92,246,0.15);
        border-color: rgba(139,92,246,0.4);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(139,92,246,0.15);
    }
    .suggestion-card .icon { font-size: 20px; margin-bottom: 6px; }
    .suggestion-card .title {
        font-size: 13px;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 2px;
    }
    .suggestion-card .sub {
        font-size: 12px;
        color: #64748b;
    }

    /* ── Message row wrapper ── */
    .msg-row {
        display: flex;
        align-items: flex-start;
        margin: 12px 0;
        gap: 10px;
        animation: fadeSlide 0.3s ease;
    }
    .msg-row.user { flex-direction: row-reverse; }

    @keyframes fadeSlide {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Avatars ── */
    .avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .avatar.user-avatar {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        box-shadow: 0 0 12px rgba(139,92,246,0.4);
    }
    .avatar.ai-avatar {
        background: linear-gradient(135deg, #0ea5e9, #34d399);
        box-shadow: 0 0 12px rgba(52,211,153,0.3);
    }

    /* ── Bubbles ── */
    .bubble {
        max-width: 72%;
        padding: 12px 16px;
        border-radius: 18px;
        font-size: 14.5px;
        line-height: 1.7;
        word-wrap: break-word;
    }
    .user-bubble {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #fff;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 20px rgba(139,92,246,0.3);
    }
    .ai-bubble {
        background: rgba(255,255,255,0.07);
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
        border-bottom-left-radius: 4px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }

    /* ── Timestamp ── */
    .msg-meta {
        font-size: 10px;
        color: #475569;
        margin-top: 3px;
        padding: 0 4px;
    }
    .msg-meta.right { text-align: right; }

    /* ── Divider ── */
    .chat-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
        margin: 8px 0;
    }

    /* ── Chat input ── */
    .stChatInput > div {
        background: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    }
    .stChatInput > div:focus-within {
        border-color: rgba(139,92,246,0.7) !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,0.2), 0 8px 32px rgba(0,0,0,0.3) !important;
    }
    .stChatInput textarea,
    .stChatInput textarea:focus,
    [data-testid="stChatInput"] textarea,
    div[data-baseweb="textarea"] textarea {
        color: #000000 !important;
        caret-color: #000000 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        -webkit-text-fill-color: #000000 !important;
    }
    .stChatInput textarea::placeholder,
    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
    }

    /* ── Spinner ── */
    .stSpinner > div { color: #a78bfa !important; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: rgba(15,12,41,0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(20px);
    }
    .sidebar-logo {
        font-size: 24px;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.2rem;
        display: block;
    }
    .new-chat-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        cursor: pointer;
        width: 100%;
        box-shadow: 0 4px 15px rgba(139,92,246,0.3);
        transition: all 0.2s ease;
    }
    .new-chat-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(139,92,246,0.4);
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(139,92,246,0.25) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(139,92,246,0.4) !important;
    }
    .history-item {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 8px;
        padding: 8px 10px;
        margin: 4px 0;
        font-size: 12.5px;
        color: #94a3b8;
        cursor: pointer;
        transition: background 0.15s;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .history-item:hover { background: rgba(139,92,246,0.1); color: #c4b5fd; }
    .history-label {
        font-size: 11px;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 12px 0 6px;
    }
    .sidebar-input label { color: #64748b !important; font-size: 12px !important; }
    .sidebar-input input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-size: 12px !important;
    }
    .stat-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 10px 14px;
        margin: 6px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stat-label { font-size: 12px; color: #64748b; }
    .stat-value { font-size: 14px; font-weight: 600; color: #a78bfa; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<span class="sidebar-logo">✨ Sravan Gen AI</span>', unsafe_allow_html=True)

    if st.button("＋  New Conversation"):
        st.session_state.messages = []
        st.rerun()

    # Stats
    total = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.markdown(f"""
    <div class="stat-box">
        <span class="stat-label">Messages sent</span>
        <span class="stat-value">{total}</span>
    </div>
    """, unsafe_allow_html=True)

    # History
    user_msgs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
    if user_msgs:
        st.markdown('<div class="history-label">This Session</div>', unsafe_allow_html=True)
        for msg in user_msgs:
            preview = ("💬  " + msg[:38] + "…") if len(msg) > 38 else ("💬  " + msg)
            st.markdown(f'<div class="history-item">{preview}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="history-label">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-input">', unsafe_allow_html=True)
    api_url = st.text_input("Backend URL", value="http://localhost:8000", label_visibility="visible")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:11px;color:#334155;margin-top:4px;">uvicorn backend:app --port 8000</p>',
        unsafe_allow_html=True,
    )

# ── Welcome screen ────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="chat-header">
        <div class="logo">✨</div>
        <h1>How can I help you today?</h1>
        <p>Powered by Claude AI — ask me anything</p>
    </div>
    <div class="suggestion-grid">
        <div class="suggestion-card">
            <div class="icon">💡</div>
            <div class="title">Explain a concept</div>
            <div class="sub">Break down complex ideas simply</div>
        </div>
        <div class="suggestion-card">
            <div class="icon">🐍</div>
            <div class="title">Python help</div>
            <div class="sub">Code, debug, or learn Python</div>
        </div>
        <div class="suggestion-card">
            <div class="icon">✍️</div>
            <div class="title">Write something</div>
            <div class="sub">Emails, essays, summaries</div>
        </div>
        <div class="suggestion-card">
            <div class="icon">🔍</div>
            <div class="title">Analyze & compare</div>
            <div class="sub">Pros, cons, and insights</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Render messages ───────────────────────────────────────────────────────────
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-row user">
            <div class="avatar user-avatar">👤</div>
            <div>
                <div class="bubble user-bubble">{msg["content"]}</div>
                <div class="msg-meta right">You</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        content = msg["content"]
        web_tag = ""
        if content.startswith("Live web search used.\n\n"):
            content = content[len("Live web search used.\n\n"):]
            web_tag = '<span style="font-size:11px;background:rgba(52,211,153,0.15);color:#34d399;border:1px solid rgba(52,211,153,0.3);border-radius:20px;padding:2px 10px;margin-left:6px;">Live Web Search</span>'
        st.markdown(f"""
        <div class="msg-row">
            <div class="avatar ai-avatar">✨</div>
            <div>
                <div class="bubble ai-bubble">{content}</div>
                <div class="msg-meta">Claude AI {web_tag}</div>
            </div>
        </div>
        <div class="chat-divider"></div>
        """, unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
question = st.chat_input("Ask anything…")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.msg_count += 1

    with st.spinner("Searching the web and thinking…"):
        try:
            resp = requests.post(
                f"{api_url}/ask-ai",
                json={"userQuestion": question},
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                answer = data.get("answer", "No response received.")
                web_used = data.get("web_search_used", False)
                if web_used:
                    answer = "Live web search used.\n\n" + answer
            else:
                answer = f"Backend error {resp.status_code}: {resp.text}"
                web_used = False
        except requests.exceptions.ConnectionError:
            answer = "Cannot reach the backend. Make sure `uvicorn backend:app --port 8000` is running."
            web_used = False
        except Exception as e:
            answer = f"Unexpected error: {e}"
            web_used = False

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
