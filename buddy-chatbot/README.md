# 🦊 AI Partner "Fuu" (Multi-Modal Assistant)

**Personal AI Assistant System built with Python, Gemini API, and Streamlit.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Gemini API](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-orange?style=for-the-badge&logo=google)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge&logo=streamlit)
![VOICEVOX](https://img.shields.io/badge/VOICEVOX-TTS-green?style=for-the-badge)

## 📖 Overview (概要)
**"Fuu"** は、生成AI (Google Gemini 1.5 Flash) を活用した、多機能なパーソナルAIアシスタントです。
単なるテキストチャットに留まらず、**「音声会話」「視覚（画像認識）」「人格の切り替え」** を実装し、ユーザーに寄り添うパートナーとして開発しました。
レガシーな開発環境から脱却し、最新のLLM技術をキャッチアップするために個人開発を行っています。

## ✨ Key Features (主な機能)

### 1. 🗣️ Voice Interaction (音声対話)
* **TTS (Text-to-Speech):** VOICEVOX エンジンと連携し、AIの回答を「キャラクターボイス（四国めたん等）」でリアルタイムに再生。
* **Web Playback:** Streamlit上で音声プレイヤーを自動起動し、ブラウザベースでの音声会話を実現。

### 2. 👁️ Computer Vision (視覚機能)
* **Image Analysis:** ユーザーがアップロードした画像を Gemini 1.5 Flash Vision で解析。
* **Contextual Response:** 「これ何？」「見て！」といった問いかけに対し、画像の状況（色、物体、雰囲気）を理解してコメントします。

### 3. 👥 Multi-Agent System (チーム開発モード)
* **Persona Switching:** サイドバーから担当AIを切り替え可能。
    * 🦊 **Fuu:** 元気な盛り上げ役 (メインパートナー)
    * 🔖 **Shiori:** 癒やし担当 (天然・文学少女)
    * 🐍 **Gem Py:** 技術担当 (論理的Pythonアドバイザー)
    * 🌙 **Luna:** マネージャー (キャリア相談)
* **Individual Memory:** キャラクターごとに会話履歴（Context）を分離して管理。

### 4. 🖥️ Modern Web UI
* **Streamlit:** PythonのみでインタラクティブなチャットUIを構築。
* **Responsiveness:** PC/スマホどちらでも閲覧可能なレスポンシブデザイン。

## 🛠️ Tech Stack (使用技術)

* **Language:** Python 3.11
* **LLM:** Google Gemini 1.5 Flash (via `google-generativeai`)
* **Frontend:** Streamlit
* **Audio:** VOICEVOX (Local Server), `requests`
* **Image Processing:** Pillow (PIL)
* **Environment:** `.env` for API Key management

## 🚀 Future Roadmap (今後の展望)

本プロジェクトは現在進行系で開発中です。SCSK様での業務を見据え、以下の機能拡張を計画しています。

* **Emotional Voice Control:** AIの感情分析結果に基づき、VOICEVOXのパラメータ（抑揚・ピッチ）を動的に変化させる。
* **Autonomous Agent:** ユーザーの呼びかけを待つだけでなく、スケジュールや時間帯をトリガーにAIから自発的に話しかける機能の実装。
* **RAG (Retrieval-Augmented Generation):** 独自のドキュメント（技術書や日記）を読み込ませ、より個人的な文脈に沿った回答生成。

## 👤 Author
**Yukiya Nishiyama**
* **Goal:** 生成AI技術を活用し、SI業務の変革・効率化を推進するエンジニアを目指しています。
* **Note:** 本リポジトリは個人学習およびPoCの一環として作成されました。