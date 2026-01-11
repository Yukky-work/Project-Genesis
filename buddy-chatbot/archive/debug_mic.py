import streamlit as st
from streamlit_mic_recorder import speech_to_text

st.title("🎙️ マイク・テストセンター")

st.write("ボタンを押して、何か喋ってみてください。")
st.write("※ Chromeブラウザ推奨です。")

# 最小構成のマイクボタン
text = speech_to_text(
    language='ja',
    start_prompt="● テスト開始",
    stop_prompt="■ 完了",
    just_once=False,
    key='DEBUG_MIC'
)

# デバッグ表示: 変数の中身をそのまま表示
st.write(f"受け取ったデータ: {text}")

if text:
    st.success(f"聞こえました！: {text}")
else:
    st.info("まだ何も聞こえていません（または認識失敗）。")