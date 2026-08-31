# 📋 System Specifications & API Contracts

This document defines the functional and non-functional specifications, dataset schemas, REST API contracts, and evaluation benchmarks for the **Japanese Foods Information Retrieval System**.

---

## 1. System Requirements

### 1.1 Functional Requirements (FR)
- **FR-1: Full-Text Recipe Search**: Support lexical keyword search over recipe titles and ingredient lists.
- **FR-2: Dynamic Query Expansion**: Automatically apply pseudo-relevance feedback on initial candidate matches to discover and append co-occurring culinary terms.
- **FR-3: Pantry Ingredient Matcher**: Allow users to provide a list of available ingredients and retrieve recipes sorted by ingredient coverage and cosine similarity.
- **FR-4: Inverted Index Lookup**: Provide an inspection interface for term Document Frequency (DF) and postings list verification with fuzzy spelling suggestions.
- **FR-5: Culinary Clustering**: Group recipes into $K=6$ clusters and provide 2D PCA spatial coordinates for graphical exploration.
- **FR-6: Quantitative IR Evaluation**: Compute $P@K, R@K, AP$, confusion metrics (TP, FP, FN), and session MAP scores.
- **FR-7: Live Data Scraping & Pipeline Trigger**: On-demand web scraping from Cookpad / Culinary APIs and hot-reloading the model in memory.
- **FR-8: Self-Healing Default Dataset**: Automatic fallback and dataset reconstruction if local data files are missing or empty.
- **FR-9: Dark/Light Mode Theme Toggle**: Persistent theme switching saved in client storage.
- **FR-10: Bilingual Localization & Language Switcher**: Instant switching between Thai (`🇹🇭 ภาษาไทย`) and English (`🇬🇧 English`) with state persistence.
- **FR-11: Quick Category Filters & Pantry Presets**: Interactive one-click category chips and common Japanese dish pantry presets.
- **FR-12: Educational IR Concept Tooltips**: Interactive context tooltips explaining VSM, TF-IDF, PRF, and evaluation metrics.
- **FR-13: Comprehensive Fault-Tolerance & Fallbacks**: Built-in offline NLTK tokenizers, port hunting conflict resolution, and substring search fallbacks on unseen queries.

### 1.2 Non-Functional Requirements (NFR)
- **NFR-1: Low Latency**: Search and expansion response time $< 50\text{ms}$ on standard CPU.
- **NFR-2: Zero Build Step Frontend**: Pure HTML5, CSS3, and Vanilla JavaScript with no npm/webpack/bundler compilation required.
- **NFR-3: Cross-Platform Compatibility**: Fully compatible with Windows (handling UTF-8 console output), Linux, and macOS.
- **NFR-4: Responsive UI**: Mobile-friendly 2-tier header layout adapting across desktop, tablet, and mobile breakpoints (360px to 1440px+) with zero button collision.
- **NFR-5: Graceful Degradation**: Offline-safe operation with fallback UI states if external CDNs or APIs are unreachable.

---

## 2. Dataset Schema Specifications

### `data/processed/Japan_Food_Ingredients_Cleaned.csv`
Primary indexed dataset used by `engine.py`.

| Field Name | Type | Nullable | Description | Example |
|---|---|---|---|---|
| `Recipe Title` | `String` | No | Original English title of the dish | `Spicy Chicken Japanese Curry` |
| `Recipe URL` | `String` | No | Source URL on Cookpad | `https://cookpad.com/eng/recipes/...` |
| `Ingredients` | `String` | Yes | Raw scraped ingredients string | `500 g minced chicken, 500 g carrot...` |
| `Cleaned Title` | `String` | No | Tokenized, lemmatized title | `spicy chicken japanese curry` |
| `Cleaned Ingredients`| `String` | Yes | Stopword-filtered, lemmatized tokens | `chicken carrot onion butter...` |

---

## 3. REST API Contract Specifications

### 3.1 `GET /api/search`
Retrieves ranked recipes matching a user query.

