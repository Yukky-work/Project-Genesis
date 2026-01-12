# app.py
# Project_Genesis: 3D Galaxy Monitor (DB連携版)

import streamlit as st
import pandas as pd
import plotly.express as px
import db  # さっき作った db.py を読み込む！
from datetime import datetime

# ページ設定
st.set_page_config(page_title="Project_Genesis", layout="wide")

# タイトル
st.title("🌌 Project_Genesis: 3D Galaxy Monitor")
st.write("マウスで宇宙をぐりぐり動かしてください！")

# --- データベース操作関数 ---

def load_data():
    """スプレッドシートからデータを読み込んでDataFrameにする"""
    sheet = db.get_database()
    if sheet:
        # シートの全データを辞書リストとして取得
        records = sheet.get_all_records()
        if records:
            return pd.DataFrame(records)
    
    # データがない、または接続エラーの場合は空のDataFrameを返す
    return pd.DataFrame(columns=["star_id", "x", "y", "z", "color", "size", "timestamp"])

def add_star_to_db():
    """新しい星を生成してスプレッドシートに追加する"""
    import random
    
    # ランダムな星のデータを生成
    new_star = [
        random.randint(1000, 9999),  # ID
        random.uniform(-10, 10),     # X
        random.uniform(-10, 10),     # Y
        random.uniform(-10, 10),     # Z
        random.choice(["blue", "red", "yellow", "white"]), # Color
        random.randint(10, 50),      # Size
        datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Timestamp
    ]
    
    sheet = db.get_database()
    if sheet:
        # スプレッドシートに行を追加
        sheet.append_row(new_star)
        return True
    return False

# --- メイン処理 ---

# 1. データの読み込み
df = load_data()

# 2. サイドバー（コントロールパネル）
# app.py のサイドバー部分を修正

st.sidebar.header("⚡ Genesis Control")

# 1. パスワード入力欄を作る
user_pass = st.sidebar.text_input("🔑 アクセスキー", type="password")

# 2. パスワードが合っているかチェック
if user_pass == st.secrets["app_password"]:
    st.sidebar.success("認証成功！")
    
    # ★ここにボタンを隠す！
    if st.sidebar.button("🚀 ビッグバン (星を生成)"):
        if add_star_to_db():
            st.success("新しい星が宇宙に誕生しました！")
            st.rerun()
        else:
            st.error("星の生成に失敗しました... (DB接続エラー)")
else:
    # パスワードが違う、または空の時
    st.sidebar.info("パスワードを入力するとボタンが現れます")

# 3. データがある場合のみ3D宇宙を表示
if not df.empty:
    # 3D散布図の作成
    fig = px.scatter_3d(
        df,
        x='x', y='y', z='z',
        color='color',
        size='size',
        hover_data=['timestamp'],
        range_x=[-10, 10], range_y=[-10, 10], range_z=[-10, 10],
        opacity=0.8,
        height=700
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # データフレームの表示（デバッグ用）
    with st.expander("📊 生データを見る"):
        st.dataframe(df)

else:
    st.info("👈 サイドバーのボタンを押して、最初の星を作ってください！")