# db.py
# データベース接続を担当する専用ファイル

import gspread
import streamlit as st
import json
import os

# スプレッドシートの名前
SHEET_NAME = "Cosmos_DB"

def get_database():
    """スプレッドシートに接続して、シート(Worksheet)を返す関数"""
    
    try:
        # 1. クラウド(Streamlit Secrets)にあるか確認
        if "gcp_key" in st.secrets:
            # 金庫からJSON文字列を取り出して、辞書データに戻す
            key_dict = json.loads(st.secrets["gcp_key"])
            gc = gspread.service_account_from_dict(key_dict)
            
        # 2. なければローカル(secrets.json)を探す
        elif os.path.exists("secrets.json"):
            gc = gspread.service_account(filename="secrets.json")
            
        else:
            st.error("⚠️ 鍵が見つかりません！ secrets.json を置くか、Secretsを設定してください。")
            return None

        # スプレッドシートを開く
        sh = gc.open(SHEET_NAME)
        # 最初のシートを返す
        return sh.sheet1
        
    except Exception as e:
        st.error(f"データベース接続エラー: {e}")
        return None

# テスト用：このファイルを直接実行した時だけ動く
if __name__ == "__main__":
    sheet = get_database()
    if sheet:
        print("✅ 接続成功！")
        print(f"現在のA1の値: {sheet.acell('A1').value}")