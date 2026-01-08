# read_profile.py
import json

# 1. JSONファイルを開いて読み込む
with open('fuu_profile.json', 'r', encoding='utf-8') as file:
    # json.load() で、ファイルの中身をPythonの「辞書」として読み込む
    fuu_data = json.load(file)

# 2. 読み込んだデータを使ってみる
print("--- 🦊 Fuuの自己紹介 ---")
print(f"名前: {fuu_data['name']}")
print(f"年齢: {fuu_data['age']}歳")
print(f"特徴: {fuu_data['description']}")

# 3. リスト（配列）の中身も取り出せます
print("\n--- ❤️ Fuuの好きなもの ---")
for item in fuu_data['likes']:
    print(f"- {item}")

print("\n---------------------------")