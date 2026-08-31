import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import Counter
import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from .preprocessing.text_cleaner import clean_recipe_dataset
from .crawler.url_scraper import scrape_recipe_urls
from .crawler.recipe_scraper import scrape_recipe_details

# Ensure NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
POSSIBLE_PATHS = [
    PROJECT_ROOT / "data" / "processed" / "Japan_Food_Ingredients_Cleaned.csv",
    PROJECT_ROOT / "Japan_Food_Ingredients_Cleaned.csv",
    Path("data/processed/Japan_Food_Ingredients_Cleaned.csv"),
    Path("Japan_Food_Ingredients_Cleaned.csv")
]

DEFAULT_DATA_PATH = None
for p in POSSIBLE_PATHS:
    if p.exists():
        DEFAULT_DATA_PATH = p.resolve()
        break

if DEFAULT_DATA_PATH is None:
    DEFAULT_DATA_PATH = POSSIBLE_PATHS[0]


class JapaneseFoodIREngine:
    def __init__(self, data_path: Path = DEFAULT_DATA_PATH, n_clusters: int = 6):
        self.data_path = Path(data_path)
        self.n_clusters = n_clusters
        
        try:
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            self.lemmatizer = None
            self.stop_words = {
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
                'he', 'him', 'his', 'she', 'her', 'it', 'its', 'they', 'them', 'their', 'theirs',
                'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
                'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
                'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
                'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
                'to', 'from', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then'
            }
        
        self.df = None
        self.vectorizer = None
        self.tfidf_matrix = None
        self.inverted_index = {}
        self.kmeans_model = None
        self.pca_coordinates = None
        self.cluster_names = {}
        self.centroids_2d = []
        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.pipeline_logs = []
        
        self.load_and_index()

    def log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.pipeline_logs.append(entry)
        if len(self.pipeline_logs) > 50:
            self.pipeline_logs.pop(0)

    def load_and_index(self):
        from .default_data import ensure_data_files
        
        if not self.data_path.exists() or self.data_path.stat().st_size == 0:
            ensure_data_files()
            
        try:
            self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
        except Exception:
            self.df = pd.read_csv(self.data_path, encoding='latin1')

        if len(self.df) == 0:
            ensure_data_files()
            self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')

        self.df['Cleaned Ingredients'] = self.df['Cleaned Ingredients'].fillna('')
        self.df['Cleaned Title'] = self.df['Cleaned Title'].fillna('')
        self.df['Search_Text'] = (self.df['Cleaned Title'].astype(str) + " ") * 6 + self.df['Cleaned Ingredients'].astype(str)
        
        # TF-IDF Vectorization with empty vocabulary fallback
        try:
            self.vectorizer = TfidfVectorizer()
            self.tfidf_matrix = self.vectorizer.fit_transform(self.df['Search_Text'])
            self.feature_names = self.vectorizer.get_feature_names_out()
        except ValueError:
            # Vocabulary was empty; rebuild healthy defaults
            ensure_data_files()
            self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
            self.df['Cleaned Ingredients'] = self.df['Cleaned Ingredients'].fillna('')
            self.df['Cleaned Title'] = self.df['Cleaned Title'].fillna('')
            self.df['Search_Text'] = (self.df['Cleaned Title'].astype(str) + " ") * 6 + self.df['Cleaned Ingredients'].astype(str)
            self.vectorizer = TfidfVectorizer()
            self.tfidf_matrix = self.vectorizer.fit_transform(self.df['Search_Text'])
            self.feature_names = self.vectorizer.get_feature_names_out()
        
        # Inverted Index Generation
        self.inverted_index = {}
        for col_idx, term in enumerate(self.feature_names):
            doc_indices = self.tfidf_matrix[:, col_idx].nonzero()[0].tolist()
            self.inverted_index[term] = {
                'df': len(doc_indices),
                'postings': [int(d) for d in doc_indices]
            }
            
        # Adaptive K-Means Clustering (safe for any dataset size)
        actual_clusters = max(1, min(self.n_clusters, len(self.df)))
        self.kmeans_model = KMeans(n_clusters=actual_clusters, init='k-means++', max_iter=100, n_init=1, random_state=0)
        self.df['Cluster_ID'] = self.kmeans_model.fit_predict(self.tfidf_matrix)
        
        # Safe PCA 2D coordinates for visualization
        try:
            if len(self.df) >= 2 and self.tfidf_matrix.shape[1] >= 2:
                pca = PCA(n_components=2, random_state=0)
                reduced = pca.fit_transform(self.tfidf_matrix.toarray())
                centroids_2d = pca.transform(self.kmeans_model.cluster_centers_)
                self.df['pca_x'] = reduced[:, 0]
                self.df['pca_y'] = reduced[:, 1]
                self.centroids_2d = centroids_2d.tolist()
            else:
                self.df['pca_x'] = 0.0
                self.df['pca_y'] = 0.0
                self.centroids_2d = [[0.0, 0.0] for _ in range(actual_clusters)]
        except Exception:
            self.df['pca_x'] = 0.0
            self.df['pca_y'] = 0.0
            self.centroids_2d = [[0.0, 0.0] for _ in range(actual_clusters)]
        
        # Cluster labels naming
        order_centroids = self.kmeans_model.cluster_centers_.argsort()[:, ::-1]
        self.cluster_names = {}
        for i in range(actual_clusters):
            top_words = [self.feature_names[ind] for ind in order_centroids[i, :4] if ind < len(self.feature_names)]
            words_str = ', '.join(top_words).title() if top_words else f"Group {i+1}"
            self.cluster_names[i] = f"Cluster {i+1}: {words_str}"

        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def reindex_existing_data(self) -> Dict[str, Any]:
        """Re-runs text cleaning on raw data and rebuilds the VSM index"""
        self.log("Starting data cleaning and model re-indexing...")
        clean_recipe_dataset(progress_callback=self.log)
        self.load_and_index()
        self.log(f"Re-indexing complete! {len(self.df)} recipes indexed.")
        return self.get_status()

    def run_scraping_pipeline(self, target_count: int = 20) -> Dict[str, Any]:
        """Performs live web scraping from Cookpad, cleans text, and rebuilds the model"""
        start_time = time.time()
        self.log(f"Starting web scraping pipeline for {target_count} recipes...")
        
        try:
            # 1. Scrape links
            links_count = scrape_recipe_urls(amount=target_count, progress_callback=self.log)
            # 2. Scrape details
            details_count = scrape_recipe_details(max_items=target_count, progress_callback=self.log)
            # 3. Clean text
            clean_recipe_dataset(progress_callback=self.log)
            # 4. Rebuild index
            self.load_and_index()
            
            elapsed = round(time.time() - start_time, 2)
            self.log(f"Pipeline finished successfully in {elapsed}s. {len(self.df)} total recipes available.")
            
            return {
                'success': True,
                'message': f"Successfully scraped {details_count} recipes and updated index in {elapsed}s.",
                'recipes_count': len(self.df),
                'vocabulary_size': len(self.feature_names),
                'elapsed_seconds': elapsed,
                'status': self.get_status()
            }
        except Exception as e:
            self.log(f"Error during scraping pipeline: {e}")
            return {
                'success': False,
                'error': str(e),
                'status': self.get_status()
            }

    def get_status(self) -> Dict[str, Any]:
        return {
            'total_recipes': len(self.df) if self.df is not None else 0,
            'vocabulary_size': len(self.feature_names) if self.feature_names is not None else 0,
            'n_clusters': self.n_clusters,
            'last_updated': self.last_updated,
            'recent_logs': self.pipeline_logs[-15:]
        }

    def preprocess_query(self, raw_query: str) -> str:
        clean_text = re.sub(r'[^a-z\s]', ' ', raw_query.lower())
        tokens = [
            self.lemmatizer.lemmatize(w)
            for w in clean_text.split()
            if w not in self.stop_words and len(w) > 1
        ]
        return " ".join(tokens)

    def expand_query(self, query: str, max_expansion_words: int = 5) -> Tuple[str, List[str]]:
        clean_q = self.preprocess_query(query)
        if not clean_q:
            return query, []
            
        query_vec = self.vectorizer.transform([clean_q])
        initial_sim = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_10_idx = initial_sim.argsort()[-10:][::-1]
        
        local_concepts = []
        for idx in top_10_idx:
            if initial_sim[idx] > 0:
                ingredients_text = str(self.df['Cleaned Ingredients'].iloc[idx])
                local_concepts.extend(ingredients_text.split())
                
        concept_counts = Counter(local_concepts)
        existing_words = set(clean_q.split())
        for w in existing_words:
            concept_counts.pop(w, None)
            
        if not concept_counts:
            return clean_q, []
            
        max_freq = concept_counts.most_common(1)[0][1]
        dynamic_concepts = [
            w for w, count in concept_counts.most_common()
            if w not in existing_words and count >= max_freq and len(w) > 1
        ]
        
        added_words = dynamic_concepts[:max_expansion_words]
        if added_words:
            expanded_query = f"{clean_q} {' '.join(added_words)}"
            return expanded_query, added_words
        return clean_q, []

    def search(self, query: str, top_k: int = 15, use_expansion: bool = True, cluster_filter: int = None) -> Dict[str, Any]:
        raw_query = query.strip()
        if not raw_query:
            results = []
            for idx in range(len(self.df)):
                cluster_id = int(self.df.iloc[idx]['Cluster_ID'])
                if cluster_filter is not None and cluster_id != cluster_filter:
                    continue
                row = self.df.iloc[idx]
                results.append({
                    'id': int(idx),
                    'title': str(row['Recipe Title']),
                    'url': str(row['Recipe URL']),
                    'score': 1.0,
                    'cluster_id': cluster_id,
                    'cluster_name': self.cluster_names.get(cluster_id, f"Cluster {cluster_id+1}"),
                    'ingredients': str(row['Ingredients']),
                    'cleaned_ingredients': str(row['Cleaned Ingredients']),
                    'pca_x': float(row['pca_x']),
                    'pca_y': float(row['pca_y'])
                })
                if len(results) >= top_k:
                    break
            return {
                'raw_query': '',
                'clean_query': '',
                'expanded_query': '',
                'added_terms': [],
                'results': results,
                'total_results': len(results)
            }
            
        clean_q = self.preprocess_query(raw_query)
        if use_expansion:
            expanded_q, added_terms = self.expand_query(raw_query)
            search_text = expanded_q
        else:
            expanded_q = clean_q
            added_terms = []
            search_text = clean_q
            
        if not search_text:
            return {
                'raw_query': raw_query,
                'clean_query': clean_q,
                'expanded_query': expanded_q,
                'added_terms': added_terms,
                'results': [],
                'total_results': 0
            }

        query_vec = self.vectorizer.transform([search_text])
        similarity_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        sorted_indices = similarity_scores.argsort()[::-1]
        
        results = []
        for idx in sorted_indices:
            score = float(similarity_scores[idx])
            if score <= 0.0:
                continue
                
            cluster_id = int(self.df.iloc[idx]['Cluster_ID'])
            if cluster_filter is not None and cluster_id != cluster_filter:
                continue
                
            row = self.df.iloc[idx]
            results.append({
                'id': int(idx),
                'title': str(row['Recipe Title']),
                'url': str(row['Recipe URL']),
                'score': round(score, 4),
                'cluster_id': cluster_id,
                'cluster_name': self.cluster_names.get(cluster_id, f"Cluster {cluster_id+1}"),
                'ingredients': str(row['Ingredients']),
                'cleaned_ingredients': str(row['Cleaned Ingredients']),
                'pca_x': float(row['pca_x']),
                'pca_y': float(row['pca_y'])
            })
            
            if len(results) >= top_k:
                break
                
        # Fallback: if TF-IDF cosine similarity yielded 0 results, perform substring and token matching
        if not results:
            query_lower = raw_query.lower()
            tokens = [w for w in query_lower.split() if len(w) > 2]
            for idx in range(len(self.df)):
                row = self.df.iloc[idx]
                title_lower = str(row['Recipe Title']).lower()
                ing_lower = str(row['Ingredients']).lower()
                
                score = 0.0
                if query_lower in title_lower:
                    score = 0.85
                elif any(tok in title_lower for tok in tokens):
                    score = 0.65
                elif any(tok in ing_lower for tok in tokens):
                    score = 0.45

                if score > 0.0:
                    cluster_id = int(row['Cluster_ID'])
                    if cluster_filter is not None and cluster_id != cluster_filter:
                        continue
                    results.append({
                        'id': int(idx),
                        'title': str(row['Recipe Title']),
                        'url': str(row['Recipe URL']),
                        'score': round(score, 4),
                        'cluster_id': cluster_id,
                        'cluster_name': self.cluster_names.get(cluster_id, f"Cluster {cluster_id+1}"),
                        'ingredients': str(row['Ingredients']),
                        'cleaned_ingredients': str(row['Cleaned Ingredients']),
                        'pca_x': float(row['pca_x']),
                        'pca_y': float(row['pca_y'])
                    })
                    if len(results) >= top_k:
                        break

        return {
            'raw_query': raw_query,
            'clean_query': clean_q,
            'expanded_query': expanded_q,
            'added_terms': added_terms,
            'results': results,
            'total_results': len(results)
        }

    def pantry_search(self, available_ingredients: List[str], top_k: int = 15) -> Dict[str, Any]:
        pantry_str = " ".join(available_ingredients)
        search_res = self.search(pantry_str, top_k=top_k, use_expansion=False)
        
        clean_pantry_tokens = set(self.preprocess_query(pantry_str).split())
        for item in search_res['results']:
            recipe_tokens = set(item['cleaned_ingredients'].split())
            matched = clean_pantry_tokens.intersection(recipe_tokens)
            missing = recipe_tokens - clean_pantry_tokens
            item['matched_ingredients'] = list(matched)
            item['missing_ingredients'] = list(missing)[:8]
            item['match_ratio'] = round(len(matched) / max(1, len(recipe_tokens)), 2)
            
        return search_res

    def inspect_inverted_index(self, term: str) -> Dict[str, Any]:
        term_clean = term.lower().strip()
        if self.lemmatizer is not None:
            try:
                term_clean = self.lemmatizer.lemmatize(term_clean)
            except Exception:
                pass

        if term_clean in self.inverted_index:
            info = self.inverted_index[term_clean]
            postings_details = []
            for doc_id in info['postings'][:20]:
                postings_details.append({
                    'doc_id': doc_id,
                    'title': self.df.iloc[doc_id]['Recipe Title']
                })
            return {
                'term': term_clean,
                'found': True,
                'df': info['df'],
                'total_docs': len(self.df),
                'postings_count': len(info['postings']),
                'sample_postings': postings_details
            }

        # Fallback: fuzzy suggestion of close terms
        import difflib
        suggestions = difflib.get_close_matches(term_clean, list(self.feature_names), n=5, cutoff=0.5)
        return {
            'term': term_clean,
            'found': False,
            'df': 0,
            'total_docs': len(self.df),
            'postings_count': 0,
            'sample_postings': [],
            'suggestions': suggestions
        }

    def compute_evaluation_metrics(self, retrieved_indices: List[int], query_text: str, k: int = 15) -> Dict[str, Any]:
        expanded_q, _ = self.expand_query(query_text)
        terms = [re.escape(t) for t in expanded_q.split() if len(t) > 1]
        if not terms:
            return {'precision_at_k': 0.0, 'recall_at_k': 0.0, 'average_precision': 0.0, 'tp': 0, 'fp': 0, 'fn': 0}
            
        eval_pattern = r'\b(?:' + '|'.join(terms) + r')\b'
        relevant_mask = (
            self.df['Cleaned Title'].str.contains(eval_pattern, case=False, na=False) |
            self.df['Cleaned Ingredients'].str.contains(eval_pattern, case=False, na=False)
        )
        relevant_docs = self.df[relevant_mask].index.tolist()
        relevant_set = set(relevant_docs)
        
        retrieved_k = retrieved_indices[:k]
        tp_set = set(retrieved_k).intersection(relevant_set)
        tp = len(tp_set)
        fp = len(retrieved_k) - tp
        fn = len(relevant_set) - tp
        
        p_at_k = tp / k if k > 0 else 0.0
        recall_at_k = tp / len(relevant_set) if len(relevant_set) > 0 else 0.0
        
        score = 0.0
        hits = 0.0
        for i, idx in enumerate(retrieved_indices):
            if idx in relevant_set:
                hits += 1.0
                score += hits / (i + 1.0)
        ap = score / len(relevant_set) if len(relevant_set) > 0 else 0.0
        
        return {
            'precision_at_k': round(p_at_k, 4),
            'recall_at_k': round(recall_at_k, 4),
            'average_precision': round(ap, 4),
            'tp': tp,
            'fp': fp,
            'fn': fn,
            'total_relevant': len(relevant_set),
            'k': k
        }

    def get_clusters_summary(self) -> Dict[str, Any]:
        summary = []
        for i in range(self.n_clusters):
            cluster_df = self.df[self.df['Cluster_ID'] == i]
            recipes = []
            for _, r in cluster_df.head(5).iterrows():
                recipes.append({
                    'title': str(r['Recipe Title']),
                    'url': str(r['Recipe URL'])
                })
            summary.append({
                'cluster_id': i,
                'name': self.cluster_names.get(i, f"Cluster {i+1}"),
                'count': len(cluster_df),
                'sample_recipes': recipes,
                'centroid': self.centroids_2d[i]
            })

        points = []
        for idx in range(len(self.df)):
            row = self.df.iloc[idx]
            points.append({
                'id': int(idx),
                'title': str(row['Recipe Title']),
                'cluster_id': int(row['Cluster_ID']),
                'pca_x': float(row['pca_x']),
                'pca_y': float(row['pca_y'])
            })

        return {
            'clusters': summary,
            'points': points,
            'total_clusters': len(summary)
        }


_engine_instance = None

def get_engine() -> JapaneseFoodIREngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = JapaneseFoodIREngine()
    return _engine_instance
