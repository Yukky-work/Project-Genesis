# memory_test.py

# 1. ファイルを開く（日記帳を用意する）
# 'w' は "Write（書き込み）" モード
# encoding='utf-8' は、日本語が文字化けしないようにするおまじない
with open('fuu_diary.txt', 'w', encoding='utf-8') as file:
    # 2. ファイルに書き込む（ペンで書く）
    file.write('2026-01-05: 今日はYukiyaとお勉強したよ！\n')
    file.write('FuuはPythonで日記が書けるようになった！えへへ！')

# 3. 完了メッセージ
print("日記の書き込みが完了しました！")