from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

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


def run_food_clustering(true_k: int = 6, show_plot: bool = True):
    if DATA_PATH is None or not DATA_PATH.exists():
        print(f"Cannot find dataset in {POSSIBLE_DATA_PATHS}")
        return

    df = pd.read_csv(DATA_PATH, encoding='utf-8-sig')
    df['Cleaned Ingredients'] = df['Cleaned Ingredients'].fillna('')

    print("Computing TF-IDF Matrix...")
    vectorizer = TfidfVectorizer()
    df['Search_Text'] = (df['Cleaned Title'].astype(str) + " ") * 3 + df['Cleaned Ingredients'].astype(str)
    tfidf_matrix = vectorizer.fit_transform(df['Search_Text'])

    print(f"Performing K-Means Clustering with K={true_k}...")
    kmeans_model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1, random_state=0)
    kmeans_model.fit(tfidf_matrix)
    df['Cluster'] = kmeans_model.labels_

    print("\n" + "=" * 60)
    print("Clustering Results (Top Words per Cluster):")
    print("=" * 60)

    order_centroids = kmeans_model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    for i in range(true_k):
        top_words = [terms[ind] for ind in order_centroids[i, :7]]
        print(f"🍲 Cluster {i+1}: {', '.join(top_words)}")
    print("=" * 60)

    print("Visualizing Clusters with 2D PCA...")
    pca = PCA(n_components=2, random_state=0)
    reduced_features = pca.fit_transform(tfidf_matrix.toarray())
    centroids_2d = pca.transform(kmeans_model.cluster_centers_)

    df_pca = pd.DataFrame(reduced_features, columns=['PCA1', 'PCA2'])
    df_pca['Cluster'] = [f"Cluster {c+1}" for c in df['Cluster']]
    df_pca['Recipe Title'] = df['Recipe Title']

    plt.figure(figsize=(10, 7))
    sns.set_theme(style="whitegrid")

    sns.scatterplot(
        x='PCA1',
        y='PCA2',
        hue='Cluster',
        palette=sns.color_palette('Set2', true_k),
        data=df_pca,
        legend='full',
        alpha=0.75,
        s=100
    )

    plt.scatter(
        centroids_2d[:, 0],
        centroids_2d[:, 1],
        marker='X',
        s=250,
        color='red',
        edgecolor='black',
        label='Centroids'
    )

    plt.title(f'Japanese Recipes Clustering (K-Means, K={true_k}) with PCA', fontsize=15, fontweight='bold', pad=15)
    plt.xlabel('PCA Component 1', fontsize=12)
    plt.ylabel('PCA Component 2', fontsize=12)
    plt.legend(title='Cluster & Centroid', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    if show_plot:
        plt.show()


if __name__ == '__main__':
    run_food_clustering()
