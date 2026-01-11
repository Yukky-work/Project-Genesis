# main.py
# 宇宙の歴史を積み上げる「追記モード」実装版

import os  # ファイル操作用モジュール
import pandas as pd
import config
import star_generator

# CSVファイルの名前を定数にしておく（ミス防止）
CSV_FILE = "cosmos_db.csv"

def main():
    print("=== 🌌 Galaxy Server Cosmos: Expansion Start ===")

    # 1. 既存の宇宙があるかチェック (Load)
    if os.path.exists(CSV_FILE):
        print("📂 既存の宇宙データを発見。読み込みます...")
        existing_df = pd.read_csv(CSV_FILE)
        
        # 最後に発行されたIDを取得する
        # (データが空の場合のエラー処理も軽く入れておく)
        if len(existing_df) > 0:
            last_id = existing_df['id'].max()
        else:
            last_id = 0
            
        print(f"🔄 現在の星の数: {len(existing_df)} 個 (Last ID: {last_id})")
        
    else:
        print("✨ 新規宇宙を作成します。")
        existing_df = pd.DataFrame() # 空っぽの表を作る
        last_id = 0

    # 2. 新しい星を生成 (Generate)
    new_stars_data = []
    
    # スタート地点は「最後のID + 1」から！
    start_id = last_id + 1
    end_id = start_id + config.STAR_COUNT
    
    print(f"⚡ 新たに {config.STAR_COUNT} 個の星を生成中 (ID: {start_id} ～ {end_id - 1})...")

    # range(開始, 終了) を使う
    for i in range(start_id, end_id):
        my_star = star_generator.create_star(i)
        new_stars_data.append(my_star)

    # 新しいデータのDataFrame化
    new_df = pd.DataFrame(new_stars_data)

    # 3. 新旧データの結合 (Merge)
    if not existing_df.empty:
        # pd.concatで縦に結合 (ignore_index=Trueで綺麗に繋ぐ)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    # 4. 結果表示 & 保存 (Save)
    print("\n------- 🔭 現在の全宇宙データ (最新5件のみ表示) -------")
    print(updated_df.tail(5)) # tail(5)は「後ろから5件」だけ表示する機能
    print(f"   (Total: {len(updated_df)} Stars)")
    print("-------------------------------------------------------")

    updated_df.to_csv(CSV_FILE, index=False, encoding="utf-8")
    print(f"\n💾 宇宙を拡張し、'{CSV_FILE}' を更新しました！")

    print("\n=== 🌌 Expansion Complete ===")

if __name__ == "__main__":
    main()