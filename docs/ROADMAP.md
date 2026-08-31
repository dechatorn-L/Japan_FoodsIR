# 🗺️ Product Roadmap & Engineering Vision

This document tracks completed milestones and outlines the strategic development plan for the **Japanese Foods Information Retrieval System**.

---

## 🎯 Completed Milestones (v1.0 & v1.5)

### Phase 1: Core IR Foundations & Data Pipeline ✅
- [x] Multi-source crawler for Cookpad and authentic Japanese catalog.
- [x] Custom culinary domain stopword filtering and lemmatization.
- [x] TF-IDF Vector Space Model with title weighting ($6\times$).
- [x] Dynamic Query Expansion via Pseudo-Relevance Feedback (PRF).
- [x] K-Means Clustering ($K=6$) and 2D PCA projection with Centroid markers.
- [x] Inverted Index construction with postings list lookup.
- [x] Quantitative IR Evaluation suite ($P@K, R@K, AP, MAP$).

### Phase 2: User Experience, Bilingual Localization & Design System ✅
- [x] Complete Bilingual Localization (Thai 🇹🇭 / English 🇬🇧) with dynamic DOM switching.
- [x] 2-Tier App Header architecture eliminating all button and tab collisions.
- [x] Zen Minimalist UI design with dark/light themes.
- [x] One-click pantry presets and ingredient overlap scoring.
- [x] Quick category filter chips (Ramen, Curry, Meat, Donburi, Tofu, Dessert).
- [x] Educational IR Concept tooltips explaining IR mathematics.

### Phase 3: Fault-Tolerance & Enterprise Reliability ✅
- [x] Self-healing dataset regenerator for missing/corrupted CSV files.
- [x] Built-in regex and offline stopwords fallback for restricted environments.
- [x] Dynamic server port hunting (auto-resolves port 8000 conflicts).
- [x] Substring and token matching fallback for unseen queries with zero cosine similarity.
- [x] Safe clipboard and local storage wrappers for strict browser privacy modes.

---

## 🚀 Future Milestones (v2.0+)

### Phase 4: Dense Vector Search & Hybrid Retrieval
- [ ] **Dense Neural Embeddings**: Integrate Sentence-Transformers (`all-MiniLM-L6-v2` or `multilingual-e5-small`) for semantic matching.
- [ ] **Reciprocal Rank Fusion (RRF)**: Combine sparse TF-IDF and dense vector scores:
  $$\text{RRF}(d) = \sum_{m \in \{\text{TF-IDF}, \text{Dense}\}} \frac{1}{60 + \text{rank}_m(d)}$$
- [ ] **Embedded Vector DB**: Support Qdrant / ChromaDB for sub-millisecond retrieval on large-scale datasets.

### Phase 5: Generative AI Culinary Assistant
- [ ] **Smart Recipe Modifications**: LLM-assisted ingredient substitutions (e.g. halal, vegetarian, low-sodium alternatives).
- [ ] **Step-by-Step Cooking Guide**: Dynamic cooking instructions generated from ingredient lists.
- [ ] **Chat with Japanese Chef**: Conversational recipe recommendations.

### Phase 6: Multi-Modal Visual Recipe Recognition
- [ ] **Photo-to-Recipe Search**: Upload a photo of a Japanese dish to retrieve its recipe and ingredients via computer vision.
- [ ] **Nutritional Analysis**: Automatic calorie and macronutrient estimation for retrieved recipes.
