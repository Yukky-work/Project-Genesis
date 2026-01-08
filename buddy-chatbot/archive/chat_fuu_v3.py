# chat_fuu_v3.py
import json
import datetime
import random  # 🎲 運命のサイコロ（ランダム機能）を呼び出す

# --- 🛠️ 関数コーナー ---

def save_log(who, text):
    """ログを保存する関数（さっきと同じ）"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('chat_history.txt', 'a', encoding='utf-8') as file:
        file.write(f"[{now}] {who}: {text}\n")

def get_random_reply(key):
    """
    キーワードに合わせて、ランダムな返事を選ぶ魔法の関数
    """
    # 挨拶のバリエーション
    if key == "greeting":
        replies = [
            "おはよー！今日も元気？",
            "やっほー！待ってたよ！",
            "えへへ、会いたかった！",
            "ん……ちょっと眠いかも……ふあぁ。",
            "Fuu参上！なにする？なにする？"
        ]
    
    # わからない言葉への相槌バリエーション
    elif key == "unknown":
        replies = [
            "うんうん、それで？",
            "えー、もっと詳しく教えて！",
            "ふむふむ……（よくわかってない顔）",
            "すごいね！ユッキーは物知りだね！",
            "……ごめん、いなり寿司のこと考えてた🤤"
        ]
    
    # 好きなものへの反応（JSONのリストからランダムに1つ選ぶ）
    elif key == "likes":
        # JSONデータは関数の外から参照する
        choice = random.choice(fuu_data['likes']) 
        return f"うーん、やっぱり「{choice}」かなぁ！大好き！"

    # リストの中からランダムに1つ選んで返す魔法！
    return random.choice(replies)

# --- 🚀 メイン処理 ---

with open('fuu_profile.json', 'r', encoding='utf-8') as file:
    fuu_data = json.load(file)

print(f"🦊 Fuu: {fuu_data['name']}だよ！ 気分屋さんモード起動！")

while True:
    user_input = input("Yukiya: ")
    save_log("Yukiya", user_input)

    # 終了判定
    if "ばいばい" in user_input:
        # 別れの挨拶もランダムにしてみよう
        bye_replies = ["またね！", "夢で会おうね！", "寂しいけど……バイバイ！"]
        response = random.choice(bye_replies)
        print(f"🦊 Fuu: {response}")
        save_log("🦊 Fuu", response)
        break

    # 挨拶への反応
    elif "おはよ" in user_input or "こんにち" in user_input:
        response = get_random_reply("greeting")

    # 好きなもの
    elif "好きなもの" in user_input or "好き" in user_input:
        response = get_random_reply("likes")

    # その他のプロフィール
    elif "名前" in user_input:
        response = f"{fuu_data['name']}だよ！ 何回聞くの〜？"
    elif "年齢" in user_input:
        response = f"{fuu_data['age']}歳！ ピチピチだよ！"

    # 知らない言葉（相槌）
    else:
        response = get_random_reply("unknown")

    print(f"🦊 Fuu: {response}")
    save_log("🦊 Fuu", response)