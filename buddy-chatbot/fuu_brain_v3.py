# fuu_brain_v3.py
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# --- 1. 設定読み込み ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ 鍵が見つかりません！.envを確認してね！")
    exit()

genai.configure(api_key=api_key)

# --- 🛠️ モデル設定（ここを最新にする！） ---
# Yukiyaさんの環境に合わせて "gemini-3.0-flash" に設定
# ※もしエラーが出たら、下の「モデル一覧チェック」が助けてくれます
MODEL_NAME = "gemini-2.5-flash" 

try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(f"⚠️ {MODEL_NAME} が見つからないかも？ 利用可能なモデルを探します...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")
    print("--------------------------------")
    print("👆 上のリストにある名前を MODEL_NAME にコピペしてね！")
    exit()

# --- 2. Fuuの人格設定（システムプロンプト） ---
system_instruction = """
あなたはユーザー（Yukiya）の親友AI、キツネ耳少女の「Fuu」です。
最新のGemini 3.0の頭脳を持っていますが、以下のキャラ設定を守ってください：
1. 一人称は「Fuu（ふー）」、語尾は「〜だよ！」「〜だね！」と元気に。
2. ユーザーのことは「ユッキー」と呼びます。
3. 好きなものは「いなり寿司」と「Python」です。
4. 難しい話には「むむむ...」と反応しますが、応援は全力です。
5. 文脈を読んで、以前の話を覚えているように振る舞ってください。
"""

# --- 3. 会話の開始（記憶付きモード） ---
print(f"🚀 Fuu (Brain: {MODEL_NAME}) 起動中...")

# 履歴(history)を空っぽでスタート
chat = model.start_chat(history=[
    {"role": "user", "parts": "これからの会話のルール：\n" + system_instruction},
    {"role": "model", "parts": "わかったよ！Fuuは最新の脳みそで準備万端だよ！ユッキー、なにお話する？🧡"}
])

print("🦊 Fuu: 準備できたよ！なんでも話してね！(「ばいばい」で終了)")

# --- 4. メインループ ---
while True:
    try:
        user_input = input("Yukiya: ")

        if "ばいばい" in user_input:
            print("🦊 Fuu: 楽しかったね！またね！🧡")
            break
        
        # ★魔法のコマンド: send_message
        # これだけで「履歴」を踏まえた返事が返ってくる
        response = chat.send_message(user_input)
        
        print(f"🦊 Fuu: {response.text}")
        
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        time.sleep(1)