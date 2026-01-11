# app.py
# 3D宇宙空間 対応版

import streamlit as st
import pandas as pd
import os
import star_generator
import config
import plotly.express as px  # ✨ 新しい描画エンジン！

st.set_page_config(page_title="Project_Genesis: Cosmos 3D", page_icon="🌌", layout="wide")

st.title("🌌 Project_Genesis: 3D Galaxy Monitor")
st.markdown("### マウスで宇宙をぐりぐり動かしてください！")

CSV_FILE = "cosmos_db.csv"

# --- サイドバー ---
st.sidebar.header("⚡ Genesis Control")

if st.sidebar.button("🚀 ビッグバン (星を生成)"):
    if os.path.exists(CSV_FILE):
        existing_df = pd.read_csv(CSV_FILE)
        last_id = existing_df['id'].max() if len(existing_df) > 0 else 0
    else:
        existing_df = pd.DataFrame()
        last_id = 0
        
    new_stars = []
    start_id = last_id + 1
    for i in range(start_id, start_id + config.STAR_COUNT):
        new_stars.append(star_generator.create_star(i))
        
    new_df = pd.DataFrame(new_stars)
    
    if not existing_df.empty:
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df
        
    updated_df.to_csv(CSV_FILE, index=False)
    st.sidebar.success(f"✨ 新たな星が {config.STAR_COUNT} 個、座標を持って誕生しました！")


# --- メイン画面 ---

if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    
    # 🌍 全宇宙の総人口を計算 (sum関数で一発！)
    total_pop = df['population'].sum()
    
    # 3カラムで重要指標(KPI)を表示
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("現在の星の総数", f"{len(df)} Stars")
    kpi2.metric("銀河総人口", f"{total_pop:,} 人") # カンマ区切り表示
    kpi3.metric("発見された文明数", f"{df['civilization'].nunique()} Types")
    
    tab1, tab2 = st.tabs(["🪐 3D宇宙地図", "📜 文明データ台帳"])
    
    with tab1:
        st.subheader(f"観測中の宇宙")
        # hover_data に文明情報を追加！マウスを乗せると文明が見える！
        fig = px.scatter_3d(
            df, x='x', y='y', z='z', color='color', size='size',
            hover_name='name',
            hover_data={'civilization': True, 'population': True, 'x':False, 'y':False, 'z':False},
            color_discrete_map={
                "Blue": "blue", "Red": "red", "Yellow": "gold", "White": "white", "Purple": "purple"
            },
            template="plotly_dark", opacity=0.8
        )
        st.plotly_chart(fig, use_container_width=True, height=600)
        
    with tab2:
        # 文明ごとにグループ分けして、人口ランキングを表示
        st.subheader("📊 文明別・人口統計")
        
        # 文明ごとの人口合計を計算
        civ_stats = df.groupby('civilization')['population'].sum().reset_index()
        
        col_table, col_chart = st.columns([1, 2])
        with col_table:
            st.dataframe(civ_stats, hide_index=True)
        with col_chart:
            st.bar_chart(civ_stats.set_index('civilization'))
            
        st.subheader("詳細データリスト")
        st.dataframe(df.sort_values('id', ascending=False), use_container_width=True)

else:
    st.info("👈 サイドバーのボタンを押して、文明の種をまいてください！")