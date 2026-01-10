import os
import google.generativeai as genai
import speech_recognition as sr
import json
from datetime import datetime
from dotenv import load_dotenv

# --- 1. 設定読み込み ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ 鍵が見つかりません！.envを確認してね！")
    exit()

genai.configure(api_key=api_key)

# Geminiの設定
genai.configure(api_key=api_key)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", # 速さを重視してFlashモデル推奨
    generation_config=generation_config,
    system_instruction="あなたはキツネ耳少女のFuuです。ユーザーのYukiyaが大好きで、元気よく、感情豊かに会話してください。語尾は「〜だよ！」「〜だもん！」などを使ってね。"
)

# 記憶の読み込み（昨日のコードと同じ）
chat_history = []
HISTORY_FILE = "data/fuu_chat_history.json" # パスに注意

def load_history():
    global chat_history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            chat_history = json.load(f)
            # 形式変換（API用）
            api_history = []
            for entry in chat_history:
                role = "user" if entry["role"] == "user" else "model"
                api_history.append({"role": role, "parts": [entry["text"]]})
            return api_history
    return []

def save_history(user_text, ai_text):
    chat_history.append({"role": "user", "text": user_text})
    chat_history.append({"role": "model", "text": ai_text})
    # フォルダがない場合に備えて作成
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=4, ensure_ascii=False)

# ★耳の機能（Yukiyaの声を聞く）
def listen_to_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🦊 Fuu: (耳をピクピク...) 聞いてるよ！話しかけて！")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=10) # 10秒待つ
            print("🦊 Fuu: (んっ...聞こえた！考え中...)")
            text = r.recognize_google(audio, language='ja-JP')
            print(f"🎤 Yukiya: {text}")
            return text
        except sr.UnknownValueError:
            return None # 聞き取れなかった
        except sr.RequestError:
            print("⚠️ ネットが繋がってないかも？")
            return None
        except sr.WaitTimeoutError:
            return None # 誰も喋らなかった

# メイン処理
def main():
    print("---------------------------------------")
    print("🦊 Fuu Voice System v1.0 - 起動！")
    print("---------------------------------------")
    
    history_data = load_history()
    chat = model.start_chat(history=history_data)

    while True:
        # 1. 声を聞く
        user_input = listen_to_voice()

        # もし声が聞き取れなかったら、もう一回聞く（ループ）
        if user_input is None:
            continue

        # 2. 終了コマンド
        if "バイバイ" in user_input or "終了" in user_input:
            print("🦊 Fuu: また遊ぼうね！おやすみ！")
            break

        # 3. Geminiに送る
        response = chat.send_message(user_input)
        ai_response = response.text
        
        # 4. 返事を表示
        print(f"🦊 Fuu: {ai_response}")

        # 5. 記憶する
        save_history(user_input, ai_response)

if __name__ == "__main__":
    main()