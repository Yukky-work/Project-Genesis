# src/modules/ui.py
import streamlit as st

def setup_page():
    """ページ設定とCSSの読み込み"""
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

def display_sidebar(characters, current_name, histories):
    """サイドバーの表示処理"""
    st.sidebar.title("👥 メンバー指名")
    selected_name = st.sidebar.radio("担当者を選択:", list(characters.keys()), index=list(characters.keys()).index(current_name))
    
    current_char = characters[selected_name]
    
    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Mode Select")
    is_analysis_mode = st.sidebar.toggle("📊 データ分析モード", value=False)
    
    uploaded_file = None
    if is_analysis_mode:
        st.sidebar.info("CSVをアップロードしてください")
        uploaded_file = st.sidebar.file_uploader("CSVファイル", type=["csv"])
    else:
        st.sidebar.write("📸 画像を見せる")
        uploaded_file = st.sidebar.file_uploader("写真をアップロード", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

    # 立ち絵表示
    with st.sidebar:
        st.divider()
        st.write("🖼️ パートナー")
        if current_char['icon'].endswith(('.png', '.jpg', '.jpeg', '.gif')):
            st.image(current_char['icon'], caption=f"{selected_name}", use_container_width=True)
        else:
            st.markdown(f"<div style='font-size: 80px; text-align: center;'>{current_char['icon']}</div>", unsafe_allow_html=True)
            
        if st.button("🗑️ 会話をクリア"):
            histories[selected_name] = []
            st.rerun()
            
    return selected_name, is_analysis_mode, uploaded_file

def display_chat_history(history, char_icon):
    """会話ログの表示"""
    for msg in history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant", avatar=char_icon).write(msg["content"])

def display_main_header(name, char_data, is_analysis_mode):
    """メイン画面のヘッダー表示"""
    col1, col2 = st.columns([1, 8])
    with col1:
        if char_data['icon'].endswith(('.png', '.jpg', '.jpeg', '.gif')):
            st.image(char_data['icon'], use_container_width=True)
        else:
            st.markdown(f"<div class='breathing-icon'>{char_data['icon']}</div>", unsafe_allow_html=True)
    with col2:
        title_suffix = " [Analysis Mode 📊]" if is_analysis_mode else ""
        st.title(f"{name}{title_suffix}")
        st.caption(f"性格: {char_data['style']}")
    st.divider()