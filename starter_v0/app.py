"""
Checkpoint 5 — Streamlit UI cho Research Agent (Group E2)
Chạy: streamlit run app.py  (từ trong thư mục starter_v0/)
"""
import os
import json
from pathlib import Path
from datetime import datetime

import streamlit as st

# ── Cấu hình trang ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent — Group E2",
    page_icon="🤖",
    layout="wide",
)

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Import các module của project ────────────────────────────────────────────
try:
    from env_loader import load_lab_env
    from providers import make_provider
    from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
    from versioning import artifact_version_dict, build_artifact_version
    from chat import run_model_tool_loop, trim_history, now_iso, safe_slug, write_transcript
    load_lab_env(ROOT)
except Exception as e:
    st.error(f"Lỗi import module: {e}")
    st.stop()

# ── Sidebar: cấu hình agent ──────────────────────────────────────────────────
st.sidebar.title("⚙️ Cấu hình Agent")

version_label = st.sidebar.text_input("Artifact Version", value="v4")

provider_name = st.sidebar.selectbox(
    "Provider",
    ["groq", "openrouter", "openai", "gemini", "ollama"],
)

# Default model theo provider
_default_models = {
    "groq": "openai/gpt-oss-20b",
    "openrouter": "openai/gpt-4o-mini",
    "openai": "gpt-4o-mini",
    "gemini": "gemini-1.5-flash",
    "ollama": "qwen2.5:7b",
}
model_name = st.sidebar.text_input(
    "Model (để trống = dùng mặc định)",
    value=_default_models.get(provider_name, ""),
)

# API Key input theo provider
_env_map = {
    "groq": "GROQ_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
}
env_var = _env_map.get(provider_name)
if env_var:
    saved_key = os.getenv(env_var, "")
    entered_key = st.sidebar.text_input(
        f"API Key ({env_var})",
        value=saved_key,
        type="password",
    )
    if entered_key:
        os.environ[env_var] = entered_key.strip()
    elif not saved_key:
        st.sidebar.warning(f"⚠️ Chưa có `{env_var}`. Nhập vào đây hoặc thêm vào `.env`.")

# Cấu hình Telegram Bot (tùy chọn để gửi tin thật)
with st.sidebar.expander("📬 Cấu hình Telegram (Gửi tin thật)", expanded=False):
    tg_token_val = os.getenv("TELEGRAM_BOT_TOKEN", "")
    tg_chat_val = os.getenv("TELEGRAM_CHAT_ID", "")
    new_tg_token = st.text_input("TELEGRAM_BOT_TOKEN", value=tg_token_val, type="password", help="Token từ @BotFather")
    new_tg_chat = st.text_input("TELEGRAM_CHAT_ID", value=tg_chat_val, help="Chat ID của kênh/user (vd: @channel hoặc số)")
    if new_tg_token:
        os.environ["TELEGRAM_BOT_TOKEN"] = new_tg_token.strip()
    if new_tg_chat:
        os.environ["TELEGRAM_CHAT_ID"] = new_tg_chat.strip()

history_window = st.sidebar.slider("History Window", min_value=1, max_value=10, value=5)
max_tool_rounds = st.sidebar.slider("Max Tool Rounds", min_value=1, max_value=8, value=4)

# ── Khởi tạo session state ───────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

if "transcript" not in st.session_state:
    sp_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    artifact_version = build_artifact_version(version_label, sp_path, tools_path)
    ts = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    tid = f"{safe_slug(version_label)}_{safe_slug(provider_name)}_{ts}"
    st.session_state.transcript_path = TRANSCRIPTS_DIR / f"{tid}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": tid,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": model_name or "default",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🤖 Research Agent UI — Group E2")
st.caption("Giao diện chat với Research Agent. Transcript tự động lưu theo chuẩn RUBRIC.")

# ── Hiển thị lịch sử chat ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tool_calls"):
            with st.expander("🛠️ Tool Calls", expanded=False):
                for tc in msg["tool_calls"]:
                    st.markdown(f"**`{tc['name']}`**")
                    st.json(tc.get("args", {}))

# ── Chat input ───────────────────────────────────────────────────────────────
user_input = st.chat_input("Nhập câu hỏi hoặc yêu cầu nghiên cứu…")

if user_input:
    # Hiển thị tin người dùng
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Tải tool declarations
    tool_declarations = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    openai_tools = to_openai_tools(tool_declarations)
    system_prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")

    # Khởi tạo provider
    with st.chat_message("assistant"):
        status = st.status("Đang xử lý…", expanded=True)
        reply_placeholder = st.empty()

        try:
            provider = make_provider(provider_name)
        except Exception as e:
            status.update(label="Lỗi provider", state="error")
            reply_placeholder.error(f"Lỗi khởi tạo provider: {e}")
            st.stop()

        messages = [
            {"role": "system", "content": system_prompt},
            *trim_history(st.session_state.history, history_window),
            {"role": "user", "content": user_input},
        ]

        turn_record = {
            "turn_index": len(st.session_state.transcript["turns"]) + 1,
            "started_at": now_iso(),
            "user": user_input,
            "status": "started",
            "assistant_text": None,
            "rounds": [],
            "tool_events": [],
        }

        try:
            result = run_model_tool_loop(
                provider=provider,
                messages=messages,
                tools=openai_tools,
                model=model_name or None,
                max_tool_rounds=max_tool_rounds,
            )
            turn_record.update(result)
            assistant_text = result["assistant_text"]

            # Ghi tool calls vào status
            all_tool_calls = [
                tc
                for rnd in result.get("rounds", [])
                for tc in rnd.get("tool_calls", [])
            ]
            for tc in all_tool_calls:
                status.write(f"🔧 `{tc['name']}` → `{tc['args']}`")

            status.update(label="✅ Hoàn thành", state="complete", expanded=False)
            reply_placeholder.markdown(assistant_text)

            # Lưu vào session
            st.session_state.history.append({"role": "user", "content": user_input})
            st.session_state.history.append({"role": "assistant", "content": assistant_text})
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_text,
                "tool_calls": all_tool_calls,
            })

        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            status.update(label="Gặp lỗi", state="error")
            reply_placeholder.error(f"Lỗi: {err}")
            turn_record.update({"status": "provider_error", "error": err})

        turn_record["ended_at"] = now_iso()
        st.session_state.transcript["turns"].append(turn_record)
        write_transcript(st.session_state.transcript_path, st.session_state.transcript)
        st.caption(f"💾 Transcript: `{st.session_state.transcript_path.name}`")
