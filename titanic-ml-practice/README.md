# 🚢 Project_Genesis: Titanic Survival AI 🔮

[![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/sklearn-RandomForest-F7931E?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

> **"Can AI predict destiny?"**
> 7日間で、Python未経験から構築した機械学習Webアプリケーション。

---

## 📖 Table of Contents (目次)
1. [Overview (概要)](#-overview-概要)
2. [Demo & Features (デモと機能)](#-demo--features-デモと機能)
3. [Architecture & Tech (技術構成)](#-architecture--tech-技術構成)
4. [Data Analysis & Experimentation (分析と実験)](#-data-analysis--experimentation-分析と実験)
5. [Installation (セットアップ)](#-installation-セットアップ)
6. [Roadmap (今後の展望)](#-roadmap-今後の展望)
7. [Team & Author (開発者)](#-team--author-開発者)

---

## 🧐 Overview (概要)
**【課題背景】**
データサイエンスの古典的課題である「タイタニック号の生存予測」を題材に、単なる分析に留まらず、**「誰もが直感的に使えるWebサービス」** へと昇華させることを目的としたプロジェクトです。

**【ソリューション】**
機械学習モデル（Random Forest）をバックエンドに搭載し、Streamlitを用いたインタラクティブなUIを構築。ユーザーは自身の属性を入力するだけで、瞬時に生存確率をシミュレーションできます。

---

## 📸 Demo & Features (デモと機能)

![Demo GIF](./assets/demo.gif)
*(※ここにアプリが動いているGIF動画やスクリーンショットを配置してください)*

* **Real-time Prediction:** スライダー操作に合わせて、推論結果（生存確率）をミリ秒単位で再計算。
* **Dynamic UI:** 生存率が高い場合（>50%）は祝福のエフェクト🎉、低い場合は警告💀を表示。
* **Responsiveness:** PC/スマホ両対応のレスポンシブデザイン。

---

## 🛠 Architecture & Tech (技術構成)

### Directory Structure
```
titanic-ml-practice/
├── app.py              # アプリケーション本体 (Streamlit)
├── titanic_model.pkl   # 学習済みAIモデル (Joblib)
├── requirements.txt    # 依存ライブラリ一覧
├── data/
│   └── train.csv       # 学習用データ
├── notebooks/
│   └── Titanic_Gemini.ipynb  # データ分析・モデル構築の過程 (Jupyter)
└── README.md           # This file
```
---

### Technology Stack
* **Language:** Python 3.10
* **Framework:** Streamlit (Frontend & Backend)
* **ML Libraries:** Scikit-learn (Random Forest), Pandas, NumPy
* **Environment:** Google Colab (Development), Local (Deployment)

---

## 🧪 Data Analysis & Experimentation (分析と実験)
**Luna's Point (ビジネスインサイト):**
モデル構築の過程で、以下のファクトが判明しました。
* **"Money Matters":** 運賃($)が高い乗客ほど生存率が著しく高い。
* **"Lady First":** 男性より女性の生存率が圧倒的に高い。

**Gem Py's Point (技術的検証):**
* **Model Selection:** 決定木(Decision Tree)では過学習が見られたため、**Random Forest** を採用。
* **Hyperparameter Tuning:** GridSearchを用いて最適化を実施。
    * `n_estimators`: 10 (軽量化のため最小構成を採用)
    * `max_depth`: 5 (汎化性能を重視)
* **Result:** Test Accuracy **82.46%** を達成。

---

## 💻 Installation (セットアップ)
あなたのローカル環境でこのアプリを動かす手順です。

1. **Clone the repo**
   ```
   git clone [https://github.com/YourUsername/Project_Genesis.git](https://github.com/YourUsername/Project_Genesis.git)
   ```
   ```
   cd Project_Genesis2. Install dependencies
   ```
   ```
   pip install -r requirements.txt
   ```
3. **Run the app**
   ```
    streamlit run app.py
   ```

## 🗺️ Roadmap (今後の展望)
私は **Cloud & AI Engineer** としてのキャリア構築を目指し、現在はGoogle Cloudエコシステムを中心とした技術習得に取り組んでいます。

| Phase | Focus Area | Key Milestones |
| :--- | :--- | :--- |
| **Q1 2026** | **Foundation** | ・**Kaggle Start** (データ分析の実践)<br>・**Cloud Digital Leader** 取得 (クラウド基礎) |
| **Q2 2026** | **Development** | ・**Associate Cloud Engineer** 取得<br>・Pythonによる実用アプリケーション開発 |
| **Q3 2026** | **Challenge** | ・**Kaggle Medalist (Bronze)** 🥉 獲得<br>・Generative AI (LLM) の活用 |
| **Q4 2026** | **Professional** | ・**Professional Data Engineer** 取得<br>・大規模データ基盤の設計・構築スキルの習得 |

## 🤝 Team & Author (開発者)

**Lead Developer: Yukky**
* **Cloud & AI Engineer** (Aspiring)
* Focus: Python, Google Cloud, Generative AI
* [GitHub Profile](https://github.com/) | [LinkedIn](https://www.linkedin.com/in/yukiya-nishiyama-37b7aa3a1)

**Co-Developed with Team Genesis (AI Agents):**
* **Gemini** (Project Manager)
* **Gem Py** (Tech Lead)
* **Fuu** (UX Designer & Mood Maker)
* **Luna** (Business Manager)
* **Rikka** (Ops & Database)
* **Shiori** (Wellness Mentor)

---

*© 2025 Project_Genesis. Released under the [MIT License](./LICENSE).*

