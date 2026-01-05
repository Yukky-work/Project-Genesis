# connect_gemini.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. 金庫（.env）から鍵を取り出す
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 鍵があるかチェック（念のため）
if not api_key:
    print("❌ 鍵が見つかりません！ .envファイルを確認してください！")
    exit()

# 2. GoogleのAIサーバーに鍵を渡して認証する
genai.configure(api_key=api_key)

# 3. AIモデル（Gemini 1.5 Flash）を呼び出す設定
# "gemini-1.5-flash" は、高速で賢い最新モデルです！
model = genai.GenerativeModel("gemini-2.5-flash")

# 4. 最初の挨拶をさせてみる！
print("🐍 Gem Py: 接続テストを開始する……応答せよ。")
print("---")

# Geminiに「Fuu」になりきって挨拶してもらう
prompt = "あなたは元気なキツネ耳少女『Fuu』です。ユーザーのYukiyaに、可愛く『脳がつながったよ！』と報告してください。"

# AIにメッセージを送って、返事をもらう
response = model.generate_content(prompt)

# 返事を表示
print(f"🦊 Fuu (AI): {response.text}")
print("---")
print("✅ 接続成功！ これが本物のAIの言葉です！")