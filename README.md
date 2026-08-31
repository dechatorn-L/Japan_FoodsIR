# 🍣 Japanese Foods Information Retrieval (IR) & Culinary Engine
> **日本料理 情報検索システム** &middot; Intelligent Recipe Search, Vector Space Modeling (VSM), TF-IDF, Pseudo-Relevance Feedback (Query Expansion), K-Means Clustering, 2D PCA Visualization, Bilingual UI (TH/EN), and Fault-Tolerant Data Pipeline.

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4%2B-orange.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![NLTK](https://img.shields.io/badge/NLTK-NLP-green.svg)](https://www.nltk.org)
[![UI](https://img.shields.io/badge/Frontend-Zen%20Minimalist%20Bilingual-pink.svg)](./web)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

## 📌 1. Project Overview

The **Japanese Foods Information Retrieval System** is an end-to-end NLP & IR framework designed to crawl, preprocess, index, cluster, and retrieve Japanese culinary recipes with high relevance and semantic interpretability.

Originally developed as an Information Retrieval (IR) academic project, this repository has been modernized with a modular architecture, bilingual localization (Thai 🇹🇭 / English 🇬🇧), 2-tier header UX, interactive pantry matcher, educational IR tooltips, and a self-healing fault-tolerant data pipeline.

```
       [ Multi-Source Ingestion & Crawler ] ───> (Cookpad + Fallback Authentic Catalog)
                       │
                       ▼
          [ Text Preprocessing & NLP ]      ───> (NLTK + Regex Fallback + Culinary Stopwords)
                       │
                       ▼
           [ TF-IDF Vector Space Model ]    ───> (Title 6x Boost + Cleaned Ingredients)
                       │
             ┌─────────┴─────────────────────────┐
             ▼                                   ▼
    [ Inverted Index & VSM ]            [ K-Means (K=6) + 2D PCA ]
             │                                   │
             ▼                                   ▼
   [ Pseudo-Relevance Feedback ]        [ Interactive Food Scatter Map ]
   (Dynamic Query Expansion)
             │
             ▼
   [ Ranking & Retrieval Engine ] ──────> [ Web App / Streamlit / CLI / REST API ]
```

---

## ✨ 2. Key Features

- **🔍 Vector Space Model (VSM) & TF-IDF Retrieval**: Computes cosine similarities between weighted query vectors and document term vectors. Title weighting multiplier ($6\times$) ensures dishes matching search titles rank prominently.
- **⚡ Pseudo-Relevance Feedback (Dynamic Query Expansion)**: Automatically detects co-occurring culinary concepts in the top-10 candidate matches to dynamically expand user queries (e.g. `chicken` $\rightarrow$ `chicken sauce renkon ginger egg`).
- **🌐 Bilingual Localization (Thai 🇹🇭 / English 🇬🇧)**: Instant client-side language switching across all 6 tabs, modal dialogs, placeholders, and educational tooltips with `localStorage` state persistence.
- **🍱 Pantry / Fridge Matcher ("Cook with What You Have")**: Matches available ingredients in the kitchen with one-click presets (*Noodle Night, Izakaya Skewers, Comfort Curry, Healthy Tofu, Bento Box*) and displays exact missing ingredient lists.
- **🍜 Quick Category Chips**: One-click category filtering for *Ramen & Noodles, Curry & Stews, Yakitori & Meat, Donburi Rice Bowls, Tofu & Salads, and Matcha Desserts*.
- **📊 K-Means Clustering ($K=6$) & 2D PCA Map**: Groups 100 recipes into 6 distinct culinary clusters and projects them in 2D space with Centroids (`✖`).
- **📖 Inverted Index Vocabulary Inspector**: Real-time inspection of Document Frequency (DF) and postings lists with fuzzy suggestions for misspelled terms.
- **📈 IR Evaluation Dashboard**: Quantitative calculation of standard IR metrics ($P@K$, $Recall@K$, $AP$, and session $MAP$) alongside True Positive, False Positive, and False Negative counts.
- **⚙️ Live Web Scraper & Pipeline Management**: On-demand web scraping from Cookpad / Culinary APIs with real-time log polling and hot-reload.
- **🛡️ Full-Stack Fault-Tolerance & Fallbacks**: Self-healing dataset recovery, offline NLTK tokenizers, port conflict auto-resolution, and safe clipboard handling.

---

## 📐 3. Mathematical Foundations

### 3.1 Term Frequency - Inverse Document Frequency (TF-IDF)
For a term $t$ in document $d$ within a corpus of $N$ documents:

$$\text{TF}(t, d) = \frac{f_{t, d}}{\sum_{t' \in d} f_{t', d}}$$

$$\text{IDF}(t, D) = \ln \left( \frac{1 + N}{1 + \text{DF}(t)} \right) + 1$$

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

### 3.2 Cosine Similarity Ranking
Document relevance to a query vector $\vec{q}$ is computed using cosine similarity:

$$\text{Cosine Similarity}(\vec{q}, \vec{d}) = \frac{\vec{q} \cdot \vec{d}}{\|\vec{q}\|_2 \|\vec{d}\|_2} = \frac{\sum_{i=1}^{V} q_i d_i}{\sqrt{\sum_{i=1}^{V} q_i^2} \sqrt{\sum_{i=1}^{V} d_i^2}}$$

### 3.3 Dynamic Query Expansion (Pseudo-Relevance Feedback)
Given initial query $\vec{q}$, retrieve top $M$ documents ($M=10$). The term frequency distribution across $M$ is evaluated:

$$\text{freq}(w) = \sum_{d \in \text{Top-}M} c(w, d), \quad \forall w \notin \vec{q}$$

Terms satisfying dynamic threshold $\text{freq}(w) \ge \max_{w'} \text{freq}(w')$ and length $> 1$ are appended:

$$\vec{q}_{\text{expanded}} = \vec{q} \cup \{w_1, w_2, \dots, w_k\}$$

### 3.4 K-Means Clustering Objective
Partitions the $N$ recipes into $K=6$ clusters $S = \{S_1, S_2, \dots, S_K\}$ minimizing intra-cluster variance:

$$\arg\min_{S} \sum_{i=1}^{K} \sum_{\vec{x} \in S_i} \|\vec{x} - \boldsymbol{\mu}_i\|^2$$

### 3.5 Evaluation Metrics ($P@K, R@K, AP, MAP$)
- **Precision at Rank $K$**:
  $$P@K = \frac{|\text{Retrieved}_K \cap \text{Relevant}|}{K}$$

- **Recall at Rank $K$**:
  $$R@K = \frac{|\text{Retrieved}_K \cap \text{Relevant}|}{|\text{Relevant}|}$$

- **Average Precision ($AP$)**:
  $$AP = \frac{1}{|\text{Relevant}|} \sum_{k=1}^{|\text{Retrieved}|} P@k \times \text{rel}(k)$$

- **Mean Average Precision ($MAP$)**:
  $$MAP = \frac{1}{|Q|} \sum_{q=1}^{|Q|} AP(q)$$

---

## 🗂️ 4. Directory Structure

```
Japanese_Foods_IR-main/
├── app_streamlit.py       # Streamlit Interactive Dashboard
├── server.py              # Production Web Server Entrypoint
├── engine.py              # Legacy Engine Backward Compatibility
├── requirements.txt       # Python Project Dependencies
│
├── src/                   # Modular Source Code
│   ├── engine.py          # Unified Core IR Engine (VSM, PRF, K-Means, Inverted Index)
│   ├── default_data.py    # Curated 100 Authentic Japanese Recipes & Self-Healing Generator
│   ├── crawler/           # Multi-Source Crawler & Recipe Extractor
│   │   ├── url_scraper.py
│   │   └── recipe_scraper.py
│   ├── preprocessing/     # NLP Cleaning & Domain Stopwords
│   │   └── text_cleaner.py
│   ├── modeling/          # VSM & Evaluation CLI Tools
│   └── web/               # Embedded HTTP Server & REST API Handlers
│       └── server.py
│
├── web/                   # Zen Minimalist Frontend (Zero Build Step)
│   ├── index.html         # 2-Tier Header, Bilingual DOM & Responsive Layout
│   ├── style.css          # Zen Kyoto Minimalist Styling & CSS Variables
│   └── app.js             # Client-side i18n, Chart.js Controller & Event Handlers
│
├── data/                  # Data Storage
│   ├── raw/               # Raw Scraped CSVs
│   └── processed/         # Cleaned Corpus (Japan_Food_Ingredients_Cleaned.csv)
│
├── docs/                  # Project Documentation
│   ├── INDEX.md           # Documentation Hub
│   ├── ARCHITECTURE.md    # Architecture & Data Flow
│   ├── SPECIFICATION.md   # System Specifications & REST Contracts
│   ├── STYLE_GUIDE.md     # UI Design System & Component Specs
│   └── ROADMAP.md         # Future Plans
│
└── .agents/               # Agent Customizations & Skills
    ├── rules/
    │   └── style.md       # Concise Style Rule
    └── skills/
        └── food_IR/
            └── SKILL.md   # Japanese Foods IR Skill Definition
```

---

## 🚀 5. Quick Start & Execution

### 5.1 Installation
```powershell
# Clone repository
git clone https://github.com/your-org/Japanese_Foods_IR.git
cd Japanese_Foods_IR-main

# Install dependencies
pip install -r requirements.txt
```

### 5.2 Running the Modern Web Interface (Recommended)
```powershell
python server.py --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your web browser.

### 5.3 Running the Streamlit Dashboard
```powershell
streamlit run app_streamlit.py
```

### 5.4 Running the Terminal CLI
```powershell
python Model/VSM.py
```

---

## 📜 6. License
Distributed under the MIT License. Built for Information Retrieval & Natural Language Processing.
