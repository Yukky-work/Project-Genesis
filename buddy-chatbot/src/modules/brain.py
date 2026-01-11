# src/modules/brain.py
import os
import google.generativeai as genai
from PIL import Image
import pandas as pd
import sys
import contextlib
from io import StringIO
from dotenv import load_dotenv

# ★グラフ描画用ライブラリ
import matplotlib.pyplot as plt
import japanize_matplotlib # 日本語文字化け対策

# 初期化処理
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
MODEL_NAME = os.getenv("API_MODEL", "gemini-1.5-flash")
model = genai.GenerativeModel(MODEL_NAME)

def execute_python_code(code_str):
    """
    AIが書いたコードを実行し、テキスト結果とグラフ画像(あれば)を返す
    戻り値: (text_result, figure_object)
    """
    # 簡易セキュリティ
    if "os.system" in code_str or "subprocess" in code_str:
        return "【セキュリティ警告】危険なコマンドは実行できません。", None

    output_capture = StringIO()
    created_figure = None

    try:
        # 前のグラフが残っていると重なるのでクリア
        plt.close('all') 
        plt.clf()

        # 標準出力をキャプチャしながら実行
        with contextlib.redirect_stdout(output_capture):
            exec(code_str, globals()) 
        
        result_text = output_capture.getvalue()
        if not result_text:
            result_text = "(実行完了: テキスト出力なし)"

        # ★グラフが描画されたかチェック
        # (AIが plt.plot() などをしていれば、gcf() で現在の図を取得できる)
        if plt.get_fignums():
            created_figure = plt.gcf() # 図形オブジェクトを捕獲
            
        return result_text, created_figure

    except Exception as e:
        return f"実行エラー: {e}", None

def get_gemini_response(prompt, image=None, csv_file=None, audio_bytes=None, system_prompt=""):
    """Geminiに問い合わせる統合関数"""
    
    content_list = [system_prompt]

    # モード別の追加情報
    if csv_file:
        try:
            df = pd.read_csv(csv_file)
            content_list.append(f"【CSVデータ(先頭5行)】\n{df.head().to_markdown()}")
        except: pass
    
    if image:
        content_list.append(Image.open(image))
        
    if audio_bytes:
        content_list.append({"mime_type": "audio/webm", "data": audio_bytes})

    # ユーザーのテキストプロンプト
    content_list.append(f"ユーザー: {prompt}")

    try:
        response = model.generate_content(content_list)
        return response.text
    except Exception as e:
        return f"エラーが発生しました: {e}"