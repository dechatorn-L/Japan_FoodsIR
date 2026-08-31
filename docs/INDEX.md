# 📚 Japanese Foods IR - Documentation Index

Welcome to the comprehensive technical documentation for the **Japanese Foods Information Retrieval (IR) System**.

```
docs/
├── INDEX.md           # Documentation Hub & Navigation
├── ARCHITECTURE.md    # System Architecture, IR Algorithms, and Data Pipeline
├── SPECIFICATION.md   # Functional Specs, Data Schemas, and API Contracts
├── STYLE_GUIDE.md     # UI/UX Design System, Color Tokens, and Components
└── ROADMAP.md         # Future Feature Expansions, AI Integrations, and Scaling
```

---

## 📑 Documentation Index

### 1. [System Architecture (`ARCHITECTURE.md`)](file:///c:/Projects/Japanese_Foods_IR-main/docs/ARCHITECTURE.md)
Detailed walkthrough of the IR pipeline:
- Web scraping & raw recipe extraction
- NLTK preprocessing & culinary stopword removal
- TF-IDF Vector Space Model & title weighting
- Inverted Index construction (DF + Postings)
- Pseudo-Relevance Feedback (Dynamic Query Expansion)
- K-Means Clustering ($K=6$) & 2D PCA Dimensionality Reduction
- Component interaction & REST API architecture

### 2. [System Specifications (`SPECIFICATION.md`)](file:///c:/Projects/Japanese_Foods_IR-main/docs/SPECIFICATION.md)
Formal specifications and contracts:
- Functional & Non-Functional Requirements
- Dataset Schemas (`Cleaned`, `Full`, `Links`)
- REST API Endpoints, Parameters, and JSON Responses
- IR Performance Metrics ($P@K, R@K, AP, MAP$) and Acceptance Criteria

### 3. [Design System & Style Guide (`STYLE_GUIDE.md`)](file:///c:/Projects/Japanese_Foods_IR-main/docs/STYLE_GUIDE.md)
Frontend design tokens and aesthetics:
- Culinary Color Palette (Crimson, Sakura, Matcha, Nori, Amber)
- Dark & Light Mode Theme Tokens
- Typography hierarchy (`Plus Jakarta Sans`, `Noto Serif JP`, `JetBrains Mono`)
- Glassmorphism & UI Component Guidelines
- Chart.js Styling and Responsive Breakpoints

### 4. [Roadmap & Feature Expansion Plan (`ROADMAP.md`)](file:///c:/Projects/Japanese_Foods_IR-main/docs/ROADMAP.md)
Strategic plan for future scaling and enhancements:
- Hybrid Search (TF-IDF + Dense Vector Embeddings / Qdrant)
- Generative AI Chef Assistant (Gemini API Integration)
- Multilingual Translation Engine (TH / EN / JA)
- Multi-Modal Visual Recipe Search (Food Photo $\rightarrow$ Recipe)
- Automated Nutritional Analysis & Shopping List Generator
