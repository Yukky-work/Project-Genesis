# src/main.py
import streamlit as st
import re # ★追加: これがないとコードを見つけられません
from characters import DATA as CHARACTERS

# 分割したモジュールをインポート
from modules import ui, brain, voice

# --- 1. 初期設定 ---
ui.setup_page()

if "histories" not in st.session_state:
    st.session_state["histories"] = {name: [] for name in CHARACTERS.keys()}
    if "current_char_name" not in st.session_state:
        st.session_state["current_char_name"] = list(CHARACTERS.keys())[0]

# --- 2. サイドバー表示 ---
selected_name, is_analysis_mode, uploaded_file = ui.display_sidebar(
    CHARACTERS, 
    st.session_state["current_char_name"], 
    st.session_state["histories"]
)
st.session_state["current_char_name"] = selected_name

current_char = CHARACTERS[selected_name]
current_history = st.session_state["histories"][selected_name]
char_index = list(CHARACTERS.keys()).index(selected_name)

# --- 3. メイン画面ヘッダー ---
ui.display_main_header(selected_name, current_char, is_analysis_mode)

# --- 4. 会話ログ表示 ---
ui.display_chat_history(current_history, current_char['icon'])

# --- 5. 入力エリア ---
st.write("---")
col_mic, col_spacer = st.columns([2, 8])
with col_mic:
    st.write("🎙️ 音声入力:")
    audio_data = voice.get_audio_input(char_index)

text_input = st.chat_input(f"{selected_name} にメッセージを送る...")

# --- 6. 処理実行 ---
if audio_data or text_input:
    # (ユーザー入力表示...省略...前と同じ)
    display_text = "🎤 (音声)" if audio_data else text_input
    if is_analysis_mode and uploaded_file: display_text += f" + 📎{uploaded_file.name}"
    elif not is_analysis_mode and uploaded_file: display_text += " + 📸"
    
    st.chat_message("user").write(display_text)
    st.session_state["histories"][selected_name].append({"role": "user", "content": display_text})

    # AI処理
    with st.spinner(f"{selected_name} が考え中..."):
        ai_msg = brain.get_gemini_response(
            prompt=text_input if text_input else "音声入力",
            image=uploaded_file if not is_analysis_mode else None,
            csv_file=uploaded_file if is_analysis_mode else None,
            audio_bytes=audio_data['bytes'] if audio_data else None,
            system_prompt=current_char['prompt']
        )
        
        # 1. AIの回答を表示
        st.chat_message("assistant", avatar=current_char['icon']).write(ai_msg)
        st.session_state["histories"][selected_name].append({"role": "assistant", "content": ai_msg})
        
        # 2. ★Phase 5: コード実行 & グラフ描画
        code_match = re.search(r"```python\n(.*?)```", ai_msg, re.DOTALL)
        
        if code_match:
            python_code = code_match.group(1)
            
            with st.status("👩‍💻 Fuuがコードを実行中...", expanded=True):
                st.write("生成されたコード:")
                st.code(python_code, language='python')
                
                # ★修正: 戻り値を2つ受け取る (テキスト, グラフ画像)
                result_text, result_fig = brain.execute_python_code(python_code)
                
                st.write("実行結果:")
                st.info(result_text)
                
                # 結果ログ作成
                log_content = f"\n【システム通知: コード実行結果】\n{result_text}"

                # ★グラフがあれば表示！
                if result_fig:
                    st.write("📊 生成されたグラフ:")
                    st.pyplot(result_fig) # ここで描画！
                    log_content += "\n(グラフが生成されました)"
                
                st.session_state["histories"][selected_name].append({"role": "system", "content": log_content})

    # 音声再生
    voice_bytes = voice.play_voice(ai_msg)
    if voice_bytes:
        st.audio(voice_bytes, format="audio/wav", autoplay=True)