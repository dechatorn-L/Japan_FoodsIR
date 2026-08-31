import sys
import re
from pathlib import Path
import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from collections import Counter

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
POSSIBLE_DATA_PATHS = [
    PROJECT_ROOT / "data" / "processed" / "Japan_Food_Ingredients_Cleaned.csv",
    PROJECT_ROOT / "Japan_Food_Ingredients_Cleaned.csv",
    Path("Japan_Food_Ingredients_Cleaned.csv")
]

DATA_PATH = None
for p in POSSIBLE_DATA_PATHS:
    if p.exists():
        DATA_PATH = p
        break


def precision_at_k(retrieved, relevant, k):
    retrieved_k = retrieved[:k]
    if not retrieved_k: return 0.0
    relevant_and_retrieved = set(retrieved_k).intersection(set(relevant))
    return len(relevant_and_retrieved) / k


def recall_at_k(retrieved, relevant, k):
    retrieved_k = retrieved[:k]
    if not relevant: return 0.0
    relevant_and_retrieved = set(retrieved_k).intersection(set(relevant))
    return len(relevant_and_retrieved) / len(relevant)


def average_precision(retrieved, relevant):
    if not relevant: return 0.0
    score = 0.0
    num_hits = 0.0
    for i, p in enumerate(retrieved):
        if p in relevant:
            num_hits += 1.0
            score += num_hits / (i + 1.0)
    return score / len(relevant)


def run_vsm_cli():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    if DATA_PATH is None or not DATA_PATH.exists():
        print("Cannot find cleaned recipe dataset.")
        return

    df = pd.read_csv(DATA_PATH, encoding='utf-8-sig')
    df['Cleaned Ingredients'] = df['Cleaned Ingredients'].fillna('')

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    vectorizer = TfidfVectorizer()
    df['Search_Text'] = (df['Cleaned Title'].astype(str) + " ") * 6 + df['Cleaned Ingredients'].astype(str)
    tfidf_matrix = vectorizer.fit_transform(df['Search_Text'])
    feature_names = vectorizer.get_feature_names_out()

    inverted_index = {}
    for col_idx, term in enumerate(feature_names):
        doc_indices = tfidf_matrix[:, col_idx].nonzero()[0]
        postings_list = [f"Doc{doc_id}" for doc_id in doc_indices]
        inverted_index[term] = {
            'DF': len(doc_indices),
            'Postings': postings_list
        }

    def expand_query(query):
        query_vec = vectorizer.transform([query])
        initial_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
        top_10_idx = initial_sim.argsort()[-10:][::-1]
        
        local_concepts = []
        for idx in top_10_idx:
            if initial_sim[idx] > 0:
                ingredients_text = str(df['Cleaned Ingredients'].iloc[idx])
                local_concepts.extend(ingredients_text.split())

        concept_counts = Counter(local_concepts)
        existing_words = set(query.split())

        for w in existing_words:
            if w in concept_counts:
                del concept_counts[w]
                
        if not concept_counts:
            return query
            
        max_freq = concept_counts.most_common(1)[0][1]
        dynamic_concepts = [
            w for w, count in concept_counts.most_common()
            if w not in existing_words and count >= max_freq and len(w) > 1
        ]
        
        MAX_WORDS = 5
        final_concepts = dynamic_concepts[:MAX_WORDS]
        return f"{query} {' '.join(final_concepts)}" if final_concepts else query

    N = 15
    def search_recipes(original_query, top_n=N):
        expanded_q = expand_query(original_query)
        if expanded_q != original_query.lower():
            print(f"\n   [Query Expansion] : '{expanded_q}'")

        query_vec = vectorizer.transform([expanded_q])
        similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
        top_indices = similarity_scores.argsort()[-top_n:][::-1]
        
        results = []
        for idx in top_indices:
            score = similarity_scores[idx]
            results.append({
                'Index': idx,
                'Title': df.iloc[idx]['Recipe Title'],
                'Score': score,
                'URL': df.iloc[idx]['Recipe URL'],
                'Cluster': df.iloc[idx]['Cluster_ID'] + 1
            })
        return results

    true_k = 6
    kmeans_model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1, random_state=0)
    kmeans_model.fit(tfidf_matrix)
    df['Cluster_ID'] = kmeans_model.labels_

    session_history = []
    print("=" * 60)
    print("  🍣 Welcome to Japanese Foods IR Engine (Interactive CLI)")
    print("=" * 60)

    while True:
        try:
            user_query = input("\nEnter your search query (or 'q'/'exit' to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting search engine.")
            break

        if user_query.lower() in ['q', 'exit', 'quit']:
            print("\nThank you for using the Japanese Foods IR Engine.")
            break

        if not user_query:
            continue

        clean_text = re.sub(r'[^a-z\s]', ' ', user_query.lower())
        clean_query_words = [lemmatizer.lemmatize(w) for w in clean_text.split() if w not in stop_words and len(w) > 1]
        clean_query = " ".join(clean_query_words)

        if not clean_query:
            print("Please enter a valid culinary term.")
            continue

        search_results = search_recipes(clean_query, top_n=N)
        print(f"\nFound {len(search_results)} matching Japanese dishes:")
        for i, res in enumerate(search_results):
            print(f"[{i+1}] {res['Title']}")
            print(f"     Sim: {res['Score']:.4f} | Category: Cluster {res['Cluster']} | URL: {res['URL']}")

        # Quantitative Evaluation
        expanded_eval_query = expand_query(clean_query)
        eval_pattern = r'\b(?:' + '|'.join(expanded_eval_query.split()) + r')\b'
        relevant_docs = df[
            df['Cleaned Title'].str.contains(eval_pattern, case=False, na=False) |
            df['Cleaned Ingredients'].str.contains(eval_pattern, case=False, na=False)
        ].index.tolist()

        retrieved_indices = [res['Index'] for res in search_results]
        p_score = precision_at_k(retrieved_indices, relevant_docs, N)
        r_score = recall_at_k(retrieved_indices, relevant_docs, N)
        ap_score = average_precision(retrieved_indices, relevant_docs)

        session_history.append({'query': user_query, 'p': p_score, 'r': r_score, 'ap': ap_score})
        print(f"\nP@{N}: {p_score:.2f} | R@{N}: {r_score:.2f} | AP: {ap_score:.2f}")


if __name__ == '__main__':
    run_vsm_cli()
