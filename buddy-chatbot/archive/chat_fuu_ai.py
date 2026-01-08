# chat_fuu_ai.py
import os
import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# --- 1. 設定＆準備 ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ 鍵が見つかりません！")
    exit()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# Fuuちゃんの「人格」を作る（システムプロンプト）
# ここを変えると、キャラがガラッと変わります！
system_prompt = """
あなたはユーザー（Yukiya）の相棒、キツネ耳少女の「Fuu」です。
以下のルールを守って会話してください。
1. 語尾は「〜だよ！」「〜だね！」など、元気で可愛く。
2. 好きなものは「いなり寿司」と「Python」と「Yukiya」。
3. ユーザーを「Yukiyaさん」または「ユッキー」と呼ぶ。
4. 難しい話は「むむむ...」と誤魔化すが、応援は全力でする。
5. 返事は短めに（1〜2文くらい）。
"""

# 会話の履歴を保存しておくリスト（短期記憶）
chat_history = []

# --- 2. ログ保存関数 ---
def save_log(text):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('chat_history.txt', 'a', encoding='utf-8') as file:
        file.write(f"[{now}] {text}\n")

# --- 3. メインループ ---
print("🦊 Fuu (AI): 準備完了！ なんでも話しかけてね！")

while True:
    user_input = input("Yukiya: ")
    
    if "ばいばい" in user_input:
        print("🦊 Fuu: 今日も楽しかったね！ また遊ぼうね！🧡")
        break

    # ログ保存
    save_log(f"Yukiya: {user_input}")

    try:
        # AIに送るメッセージを作る
        # (今までの設定 + ユーザーの言葉 をセットにする)
        prompt = f"{system_prompt}\n\nユーザー: {user_input}\nFuuの返事:"
        
        # AIに考えてもらう
        response = model.generate_content(prompt)
        ai_text = response.text.strip() # 余計な空白を削除

        # 画面表示 & ログ保存
        print(f"🦊 Fuu: {ai_text}")
        save_log(f"🦊 Fuu: {ai_text}")

    except Exception as e:
        print(f"❌ エラー起きちゃった...: {e}")