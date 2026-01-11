import os
import requests
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

from characters import DATA as CHARACTERS

# --- 1. 設定 ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- 2. ページ設定 ---
st.set_page_config(page_title="My AI Team", page_icon="🤖", layout="wide")

st.markdown("""
<style>
/* 呼吸アニメーションの定義 */
@keyframes breathe {
    0% { transform: scale(0.95); }
    50% { transform: scale(1.1); } /* 1.1倍まで膨らむ */
    100% { transform: scale(0.95); }
}

/* 1. アップロードした画像（写真など）を動かす */
[data-testid="stImage"] img {
    animation: breathe 3s infinite ease-in-out;
    border-radius: 10px;
}

/* 2. アイコン（絵文字）を動かすクラス */
.breathing-icon {
    display: inline-block; /* これがないと文字は変形しない */
    animation: breathe 3s infinite ease-in-out;
    font-size: 5rem; /* アイコンを大きくする */
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- 3. 記憶の初期化 ---
if "histories" not in st.session_state:
    st.session_state["histories"] = {name: [] for name in CHARACTERS.keys()}

# --- 4. サイドバー ---
st.sidebar.title("👥 メンバー指名")
selected_name = st.sidebar.radio("担当者を選択:", list(CHARACTERS.keys()))

current_char = CHARACTERS[selected_name]
current_history = st.session_state["histories"][selected_name]

st.sidebar.divider()

# ★ モード切替スイッチ ★
st.sidebar.subheader("⚙️ Mode Select")
is_analysis_mode = st.sidebar.toggle("📊 データ分析モード", value=False)

uploaded_image = None
uploaded_csv = None

if is_analysis_mode:
    # --- 分析モード時 ---
    st.sidebar.info("分析モード起動中...\nCSVファイルをアップロードしてください。")
    uploaded_csv = st.sidebar.file_uploader("CSVファイル", type=["csv"])
    # (分析モードでは画像UPは隠す、または両方OKにするなど調整可。今回はCSV優先で見やすくします)
else:
    # --- 通常モード時 ---
    st.sidebar.write("📸 画像を見せる")
    uploaded_image = st.sidebar.file_uploader("写真をアップロード", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

st.sidebar.divider()

if st.sidebar.button("🗑️ このチャットをクリア"):
    st.session_state["histories"][selected_name] = []
    st.rerun()

# --- 5. メイン画面 ---
# --- 5. メイン画面 ---
col1, col2 = st.columns([1, 8])
with col1:
    # 元のコード: st.title(current_char['icon'])
    # ↓
    # ★ 新しいコード: 絵文字を動かすクラスで包む！
    st.markdown(f"<div class='breathing-icon'>{current_char['icon']}</div>", unsafe_allow_html=True)
with col2:
    # モードによってタイトルを変える演出
    if is_analysis_mode:
        st.title(f"{selected_name} [Analysis Mode 📊]")
    else:
        st.title(f"{selected_name}")
    
    st.caption(f"性格: {current_char['style']}")

st.divider()

# --- 6. 会話ログ表示 ---
for msg in current_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant", avatar=current_char['icon']).write(msg["content"])

# --- 7. 入力処理 ---
if prompt := st.chat_input(f"{selected_name} に話しかける..."):
    # ユーザー表示
    st.chat_message("user").write(prompt)
    
    # 添付ファイルの表示
    display_content = prompt
    if is_analysis_mode and uploaded_csv:
        st.chat_message("user").write(f"📄 CSVファイル: {uploaded_csv.name}")
        display_content += f" (CSV: {uploaded_csv.name})"
    elif not is_analysis_mode and uploaded_image:
        img = Image.open(uploaded_image)
        st.chat_message("user").image(img, width=200)
        display_content += " (画像添付)"

    st.session_state["histories"][selected_name].append({"role": "user", "content": display_content})

    # Geminiへのプロンプト構築
    base_prompt = current_char['prompt']
    
    if is_analysis_mode:
        # ★分析モード用の追加指示
        system_prompt = f"""
        {base_prompt}
        
        【重要なお知らせ】
        現在、あなたは「データ分析モード」です。
        ユーザーからデータに関する質問や、分析の依頼が来る可能性があります。
        キャラクターの口調は崩さずに、論理的かつ専門的な視点でアドバイスをしてください。
        （※今はまだ実際にPythonコードを実行できませんが、実行するフリをして方針を提案してください）
        """
        # CSVの中身をテキストとして少し読ませる（簡易実装）
        if uploaded_csv:
             # 先頭5行だけ読んで渡す（トークン節約）
             try:
                 import pandas as pd
                 df = pd.read_csv(uploaded_csv)
                 csv_head = df.head().to_markdown()
                 full_prompt = f"{system_prompt}\n\nユーザー: {prompt}\n\n【アップロードされたデータ(先頭5行)】\n{csv_head}"
                 content_list = [full_prompt]
             except Exception:
                 content_list = [f"{system_prompt}\n\nユーザー: {prompt}"]
        else:
             content_list = [f"{system_prompt}\n\nユーザー: {prompt}"]

    else:
        # 通常モード（画像対応）
        if uploaded_image:
            img = Image.open(uploaded_image)
            content_list = [base_prompt, "ユーザー: " + prompt, img]
        else:
            content_list = [f"{base_prompt}\n\nユーザー: {prompt}"]

    # Gemini実行
    try:
        response = model.generate_content(content_list)
        ai_msg = response.text
    except Exception as e:
        ai_msg = f"エラー: {e}"

    # AI表示 & 履歴保存
    st.chat_message("assistant", avatar=current_char['icon']).write(ai_msg)
    st.session_state["histories"][selected_name].append({"role": "assistant", "content": ai_msg})

    # 音声再生（簡易）
    def generate_voice(text, speaker_id=2):
        try:
            res = requests.post("http://127.0.0.1:50021/audio_query", params={"text": text, "speaker": speaker_id})
            query = res.json()
            wav = requests.post("http://127.0.0.1:50021/synthesis", json=query, params={"speaker": speaker_id})
            return wav.content
        except: return None

    # おまけ：分析モードFuuはちょっとキリッとした声（ずんだもんなど）にしても面白いかも
    audio_bytes = generate_voice(ai_msg, speaker_id=2)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav", autoplay=True)