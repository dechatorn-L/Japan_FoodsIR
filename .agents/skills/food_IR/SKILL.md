---
name: food_IR
description: Search, retrieve, cluster, and evaluate Japanese culinary recipes using Vector Space Modeling (VSM), TF-IDF, Pseudo-Relevance Feedback (Query Expansion), and K-Means clustering.
---

# Japanese Foods Information Retrieval (food_IR) Skill

This skill provides comprehensive capabilities for querying, analyzing, clustering, and evaluating Japanese recipe data using traditional Information Retrieval (IR) algorithms.

## Capabilities

1. **Recipe Information Retrieval (VSM + TF-IDF)**:
   - Vector Space Model retrieval over combined Recipe Title and Ingredient fields.
   - Title weighting multiplier ($6\times$) for relevance prioritization.
   - Cosine similarity ranking between query vectors and document vectors.

2. **Dynamic Query Expansion (Pseudo-Relevance Feedback)**:
   - Evaluates initial top-10 candidate recipes for co-occurring culinary concepts.
   - Applies dynamic frequency thresholds to expand user queries with high-relevance terms (e.g., `chicken` $\rightarrow$ `chicken sauce renkon ginger egg`).

3. **Pantry Matcher ("Cook with What You Have")**:
   - Matches available ingredients in the kitchen against all indexed dishes.
   - Calculates ingredient coverage ratio, matched tokens, and missing ingredients.

4. **Recipe Categorization & Clustering (K-Means + PCA)**:
   - Unsupervised clustering into 6 culinary clusters based on TF-IDF term distributions.
   - 2D Principal Component Analysis (PCA) projection for spatial recipe distribution with Centroids.

5. **Information Retrieval Evaluation**:
   - Computes Precision@K ($P@K$), Recall@K ($R@K$), Average Precision ($AP$), and Mean Average Precision ($MAP$).
   - Generates confusion metrics (True Positives, False Positives, False Negatives).

6. **Inverted Index Inspection**:
   - Term Document Frequency (DF) lookup.
   - Postings list inspection and fuzzy suggestions for all vocabulary tokens.

---

## Dataset Schema

The primary dataset is stored in `data/processed/Japan_Food_Ingredients_Cleaned.csv`:

| Column | Description |
|---|---|
| `Recipe Title` | Original English title of the Japanese dish |
| `Recipe URL` | Link to Cookpad recipe source |
| `Ingredients` | Raw scraped ingredients string including quantities and preparation notes |
| `Cleaned Title` | Lowercased, alphanumeric-filtered, stopword-stripped, and lemmatized title |
| `Cleaned Ingredients` | Culinary-stopword-filtered and lemmatized ingredient tokens |

---

## Programmatic Usage

### 1. Load Search Engine via Python SDK

```python
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path("c:/Projects/Japanese_Foods_IR-main")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.engine import get_engine

# Initialize unified IR engine instance
engine = get_engine()
print(f"Loaded {len(engine.df)} recipes with {len(engine.feature_names)} terms.")
```

### 2. Search with Pseudo-Relevance Feedback

```python
# Execute search with automatic PRF expansion
results = engine.search("chicken teriyaki", top_k=5, use_expansion=True)

print("Clean Query:", results['clean_query'])
print("Expanded Query:", results['expanded_query'])
print("Added Concepts:", results['added_terms'])

for r in results['results']:
    print(f"- {r['title']} (Score: {r['score']:.4f}, Cluster: {r['cluster_name']})")
```

### 3. Pantry Ingredient Matching

```python
# Match ingredients currently in fridge
pantry_results = engine.pantry_search(["chicken", "soy sauce", "garlic", "ginger"], top_k=5)

for r in pantry_results['results']:
    print(f"- {r['title']}: Match {int(r['match_ratio']*100)}% | Have: {r['matched_ingredients']} | Need: {r['missing_ingredients']}")
```

### 4. Evaluate Search Quality

```python
# Run quantitative IR evaluation benchmark
search_res = engine.search("ramen noodles", top_k=30)
retrieved_ids = [r['id'] for r in search_res['results']]

metrics = engine.compute_evaluation_metrics(retrieved_ids, "ramen noodles", k=10)
print(f"P@10: {metrics['precision_at_k']:.2f}, R@10: {metrics['recall_at_k']:.2f}, AP: {metrics['average_precision']:.2f}")
```
