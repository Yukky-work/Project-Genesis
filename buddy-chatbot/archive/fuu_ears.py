import speech_recognition as sr

def listen_to_yukiya():
    # マイクの準備（耳を澄ます）
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("🦊 Fuu: 耳を澄ませています...（話しかけてね！）")
        # 周囲の雑音を少し調整
        r.adjust_for_ambient_noise(source)
        # 音声を録音
        audio = r.listen(source)

    try:
        print("🦊 Fuu: ...（考え中）...")
        # Googleの音声認識を使って文字に変換
        text = r.recognize_google(audio, language='ja-JP')
        print(f"🎤 Yukiya: {text}")
        return text
        
    except sr.UnknownValueError:
        print("🦊 Fuu: ごめんね、よく聞き取れなかったよ...")
        return None
    except sr.RequestError:
        print("🦊 Fuu: インターネットが繋がってないみたい...")
        return None

# テスト実行
if __name__ == "__main__":
    while True:
        user_voice = listen_to_yukiya()
        if user_voice == "バイバイ":
            print("🦊 Fuu: またねー！")
            break