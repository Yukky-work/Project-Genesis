# read_test.py

# 1. ファイルを開く（今度は 'r' = Read 読み込みモード）
# 書き込み時は 'w' でしたが、読むときは 'r' を使います
with open('fuu_diary.txt', 'r', encoding='utf-8') as file:
    # 2. 中身を全部読み込んで、変数 'content' に入れる
    content = file.read()

# 3. 読み込んだ内容を画面に表示する
print("--- 📖 Fuuの日記を開きます ---")
print(content)
print("-------------------------------")