import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure src is in python path
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from engine import get_engine

st.set_page_config(
    page_title="Japanese Foods IR & Culinary Engine",
    page_icon="🍣",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #e03131;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #868e96;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-badge {
        background: rgba(224, 49, 49, 0.1);
        border: 1px solid rgba(224, 49, 49, 0.3);
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        display: inline-block;
    }
    .preset-pill {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        margin-right: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_ir_engine():
    return get_engine()


engine = load_ir_engine()

# Sidebar: Language & Settings
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1580822184713-fc5400e7fe10?w=400&q=80", caption="Japanese Culinary Engine")
    st.markdown("### 🌐 Language / ภาษา")
    lang = st.radio("Select Language / เลือกภาษา:", ["🇹🇭 ภาษาไทย", "🇬🇧 English"], index=0)
    is_th = "ภาษาไทย" in lang

    st.markdown("---")
    st.markdown("### ℹ️ About Engine")
    st.caption("TF-IDF Vector Space Model · Pseudo-Relevance Feedback · K-Means (K=6) · 2D PCA")
    st.caption(f"**Total Recipes:** {len(engine.df)} items")
    st.caption(f"**Vocabulary Size:** {len(engine.feature_names)} tokens")

title_text = "🍣 Japanese Foods Information Retrieval Engine" if not is_th else "🍣 ระบบสืบค้นสูตรอาหารญี่ปุ่นอัจฉริยะ (Japanese Foods IR)"
sub_text = "Vector Space Model (VSM) · TF-IDF · Pseudo-Relevance Feedback · K-Means & PCA" if not is_th else "โมเดล Vector Space Model (VSM) · ถ่วงน้ำหนัก TF-IDF · ขยายคำค้นหา PRF · จัดกลุ่ม K-Means & PCA"

st.markdown(f'<div class="main-header">{title_text}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{sub_text}</div>', unsafe_allow_html=True)

tab_labels = [
    "🔍 Recipe Search" if not is_th else "🔍 ค้นหาสูตรอาหาร",
    "🍱 Pantry Matcher" if not is_th else "🍱 ค้นจากวัตถุดิบในครัว",
    "📊 2D PCA Cluster Map" if not is_th else "📊 แผนภาพคลัสเตอร์ (PCA)",
    "📖 Inverted Index" if not is_th else "📖 ดัชนีคำศัพท์ (Inverted Index)",
    "📈 IR Evaluation" if not is_th else "📈 ประเมินผลระบบ IR",
    "⚙️ Data Pipeline" if not is_th else "⚙️ จัดการข้อมูล & Scraper"
]

tabs = st.tabs(tab_labels)

# TAB 1: Search
with tabs[0]:
    st.subheader("Recipe Search & Query Expansion" if not is_th else "ค้นหาสูตรอาหาร & ขยายคำค้นหาอัตโนมัติ")
    
    # Category Quick Buttons
    st.markdown("**Quick Categories / หมวดหมู่ด่วน:**")
    cat_cols = st.columns(6)
    selected_query_preset = None
    if cat_cols[0].button("🍜 Ramen"): selected_query_preset = "ramen noodle"
    if cat_cols[1].button("🍛 Curry"): selected_query_preset = "curry"
    if cat_cols[2].button("🍢 Yakitori"): selected_query_preset = "chicken yakitori meatball"
    if cat_cols[3].button("🍱 Donburi"): selected_query_preset = "rice bowl"
    if cat_cols[4].button("🥗 Tofu/Salad"): selected_query_preset = "tofu salad"
    if cat_cols[5].button("🍵 Dessert"): selected_query_preset = "sweet matcha sando"

    col1, col2 = st.columns([3, 1])
    with col1:
        default_val = selected_query_preset if selected_query_preset else "chicken"
        query = st.text_input("Enter search query or ingredient:" if not is_th else "พิมพ์ชื่อเมนู หรือวัตถุดิบ:", value=default_val, placeholder="e.g. ramen, teriyaki chicken, curry, miso...")
    with col2:
        top_k = st.slider("Top Results (K):" if not is_th else "จำนวนผลลัพธ์ (K):", min_value=5, max_value=30, value=12)

    cluster_options = ["All Clusters" if not is_th else "ทุกคลัสเตอร์"] + [f"Cluster {i+1}: {engine.cluster_names[i]}" for i in range(engine.n_clusters)]
    cluster_filter = st.selectbox("Filter by Cluster:" if not is_th else "กรองตามคลัสเตอร์:", options=cluster_options)

    selected_c = None if ("All" in cluster_filter or "ทุก" in cluster_filter) else int(cluster_filter.split(":")[0].replace("Cluster", "").strip()) - 1

    if query:
        res = engine.search(query, top_k=top_k, cluster_filter=selected_c)
        
        if res['added_terms']:
            st.info(f"⚡ **Pseudo-Relevance Feedback Expansion:** Original: `{res['clean_query']}` → Expanded: `{res['expanded_query']}` (Added: `{' '.join(res['added_terms'])}`)")

        st.markdown(f"**Found {res['total_results']} matching recipes:**" if not is_th else f"**พบ {res['total_results']} สูตรอาหารที่ตรงกับคำค้นหา:**")
        
        cols = st.columns(3)
        for i, recipe in enumerate(res['results']):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {recipe['title']}")
                    st.caption(f"🏷️ {recipe['cluster_name']}")
                    st.markdown(f"**Cosine Similarity:** `{recipe['score']:.4f}`")
                    st.write(recipe['ingredients'][:180] + "...")
                    if recipe['url'] and recipe['url'] != 'No URL found':
                        st.link_button("View on Cookpad ↗" if not is_th else "ดูสูตรต้นฉบับ Cookpad ↗", recipe['url'])

# TAB 2: Pantry Matcher
with tabs[1]:
    st.subheader("🍱 Japanese Pantry & Fridge Matcher" if not is_th else "🍱 ค้นหาสูตรอาหารจากวัตถุดิบในตู้เย็น")
    st.write("Select ingredients currently available in your pantry:" if not is_th else "เลือกวัตถุดิบที่คุณมีอยู่ในครัวเพื่อค้นหาเมนูที่ทำได้:")

    common_staples = [
        'chicken', 'pork', 'beef', 'salmon', 'tuna', 'egg', 'tofu',
        'soy sauce', 'sake', 'mirin', 'dashi', 'miso', 'sesame oil',
        'ginger', 'garlic', 'green onion', 'onion', 'carrot', 'potato',
        'nori', 'ramen', 'udon', 'soba', 'rice', 'curry roux', 'cabbage'
    ]

    selected_ings = st.multiselect(
        "Available Ingredients / วัตถุดิบที่มี:" if is_th else "Available Ingredients:",
        options=common_staples,
        default=['chicken', 'soy sauce', 'sake', 'garlic', 'ginger']
    )

    if selected_ings:
        pantry_res = engine.pantry_search(selected_ings, top_k=12)
        st.markdown(f"### Matched Recipes ({len(pantry_res['results'])})" if not is_th else f"### เมนูที่ตรงกับวัตถุดิบของคุณ ({len(pantry_res['results'])})")
        
        pcols = st.columns(3)
        for i, recipe in enumerate(pantry_res['results']):
            with pcols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {recipe['title']}")
                    match_pct = int(recipe['match_ratio'] * 100)
                    st.progress(min(1.0, recipe['match_ratio']), text=f"Ingredient Match: {match_pct}%" if not is_th else f"ความตรงกันของวัตถุดิบ: {match_pct}%")
                    st.markdown(f"**✓ Have:** `{', '.join(recipe['matched_ingredients'])}`" if not is_th else f"**✓ มี:** `{', '.join(recipe['matched_ingredients'])}`")
                    if recipe['missing_ingredients']:
                        st.markdown(f"**+ Missing:** `{', '.join(recipe['missing_ingredients'][:4])}`" if not is_th else f"**+ ขาด:** `{', '.join(recipe['missing_ingredients'][:4])}`")
                    st.caption(f"Cosine Similarity: {recipe['score']:.4f}")
                    if recipe['url'] and recipe['url'] != 'No URL found':
                        st.link_button("View on Cookpad ↗", recipe['url'])

# TAB 3: Cluster Map (PCA)
with tabs[2]:
    st.subheader("📊 Recipe Clustering & 2D PCA Map" if not is_th else "📊 แผนภาพการจัดกลุ่มสูตรอาหาร (2D PCA & K-Means)")
    
    col_chart, col_info = st.columns([2, 1])
    with col_chart:
        fig, ax = plt.subplots(figsize=(9, 6))
        palette = sns.color_palette("bright", 6)
        scatter = sns.scatterplot(
            x=engine.df['pca_x'],
            y=engine.df['pca_y'],
            hue=engine.df['Cluster_ID'],
            palette=palette,
            s=80,
            alpha=0.85,
            ax=ax
        )
        
        # Centroids
        centroids = np.array(engine.centroids_2d)
        ax.scatter(centroids[:, 0], centroids[:, 1], c='red', s=160, marker='X', label='Centroids', edgecolor='black', linewidth=1.5)
        
        ax.set_title("2D PCA Spatial Distribution of Japanese Foods", fontsize=14, fontweight='bold')
        ax.set_xlabel("Principal Component 1 (PCA X)")
        ax.set_ylabel("Principal Component 2 (PCA Y)")
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)

    with col_info:
        st.markdown("### Cluster Descriptions" if not is_th else "### คำอธิบายกลุ่มคลัสเตอร์")
        summary_data = engine.get_clusters_summary()
        summary = summary_data.get('clusters', []) if isinstance(summary_data, dict) else summary_data
        for c in summary:
            with st.expander(f"**{c['name']}** ({c['count']} recipes)"):
                for r in c['sample_recipes'][:3]:
                    st.write(f"- {r['title']}")

