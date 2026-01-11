import os
import requests
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder # ★録音用(文字変換なし)

# キャラクターデータ
from characters import DATA as CHARACTERS

# --- 1. 設定 ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("APIキー設定エラー")
    st.stop()

genai.configure(api_key=API_KEY)
MODEL_NAME = os.getenv("API_MODEL")
model = genai.GenerativeModel(MODEL_NAME)

# --- 2. ページ設定 & CSS ---
st.set_page_config(page_title="My AI Team", page_icon="🤖", layout="wide")

st.markdown("""
<style>
@keyframes breathe {
    0% { transform: scale(0.98); }
    50% { transform: scale(1.02); }
    100% { transform: scale(0.98); }
}
[data-testid="stImage"] img {
    animation: breathe 3s infinite ease-in-out;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.breathing-icon {
    display: inline-block;
    animation: breathe 3s infinite ease-in-out;
    font-size: 5rem;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- 3. 記憶 ---
if "histories" not in st.session_state:
    st.session_state["histories"] = {name: [] for name in CHARACTERS.keys()}

# --- 4. サイドバー ---
st.sidebar.title("👥 メンバー指名")
selected_name = st.sidebar.radio("担当者を選択:", list(CHARACTERS.keys()))

current_char = CHARACTERS[selected_name]
current_history = st.session_state["histories"][selected_name]
char_index = list(CHARACTERS.keys()).index(selected_name) # ID用

st.sidebar.divider()
st.sidebar.subheader("⚙️ Mode Select")
is_analysis_mode = st.sidebar.toggle("📊 データ分析モード", value=False)

uploaded_image = None
uploaded_csv = None

if is_analysis_mode:
    st.sidebar.info("分析モード起動中...")
    uploaded_csv = st.sidebar.file_uploader("CSVファイル", type=["csv"])
else:
    st.sidebar.write("📸 画像を見せる")
    uploaded_image = st.sidebar.file_uploader("写真をアップロード", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

with st.sidebar:
    st.divider()
    st.write("🖼️ パートナー")
    if current_char['icon'].endswith(('.png', '.jpg', '.jpeg', '.gif')):
        st.image(current_char['icon'], caption=f"{selected_name}", use_container_width=True)
    else:
        st.markdown(f"<div style='font-size: 80px; text-align: center;'>{current_char['icon']}</div>", unsafe_allow_html=True)
    
    if st.button("🗑️ 会話をクリア"):
        st.session_state["histories"][selected_name] = []
        st.rerun()

# --- 5. メイン画面 ---
col1, col2 = st.columns([1, 8])
with col1:
    if current_char['icon'].endswith(('.png', '.jpg', '.jpeg', '.gif')):
        st.image(current_char['icon'], use_container_width=True)
    else:
        st.markdown(f"<div class='breathing-icon'>{current_char['icon']}</div>", unsafe_allow_html=True)

with col2:
    if is_analysis_mode:
        st.title(f"{selected_name} [Analysis Mode 📊]")
    else:
        st.title(f"{selected_name}")
    st.caption(f"性格: {current_char['style']}")

st.divider()

# --- 6. 会話ログ ---
for msg in current_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant", avatar=current_char['icon']).write(msg["content"])

# --- 7. 入力エリア (マルチモーダル版) ---
st.write("---") 

col_mic, col_spacer = st.columns([2, 8])
audio_data = None # 録音データが入る変数

with col_mic:
    st.write("🎙️ 音声入力 (Gemini直通):")
    # 単純な録音ボタン (mic_recorder) に戻しました
    # これなら勝手な翻訳をせず、生の音声データを返してくれます
    audio_data = mic_recorder(
        start_prompt="● 録音 (ON)",
        stop_prompt="■ 停止 (OFF)",
        key=f'MIC_{char_index}'
    )

text_input = st.chat_input(f"{selected_name} にメッセージを送る...")

# --- 8. 送信処理 ---
if audio_data or text_input:
    # A. ユーザーの入力を確定させる
    user_content_for_gemini = []
    display_text = ""

    if audio_data:
        # 音声がある場合: Geminiに「この音を聞いて」と頼む
        display_text = "🎤 (音声メッセージを送信しました)"
        # 音声データをGemini用の形式に
        user_content_for_gemini = [
            "以下の音声をユーザーの発言として聞き取り、その内容に対して返事をしてください。",
            {"mime_type": "audio/webm", "data": audio_data['bytes']}
        ]
    elif text_input:
        # テキストの場合
        display_text = text_input
        user_content_for_gemini = ["ユーザー: " + text_input]

    # B. 画面に表示
    st.chat_message("user").write(display_text)
    st.session_state["histories"][selected_name].append({"role": "user", "content": display_text})

    # C. 他の添付ファイル (画像/CSV) を追加
    base_prompt = current_char['prompt']
    final_prompt_list = [base_prompt] # まずシステムプロンプト

    # 添付ファイル処理
    if is_analysis_mode:
        final_prompt_list.append("\n【モード: データ分析】専門家として振る舞ってください。")
        if uploaded_csv:
            try:
                import pandas as pd
                df = pd.read_csv(uploaded_csv)
                csv_head = df.head().to_markdown()
                final_prompt_list.append(f"【CSVデータ(先頭5行)】\n{csv_head}")
            except: pass
    elif not is_analysis_mode and uploaded_image:
        img = Image.open(uploaded_image)
        final_prompt_list.append(img)
    
    # 最後にユーザーの入力(音声orテキスト)を結合
    final_prompt_list.extend(user_content_for_gemini)

    # D. Gemini実行
    with st.spinner(f"{selected_name} が考え中..."):
        try:
            response = model.generate_content(final_prompt_list)
            ai_msg = response.text
        except Exception as e:
            ai_msg = f"エラー: {e}"

    # E. 結果表示 & 履歴保存
    st.chat_message("assistant", avatar=current_char['icon']).write(ai_msg)
    st.session_state["histories"][selected_name].append({"role": "assistant", "content": ai_msg})

    # F. 音声再生 (VOICEVOX)
    def generate_voice(text, speaker_id=2):
        try:
            res1 = requests.post("http://127.0.0.1:50021/audio_query", params={"text": text, "speaker": speaker_id})
            if res1.status_code != 200: return None
            query = res1.json()
            res2 = requests.post("http://127.0.0.1:50021/synthesis", json=query, params={"speaker": speaker_id})
            return res2.content
        except: return None

    audio_bytes = generate_voice(ai_msg, speaker_id=2)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav", autoplay=True)