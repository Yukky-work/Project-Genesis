# chat_fuu_v2.py
import json
import datetime # 🕑 日付と時刻を扱うための魔法

# --- 🛠️ 便利な関数（道具）コーナー ---

def save_log(who, text):
    """
    会話をファイルに記録する関数です。
    who: 誰が話したか (例: "Yukiya", "🦊 Fuu")
    text: 話した内容
    """
    # 現在時刻を取得 (例: 2026-01-05 15:30:00)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # ファイルを 'a' (Append = 追記) モードで開く
    with open('chat_history.txt', 'a', encoding='utf-8') as file:
        file.write(f"[{now}] {who}: {text}\n")

# --- 🚀 メイン処理コーナー ---

# 1. Fuuのプロフィール読み込み
with open('fuu_profile.json', 'r', encoding='utf-8') as file:
    fuu_data = json.load(file)

print(f"🦊 Fuu: {fuu_data['name']}だよ！ ログ機能がついたよ！")

# 2. 無限ループで会話開始
while True:
    # ユーザーの入力を受け取る
    user_input = input("Yukiya: ")
    
    # ★ ここでユーザーの発言を記録！
    save_log("Yukiya", user_input)

    # 終了判定
    if "ばいばい" in user_input:
        response = "またね！ログに残ってるから忘れないよ！🧡"
        print(f"🦊 Fuu: {response}")
        save_log("🦊 Fuu", response) # Fuuの別れの言葉も記録
        break

    # 返事を作るロジック
    elif "好きなもの" in user_input or "好き" in user_input:
        likes = "、".join(fuu_data['likes'])
        response = f"Fuuが好きなのはね…… {likes} だよ！えへへ。"
    
    elif "名前" in user_input:
        response = f"{fuu_data['name']}だよ！ 忘れちゃったの？"

    elif "年齢" in user_input:
        response = f"永遠の{fuu_data['age']}歳だよ！"

    else:
        response = "うんうん、それでそれで？"

    # 画面に表示 ＆ ★ Fuuの返事を記録！
    print(f"🦊 Fuu: {response}")
    save_log("🦊 Fuu", response)