# TAB 4: Inverted Index
with tabs[3]:
    st.subheader("📖 Inverted Index & Vocabulary Inspector" if not is_th else "📖 ดัชนีคำศัพท์แบบผกผัน (Inverted Index)")
    term_q = st.text_input("Enter term to lookup:" if not is_th else "พิมพ์คำศัพท์เพื่อตรวจสอบ:", value="chicken")
    
    if term_q:
        info = engine.inspect_inverted_index(term_q)
        if info['found']:
            mcol1, mcol2, mcol3 = st.columns(3)
            mcol1.metric("Term", info['term'])
            mcol2.metric("Document Frequency (DF)", info['df'])
            mcol3.metric("Corpus Ratio", f"{(info['df']/info['total_docs'])*100:.1f}%")
            
            st.markdown(f"**Matched Documents ({info['df']}):**")
            st.dataframe(pd.DataFrame(info['sample_postings']), use_container_width=True)
        else:
            st.warning(f"Term '{term_q}' was not found in the vocabulary dictionary.")

# TAB 5: Evaluation
with tabs[4]:
    st.subheader("📈 Information Retrieval Evaluation" if not is_th else "📈 ประเมินผลประสิทธิภาพการสืบค้น (IR Evaluation)")
    ecol1, ecol2 = st.columns([3, 1])
    with ecol1:
        eval_q = st.text_input("Evaluation Query:" if not is_th else "คำค้นหาทดสอบ:", value="chicken teriyaki")
    with ecol2:
        eval_k = st.number_input("Cutoff (K):" if not is_th else "ลำดับตัดเกณฑ์ (K):", min_value=1, max_value=50, value=10)

    if eval_q:
        search_res = engine.search(eval_q, top_k=50)
        retrieved_ids = [r['id'] for r in search_res['results']]
        metrics = engine.compute_evaluation_metrics(retrieved_ids, eval_q, k=eval_k)
        
        mcols = st.columns(4)
        mcols[0].metric("Precision@K", f"{metrics['precision_at_k']:.2f}")
        mcols[1].metric("Recall@K", f"{metrics['recall_at_k']:.2f}")
        mcols[2].metric("Average Precision (AP)", f"{metrics['average_precision']:.2f}")
        mcols[3].metric("True Positives (TP)", f"{metrics['tp']} / {metrics['total_relevant']}")