#### Request Parameters
| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `q` | `string` | No | `""` | Search query or ingredient terms |
| `top_k` | `integer`| No | `15` | Maximum number of results to return |
| `cluster` | `integer`| No | `null` | Filter by Cluster ID (0 to 5) |

#### Response Schema (`200 OK`)
```json
{
  "raw_query": "chicken",
  "clean_query": "chicken",
  "expanded_query": "chicken sauce",
  "added_terms": ["sauce"],
  "results": [
    {
      "id": 1,
      "title": "Chili Sauce Chicken Sando",
      "url": "https://cookpad.com/eng/recipes/25431062",
      "score": 0.3608,
      "cluster_id": 1,
      "cluster_name": "Cluster 2: Toast, Sando, Whip, Cream",
      "ingredients": "1 lb ground chicken, 2 green onions...",
      "cleaned_ingredients": "chicken green onion ginger garlic egg...",
      "pca_x": -0.0452,
      "pca_y": 0.1284
    }
  ],
  "total_results": 1
}
```

---

### 3.2 `POST /api/pantry`
Matches available pantry ingredients against recipes in the database.

#### Request Body (`application/json`)
```json
{
  "ingredients": ["chicken", "soy sauce", "garlic", "egg"],
  "top_k": 10
}
```

#### Response Schema (`200 OK`)
```json
{
  "raw_query": "chicken soy sauce garlic egg",
  "results": [
    {
      "id": 14,
      "title": "Japanese Yakitori (Chicken Thigh Skewers)",
      "url": "https://cookpad.com/eng/recipes/24997517",
      "score": 0.4812,
      "cluster_id": 4,
      "cluster_name": "Cluster 5: Skewers, Meatball, Yakitori",
      "ingredients": "chicken thighs, tare sauce, soy sauce, sake...",
      "cleaned_ingredients": "chicken tare sauce sake mirin garlic ginger",
      "matched_ingredients": ["chicken", "soy sauce", "garlic"],
      "missing_ingredients": ["tare sauce", "sake", "mirin", "ginger"],
      "match_ratio": 0.43,
      "pca_x": 0.1245,
      "pca_y": -0.0892
    }
  ],
  "total_results": 1
}
```

---

### 3.3 `GET /api/clusters`
Retrieves cluster summaries and all recipe 2D PCA coordinates for visualization.

#### Response Schema (`200 OK`)
```json
{
  "clusters": [
    {
      "cluster_id": 0,
      "name": "Cluster 1: Ramen, Noodle, Broth, Miso",
      "count": 18,
      "sample_recipes": [
        {"title": "Shoyu Ramen", "url": "https://cookpad.com/eng/recipes/24560444"}
      ],
      "centroid": [-0.12, 0.45]
    }
  ],
  "points": [
    {
      "id": 0,
      "title": "Chicken Karaage",
      "cluster_id": 4,
      "pca_x": 0.295,
      "pca_y": 0.212
    }
  ],
  "total_clusters": 6
}
```

---

### 3.4 `GET /api/inverted_index?term={term}`
Inspects document frequency and postings list for a specific vocabulary term.

#### Response Schema (`200 OK`)
```json
{
  "term": "chicken",
  "found": true,
  "df": 36,
  "total_docs": 100,
  "postings_count": 36,
  "sample_postings": [
    {"doc_id": 0, "title": "Chicken Meatball for Nabe"},
    {"doc_id": 2, "title": "Spicy Chicken Japanese Curry"}
  ]
}
```

---

### 3.5 `POST /api/evaluate`
Evaluates IR precision, recall, and average precision against ground-truth relevant sets.

#### Request Body (`application/json`)
```json
{
  "query": "chicken teriyaki",
  "k": 10
}
```

#### Response Schema (`200 OK`)
```json
{
  "precision_at_k": 0.8,
  "recall_at_k": 0.67,
  "average_precision": 0.74,
  "tp": 8,
  "fp": 2,
  "fn": 4,
  "total_relevant": 12,
  "k": 10
}
```

---

### 3.6 `GET /api/pipeline/status` & `POST /api/pipeline/scrape`
Manages data ingestion, scraping, and real-time execution logs.
