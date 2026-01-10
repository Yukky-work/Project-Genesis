import os
import requests # VOICEVOX用
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# キャラクターデータ読み込み
from characters import DATA as CHARACTERS

# --- 1. 設定 ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- 2. ページ設定 ---
st.set_page_config(page_title="My AI Team", page_icon="🤖", layout="wide")

# --- 3. 記憶の初期化 ---
if "histories" not in st.session_state:
    st.session_state["histories"] = {name: [] for name in CHARACTERS.keys()}

# --- 4. サイドバー ---
st.sidebar.title("👥 メンバー指名")
selected_name = st.sidebar.radio("担当者を選択:", list(CHARACTERS.keys()))

current_char = CHARACTERS[selected_name]
current_history = st.session_state["histories"][selected_name]

st.sidebar.divider()
st.sidebar.write("📸 画像を見せる")
uploaded_file = st.sidebar.file_uploader("写真をアップロード", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

if st.sidebar.button("🗑️ このチャットをクリア"):
    st.session_state["histories"][selected_name] = []
    st.rerun()

# --- 5. メイン画面 ---
col1, col2 = st.columns([1, 8])
with col1:
    st.title(current_char['icon'])
with col2:
    st.title(f"{selected_name}")
    st.caption(f"性格: {current_char['style']}")

st.divider()

# --- 6. 会話ログ表示 ---
for msg in current_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant", avatar=current_char['icon']).write(msg["content"])

# --- 7. 画像プレビュー ---
image_data = None
if uploaded_file:
    image_data = Image.open(uploaded_file)
    st.sidebar.image(image_data, caption="解析対象の画像", use_container_width=True)

# --- 8. 音声合成関数 (VOICEVOX) ---
# ※ ここを追加・修正！
def generate_voice(text, speaker_id=2): # デフォルトは四国めたん(ID:2)
    base_url = "http://127.0.0.1:50021"
    try:
        params = {"text": text, "speaker": speaker_id}
        query_res = requests.post(f"{base_url}/audio_query", params=params)
        query_json = query_res.json()
        
        synthesis_params = {"speaker": speaker_id}
        voice_res = requests.post(f"{base_url}/synthesis", json=query_json, params=synthesis_params)
        
        return voice_res.content # バイナリデータを返す
    except Exception:
        return None

# --- 9. 入力と実行 ---
if prompt := st.chat_input(f"{selected_name} にメッセージを送る..."):
    # ユーザー表示
    st.chat_message("user").write(prompt)
    if image_data:
        st.chat_message("user").image(image_data, width=200)
    
    st.session_state["histories"][selected_name].append({"role": "user", "content": prompt})

    # Geminiへ送信
    system_prompt = current_char['prompt']
    try:
        if image_data:
            content_list = [system_prompt, "ユーザー: " + prompt, image_data]
            response = model.generate_content(content_list)
        else:
            full_prompt = f"{system_prompt}\n\nユーザー: {prompt}"
            response = model.generate_content(full_prompt)
        ai_msg = response.text
    except Exception as e:
        ai_msg = "エラーが発生しました。"

    # AI表示
    st.chat_message("assistant", avatar=current_char['icon']).write(ai_msg)
    st.session_state["histories"][selected_name].append({"role": "assistant", "content": ai_msg})

    # ★ 音声を生成して再生！
    # (全員 四国めたん の声になりますが、IDを変えればキャラ分けも可能です)
    # Fuu=2(ノーマル), Shiori=10(あまあま), Gem Py=2(ノーマル) など
    # 今回は簡易的に全員 ID=2 または 3(ずんだもん) 等でテストしてください
    audio_bytes = generate_voice(ai_msg, speaker_id=2) 
    
    if audio_bytes:
        # autoplay=True で自動再生！
        st.audio(audio_bytes, format="audio/wav", autoplay=True)