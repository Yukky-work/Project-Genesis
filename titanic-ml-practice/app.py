import streamlit as st
import pandas as pd
import joblib

# 1. AIモデルを読み込む
# ※ 同じフォルダに 'titanic_model.pkl' があることが前提
model = joblib.load('titanic_model.pkl')

# --- ページ設定 ---
st.set_page_config(
    page_title="タイタニックAI占い",
    page_icon="🚢",
    layout="wide"
)

st.title("🚢 タイタニック生存予測AI")
st.markdown("あなたがもし乗船していたら...？ AIが運命を判定します！")
st.markdown("---")

# --- 画面レイアウト (2カラム) ---
col1, col2 = st.columns(2)

# --- 右側 (col2): 入力フォーム ---
with col2:
    st.header("👇 あなたの情報を入力")
    
    # 性別
    sex = st.radio("性別は？", ["Male (男性)", "Female (女性)"])
    sex_val = 0 if "Male" in sex else 1
    
    # 年齢
    age = st.slider("年齢は？", 0, 100, 30)
    
    # 客室等級
    pclass = st.selectbox("客室のランクは？", [1, 2, 3])
    st.caption("※ 1等=超豪華, 3等=庶民")
    
    # 運賃
    fare = st.slider("チケット代($)は？", 0, 600, 50)
    
    # 予測ボタン
    predict_btn = st.button("運命を占う！🔮", type="primary")

# --- 左側 (col1): 結果表示 ---
with col1:
    st.header("🤖 AIの判定結果")
    
    # 入力データの整形
    input_data = pd.DataFrame({
        'Pclass': [pclass],
        'Sex': [sex_val],
        'Age': [age],
        'SibSp': [0], # 今回は使わないので0固定
        'Parch': [0], # 今回は使わないので0固定
        'Fare': [fare],
        'Embarked': [0] # 今回は使わないので0固定
    })
    
    # 予測実行
    prediction = model.predict_proba(input_data)
    survival_rate = prediction[0][1] * 100
    
    # 結果表示
    st.metric(label="生存確率", value=f"{survival_rate:.1f}%")
    
    # メッセージ分岐
    if survival_rate > 50:
        st.success("🎉 おめでとうございます！ 生還の可能性が高いです！")
        if predict_btn:
            st.balloons()
    else:
        st.error("💀 残念ながら... 厳しい運命が待っているかもしれません...")