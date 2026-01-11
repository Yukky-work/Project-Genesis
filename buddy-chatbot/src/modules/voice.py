# src/modules/voice.py
import requests
import streamlit as st
from streamlit_mic_recorder import mic_recorder

def get_audio_input(key_index):
    """マイク入力を取得する"""
    return mic_recorder(
        start_prompt="● 録音 (ON)",
        stop_prompt="■ 停止 (OFF)",
        key=f'MIC_{key_index}'
    )

def play_voice(text, speaker_id=2):
    """VOICEVOXで音声を再生する"""
    try:
        # クエリ作成
        res1 = requests.post("http://127.0.0.1:50021/audio_query", params={"text": text, "speaker": speaker_id})
        if res1.status_code != 200: return None
        query = res1.json()
        
        # 音声合成
        res2 = requests.post("http://127.0.0.1:50021/synthesis", json=query, params={"speaker": speaker_id})
        return res2.content
    except:
        return None