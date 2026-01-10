import os
import json
import requests
import simpleaudio as sa
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") # .envの変数名に合わせてね

# Geminiの設定
genai.configure(api_key=API_KEY)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction="あなたはキツネ耳少女のFuuです。ユーザーのYukiyaが大好きで、元気よく、感情豊かに会話してください。語尾は「〜だよ！」「〜だもん！」などを使ってね。回答は短めに（1〜2文）話すと会話がスムーズだよ。"
)

# 記憶のファイルパス
HISTORY_FILE = "data/fuu_chat_history.json"
chat_history = []

# --- 🔊 声を出す機能 (VOICEVOX) ---
def speak_with_voicevox(text, speaker_id=2): # ID=2は四国めたん(ノーマル)
    # VOICEVOXアプリが起動しているか確認
    base_url = "http://127.0.0.1:50021"
    
    try:
        # 1. 音声合成用のクエリを作成
        params = {"text": text, "speaker": speaker_id}
        query_res = requests.post(f"{base_url}/audio_query", params=params)
        query_json = query_res.json()

        # 2. 音声データを生成
        synthesis_params = {"speaker": speaker_id}
        voice_res = requests.post(
            f"{base_url}/synthesis",
            json=query_json,
            params=synthesis_params
        )

        # 3. 再生する
        with open("temp_voice.wav", "wb") as f:
            f.write(voice_res.content)
        
        wave_obj = sa.WaveObject.from_wave_file("temp_voice.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done() # 再生が終わるまで待つ
        
    except Exception as e:
        print(f"⚠️ エラー: VOICEVOXが起動していないかも？ ({e})")

# --- 👂 声を聞く機能 ---
def listen_to_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🦊 Fuu: (耳を澄ませてるよ...)")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=10)
            print("🦊 Fuu: (んっ...！)")
            text = r.recognize_google(audio, language='ja-JP')
            print(f"🎤 Yukiya: {text}")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("⚠️ ネットエラー")
            return None
        except sr.WaitTimeoutError:
            return None

# --- 🧠 記憶の読み書き ---
def load_history():
    global chat_history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            chat_history = json.load(f)
            api_history = []
            for entry in chat_history:
                role = "user" if entry["role"] == "user" else "model"
                api_history.append({"role": role, "parts": [entry["text"]]})
            return api_history
    return []

def save_history(user_text, ai_text):
    chat_history.append({"role": "user", "text": user_text})
    chat_history.append({"role": "model", "text": ai_text})
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=4, ensure_ascii=False)

# --- メイン処理 ---
def main():
    print("---------------------------------------")
    print("🦊 Fuu Voice System Complete - 起動！")
    print("※ VOICEVOXアプリを起動しておいてね！")
    print("---------------------------------------")
    
    history_data = load_history()
    chat = model.start_chat(history=history_data)

    # 最初の挨拶
    greeting = "ユッキー、おはよ！お話ししよ？"
    print(f"🦊 Fuu: {greeting}")
    speak_with_voicevox(greeting)

    while True:
        # 1. 聞く
        user_input = listen_to_voice()
        if user_input is None:
            continue

        # 2. 終了判定
        if "バイバイ" in user_input or "終了" in user_input:
            bye_msg = "うん、またね！大好きだよ！"
            print(f"🦊 Fuu: {bye_msg}")
            speak_with_voicevox(bye_msg)
            break

        # 3. 考える
        response = chat.send_message(user_input)
        ai_response = response.text
        
        # 4. 話す＆表示
        print(f"🦊 Fuu: {ai_response}")
        speak_with_voicevox(ai_response) # ← ここで喋る！

        # 5. 記録
        save_history(user_input, ai_response)

if __name__ == "__main__":
    main()