# TAB 6: Data Pipeline
with tabs[5]:
    st.subheader("⚙️ Data Ingestion Pipeline & Web Scraper" if not is_th else "⚙️ ระบบท่อส่งข้อมูล & เว็บสแครปเปอร์ (Data Pipeline)")
    st.caption("Manage datasets, scrape fresh recipes from Cookpad, clean culinary stopwords, and hot-reload models.")

    status = engine.get_status()
    scol1, scol2, scol3, scol4 = st.columns(4)
    scol1.metric("Total Indexed Recipes" if not is_th else "จำนวนสูตรอาหารในระบบ", status['total_recipes'])
    scol2.metric("Vocabulary Size" if not is_th else "ขนาดคลังคำศัพท์", status['vocabulary_size'])
    scol3.metric("Active Clusters" if not is_th else "จำนวนคลัสเตอร์", status['n_clusters'])
    scol4.metric("Last Updated" if not is_th else "อัปเดตล่าสุด", status['last_updated'])

    st.markdown("---")
    pcol1, pcol2 = st.columns(2)

    with pcol1:
        with st.container(border=True):
            st.markdown("### 🔄 Quick Re-Index & Clean Dataset" if not is_th else "### 🔄 ล้างข้อมูลและ Re-Index ทันที")
            st.write("Re-cleans text with NLTK culinary stopwords and rebuilds TF-IDF & K-Means models from local raw data." if not is_th else "ตัดคำด้วย NLTK ล้าง Culinary Stopwords และฟิตโมเดล TF-IDF + K-Means ใหม่จากไฟล์ข้อมูลเดิม")
            if st.button("Run Quick Re-Index (~1s)" if not is_th else "รัน Re-Index ทันที (~1 วินาที)", type="secondary"):
                with st.spinner("Cleaning text and rebuilding VSM index..."):
                    engine.reindex_existing_data()
                    st.success("Re-indexing completed successfully!" if not is_th else "Re-indexing สำเร็จเรียบร้อย!")
                    st.rerun()

    with pcol2:
        with st.container(border=True):
            st.markdown("### 🌐 Live Cookpad Web Scraper" if not is_th else "### 🌐 ดึงข้อมูลสูตรอาหารสด (Live Web Scraper)")
            st.write("Crawl Japanese recipe pages directly from Cookpad/API, parse ingredients, and rebuild the search engine." if not is_th else "ดึงเมนูอาหารญี่ปุ่นสดจาก Cookpad/API พร้อมสกัดวัตถุดิบและสร้างดัชนีใหม่")
            target_scrape = st.selectbox("Target Recipe Count:" if not is_th else "จำนวนเมนูที่ต้องการดึง:", [10, 20, 50, 100], index=3)
            if st.button("🌐 Start Web Scraping & Rebuild" if not is_th else "🌐 เริ่มต้น Scrape & สร้างดัชนีใหม่", type="primary"):
                with st.spinner(f"Scraping {target_scrape} recipes from Culinary Sources..."):
                    result = engine.run_scraping_pipeline(target_count=target_scrape)
                    if result['success']:
                        st.success(result['message'])
                        st.rerun()
                    else:
                        st.error(f"Scraping failed: {result['error']}")

    st.markdown("#### 💻 Pipeline Log Terminal" if not is_th else "#### 💻 บันทึกการทำงานของระบบ (Pipeline Execution Log)")
    with st.container(border=True):
        for log in status['recent_logs']:
            st.code(log, language="log")
