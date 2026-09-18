/**
 * JAPANESE FOODS INFORMATION RETRIEVAL ENGINE
 * Client-side Controller with Full Bilingual (Thai 🇹🇭 / English 🇬🇧) Localization,
 * Interactive Category Filtering, One-Click Pantry Presets, and IR Evaluation.
 */

// ==================== BILINGUAL TRANSLATION DICTIONARY ====================
const I18N = {
  th: {
    app_title_main: 'JAPANESE FOODS',
    app_title_badge: 'IR ENGINE',
    app_subtitle: '日本料理 情報検索システム · VSM · TF-IDF · Clustering',
    nav_search: 'ค้นหาสูตรอาหาร',
    nav_pantry: 'ค้นจากวัตถุดิบในครัว',
    nav_cluster: 'แผนภาพคลัสเตอร์ (PCA)',
    nav_index: 'ดัชนีคำศัพท์ (Inverted Index)',
    nav_eval: 'ประเมินผลระบบ IR',
    nav_pipeline: 'จัดการข้อมูล & Scraper',
    
    // Search Tab
    hero_title: 'ค้นหาสูตรอาหารญี่ปุ่นด้วยระบบ IR อัจฉริยะ',
    hero_desc: 'ประมวลผลด้วยโมเดล Vector Space Model (VSM), ถ่วงน้ำหนักคำด้วย TF-IDF และขยายคำค้นหาอัตโนมัติด้วย Pseudo-Relevance Feedback',
    category_label: 'หมวดหมู่อาหาร:',
    cat_all: 'ทั้งหมด (All)',
    cat_ramen: 'ราเมน & เส้น (Ramen)',
    cat_curry: 'แกงกะหรี่ & ต้ม (Curry)',
    cat_yakitori: 'ไก่ย่าง & เนื้อ (Meat)',
    cat_donburi: 'ข้าวหน้า & เบนโตะ (Donburi)',
    cat_tofu: 'สลัด & เต้าหู้ (Tofu/Salad)',
    cat_dessert: 'ขนมหวาน & มัทฉะ (Dessert)',
    search_placeholder: 'พิมพ์ชื่อเมนู หรือวัตถุดิบ (เช่น ramen, teriyaki chicken, curry, miso, sando)...',
    btn_search: 'ค้นหา',
    suggestions_label: 'คำค้นแนะนำ:',
    exp_title: 'ขยายคำค้นหาอัตโนมัติ (Dynamic Query Expansion)',
    exp_orig: 'คำค้นหาเดิม:',
    exp_final: 'คำค้นหาที่ขยายแล้ว:',
    exp_added: 'คำที่ระบบเพิ่มเข้ามา:',
    filter_cluster_label: 'กรองตามคลัสเตอร์:',
    cluster_all: 'ทุกสูตรอาหาร',
    loading_search: 'กำลังคำนวณค่าความคล้ายคลึง Cosine Similarity...',
    empty_search_title: 'ไม่พบสูตรอาหารที่ตรงกับคำค้นหา',
    empty_search_desc: 'ลองเปลี่ยนคำค้นหา หรือเลือกหมวดหมู่อาหารอื่นด้านบน',
    showing_results: 'พบ {count} สูตรอาหาร',

    // Pantry Tab
    pantry_title: 'ค้นหาสูตรอาหารจากวัตถุดิบในตู้เย็น (Pantry Matcher)',
    pantry_desc: 'เลือกวัตถุดิบที่มีอยู่ในครัว หรือกดปุ่มเมนูลัด ระบบ VSM จะคำนวณและแนะนำเมนูญี่ปุ่นที่มีสัดส่วนวัตถุดิบตรงกับที่คุณมีมากที่สุด',
    preset_title: 'ชุดวัตถุดิบสำเร็จรูป (One-Click Presets)',
    preset_desc: 'คลิกเพื่อเลือกชุดวัตถุดิบยอดนิยมทันที',
    preset_noodle_title: 'มื้อด่วนราเมน/อุด้ง',
    preset_izakaya_title: 'ชุดปาร์ตี้อิซากายะ',
    preset_curry_title: 'ข้าวแกงกะหรี่อบอุ่น',
    preset_healthy_title: 'ชุดสุขภาพ & เต้าหู้',
    preset_bento_title: 'ข้าวกล่องเบนโตะ',
    common_ing_title: 'เลือกวัตถุดิบอาหารญี่ปุ่น',
    common_ing_desc: 'คลิกเพื่อเลือกหรือยกเลิกวัตถุดิบ',
    custom_ing_placeholder: 'เพิ่มวัตถุดิบอื่น (เช่น dashi, mirin, sake)...',
    btn_add_ing: '+ เพิ่ม',
    selected_ing_label: 'วัตถุดิบที่เลือก',
    btn_clear_all: 'ล้างทั้งหมด',
    no_ing_selected: 'ยังไม่ได้เลือกวัตถุดิบ',
    btn_find_pantry: 'ค้นหาเมนูอาหารที่ทำได้',
    matched_recipes_title: 'เมนูที่ตรงกับวัตถุดิบของคุณ',
    status_ready: 'พร้อมทำงาน',
    pantry_empty_title: 'เลือกวัตถุดิบทางด้านซ้ายเพื่อเริ่มค้นหา',
    pantry_empty_desc: 'เลือกวัตถุดิบพื้นฐาน เช่น chicken, soy sauce, sake, egg หรือคลิกชุด Presets ด้านบน',
    have_tag: 'มี:',
    need_tag: 'ขาดอีก:',
    cook_recipe_link: 'ดูวิธีทำเมนูนี้ →',

    // Cluster Tab
    cluster_title: 'แผนภาพการจัดกลุ่มเมนูอาหาร (K-Means & 2D PCA)',
    cluster_desc: 'สูตรอาหารทั้งหมดถูกจัดกลุ่มเป็น 6 คลัสเตอร์ตามคุณลักษณะ TF-IDF และลดมิติข้อมูลลงสู่ระนาบ 2D ด้วย Principal Component Analysis (PCA)',
    pca_chart_title: 'การกระจายตัวของสูตรอาหารในระนาบ 2D PCA',
    cluster_overview_title: 'ภาพรวมกลุ่มเมนูอาหาร (6 คลัสเตอร์)',
    contains_recipes: 'บรรจุ {count} สูตรอาหาร',
    top_samples: 'ตัวอย่างเมนูเด่น:',

    // Inverted Index Tab
    index_title: 'ดัชนีคำศัพท์แบบผกผัน (Inverted Index Inspector)',
    index_desc: 'ตรวจสอบความถี่การปรากฏในเอกสาร (Document Frequency: DF) และรายการชี้เอกสาร (Postings List) ของคำศัพท์แต่ละคำในคลังข้อมูล',
    index_lookup_title: 'ค้นหาคำศัพท์ใน Inverted Index',
    term_placeholder: 'พิมพ์คำศัพท์ (เช่น chicken, dashi, soy, miso, ramen)...',
    btn_inspect: 'ตรวจสอบ Postings',
    quick_lookup_label: 'คำศัพท์ยอดนิยม:',
    metric_term_label: 'คำศัพท์ (Term)',
    metric_df_label: 'Document Frequency (DF)',
    metric_idf_label: 'อัตราส่วนความครอบคลุม',
    postings_matched_title: 'Postings List (เอกสารที่พบคำศัพท์นี้):',
    term_not_found: 'ไม่พบคำศัพท์ "{term}" ในคลังดัชนี',

    // Evaluation Tab
    eval_title: 'กระดานประเมินประสิทธิภาพระบบสืบค้น (IR Evaluation)',
    eval_desc: 'วัดผลคุณภาพการสืบค้นข้อมูลตามหลักทฤษฎี Information Retrieval ด้วยมาตรวัด Precision@K, Recall@K, Average Precision (AP), และ Mean Average Precision (MAP)',
    eval_run_title: 'ทดสอบประเมินคำค้นหา (Query Benchmark)',
    eval_query_label: 'คำค้นหาทดสอบ (Query):',
    eval_k_label: 'ลำดับตัดเกณฑ์ (Cutoff Rank K):',
    btn_compute_metrics: 'คำนวณผลการประเมิน',
    benchmark_suite_label: 'ชุดคำถามทดสอบมาตรฐาน (Benchmark Suite):',
    metric_pk_desc: 'สัดส่วนเอกสารที่ตรงความต้องการ ในบรรดา K ลำดับแรกที่ดึงมา',
    metric_rk_desc: 'สัดส่วนเอกสารที่ดึงมาได้ ต่อจำนวนเอกสารที่เกี่ยวข้องทั้งหมดในระบบ',
    metric_ap_desc: 'พื้นที่ใต้กราฟ Precision-Recall โดยคำนึงถึงลำดับความสำคัญของเอกสาร',
    confusion_metrics_title: 'Confusion Metrics',
    total_rel_label: 'เอกสารที่เกี่ยวข้องทั้งหมด:',
    history_table_title: 'ประวัติการประเมินในเซสชัน & ค่า Mean Average Precision (MAP)',
    history_table_desc: 'ค่า MAP คำนวณจากค่าเฉลี่ยของ Average Precision ทุกคำค้นหาที่ทดสอบในเซสชันนี้',
    th_query: 'คำค้นหา (Query)',
    empty_history_text: 'ยังไม่มีประวัติการประเมินในเซสชันนี้ ลองกดปุ่มทดสอบด้านบน',

    // Pipeline Tab
    pipeline_title: 'ระบบท่อส่งข้อมูล & เว็บสแครปเปอร์ (Data Pipeline)',
    pipeline_desc: 'จัดการชุดข้อมูลสูตรอาหารญี่ปุ่น สั่งดึงข้อมูลสดจากเว็บไซต์ Cookpad/Culinary API, ล้าง Stopwords และสร้างโมเดล VSM ใหม่แบบ Hot-Reload',
    stat_recipes_title: 'จำนวนสูตรอาหารในระบบ',
    stat_vocab_title: 'ขนาดคลังคำศัพท์ (Vocabulary)',
    stat_vocab_desc: 'จำนวน Unique Tokens ใน TF-IDF Matrix',
    stat_clusters_title: 'จำนวนคลัสเตอร์ (K-Means)',
    stat_clusters_desc: 'กลุ่มแบ่งตามลักษณะวัตถุดิบ',
    stat_updated_title: 'อัปเดตล่าสุด',
    stat_updated_desc: 'เวลาการโหลดโมเดลเข้า RAM',
    card_reindex_title: 'ล้างข้อมูลและ Re-Index ทันที',
    card_reindex_desc: 'ตัดคำด้วย NLTK ล้าง Culinary Stopwords และฟิตโมเดล TF-IDF + K-Means ใหม่จากไฟล์ข้อมูลเดิม',
    speed_instant: 'รวดเร็ว (~1 วินาที)',
    btn_run_reindex: 'รัน Re-Index ทันที',
    card_scrape_title: 'ดึงข้อมูลสูตรอาหารสด (Live Web Scraper)',
    card_scrape_desc: 'Crawl เมนูอาหารญี่ปุ่นจาก Cookpad / Culinary API พร้อมสกัดวัตถุดิบและอัปเดตระบบสืบค้นอัตโนมัติ',
    scrape_amount_label: 'จำนวนเมนูที่ต้องการดึง:',
    btn_start_scrape: 'Scrape & Rebuild Dataset',
    terminal_header: 'บันทึกการทำงานของระบบ (Pipeline Execution Log)',
    btn_clear_logs: 'ล้างประวัติ Log',

    // Modal & Extras
    modal_ing_title: 'รายการวัตถุดิบ (Ingredients):',
    btn_copy_ing: 'คัดลอกวัตถุดิบ',
    btn_copied: 'คัดลอกแล้ว! ✓',
    modal_tokens_title: 'Cleaned IR Tokens (คำสำคัญที่ใช้ในการสืบค้น):',
    btn_view_cookpad: 'ดูสูตรต้นฉบับบนเว็บ Cookpad ↗',
    footer_credit: 'พัฒนาด้วยทฤษฎี Vector Space Model (VSM), TF-IDF Cosine Similarity, Pseudo-Relevance Feedback (PRF), K-Means Clustering, และ 2D PCA'
  },

  en: {
    app_title_main: 'JAPANESE FOODS',
    app_title_badge: 'IR ENGINE',
    app_subtitle: 'Information Retrieval System · VSM · TF-IDF · K-Means',
    nav_search: 'Recipe Search',
    nav_pantry: 'Pantry Matcher',
    nav_cluster: 'Cluster Map (PCA)',
    nav_index: 'Inverted Index',
    nav_eval: 'IR Evaluation',
    nav_pipeline: 'Data Pipeline & Scraper',

    // Search Tab
    hero_title: 'Discover Japanese Culinary Recipes',
    hero_desc: 'Powered by Vector Space Model (VSM), TF-IDF Term Weighting, and Pseudo-Relevance Feedback (Query Expansion)',
    category_label: 'Food Categories:',
    cat_all: 'All Recipes',
    cat_ramen: 'Ramen & Noodles',
    cat_curry: 'Curry & Stews',
    cat_yakitori: 'Yakitori & Meat',
    cat_donburi: 'Rice & Donburi',
    cat_tofu: 'Salad & Tofu',
    cat_dessert: 'Desserts & Matcha',
    search_placeholder: 'Search dish or ingredients (e.g. ramen, teriyaki chicken, curry, miso, sando)...',
    btn_search: 'Search',
    suggestions_label: 'Quick Suggestions:',
    exp_title: 'Dynamic Query Expansion (PRF)',
    exp_orig: 'Original Query:',
    exp_final: 'Expanded Query:',
    exp_added: 'Dynamically Added Concepts:',
    filter_cluster_label: 'Filter by Cluster:',
    cluster_all: 'All Recipes',
    loading_search: 'Retrieving documents & computing Cosine Similarities...',
    empty_search_title: 'No matching recipes found',
    empty_search_desc: 'Try searching with another culinary keyword or choose a category above.',
    showing_results: 'Found {count} recipes',

    // Pantry Tab
    pantry_title: 'Japanese Pantry & Fridge Matcher',
    pantry_desc: 'Select ingredients in your fridge or choose a preset. Our VSM engine matches recipes with highest overlap and cosine similarity.',
    preset_title: 'One-Click Culinary Presets',
    preset_desc: 'Quickly populate common ingredient combinations',
    preset_noodle_title: 'Easy Noodle Night',
    preset_izakaya_title: 'Izakaya Party Skewers',
    preset_curry_title: 'Comfort Curry Dinner',
    preset_healthy_title: 'Healthy Greens & Tofu',
    preset_bento_title: 'Bento Box Essentials',
    common_ing_title: 'Select Japanese Ingredients',
    common_ing_desc: 'Click chips to toggle ingredients in your pantry',
    custom_ing_placeholder: 'Add custom ingredient (e.g. dashi, mirin, sake)...',
    btn_add_ing: '+ Add',
    selected_ing_label: 'Selected Ingredients',
    btn_clear_all: 'Clear All',
    no_ing_selected: 'No ingredients selected yet',
    btn_find_pantry: 'Find Matching Recipes',
    matched_recipes_title: 'Matched Japanese Recipes',
    status_ready: 'Ready',
    pantry_empty_title: 'Select ingredients on the left to start',
    pantry_empty_desc: 'Pick common staples like chicken, soy sauce, sake, egg, or click presets above.',
    have_tag: 'Have:',
    need_tag: 'Need:',
    cook_recipe_link: 'Cook this Recipe →',

    // Cluster Tab
    cluster_title: 'Japanese Recipe Clustering (K-Means & 2D PCA)',
    cluster_desc: 'All recipes are grouped into 6 clusters based on TF-IDF vectors and projected onto a 2D plane using Principal Component Analysis (PCA).',
    pca_chart_title: '2D PCA Recipe Spatial Distribution',
    cluster_overview_title: 'Culinary Clusters Overview (K=6)',
    contains_recipes: 'Contains {count} recipes',
    top_samples: 'Top Samples:',

    // Inverted Index Tab
    index_title: 'Inverted Index & Vocabulary Inspector',
    index_desc: 'Inspect Document Frequency (DF) and Postings Lists for vocabulary terms indexed in the IR engine.',
    index_lookup_title: 'Lookup Vocabulary Term',
    term_placeholder: 'Enter term (e.g. chicken, dashi, soy, miso, ramen)...',
    btn_inspect: 'Inspect Postings',
    quick_lookup_label: 'Popular Terms:',
    metric_term_label: 'Vocabulary Term',
    metric_df_label: 'Document Frequency (DF)',
    metric_idf_label: 'Corpus Coverage Ratio',
    postings_matched_title: 'Postings List (Matched Documents):',
    term_not_found: 'Term "{term}" was not found in the index dictionary',

    // Evaluation Tab
    eval_title: 'Information Retrieval Evaluation Dashboard',
    eval_desc: 'Evaluate retrieval quality using standard IR metrics: Precision@K, Recall@K, Average Precision (AP), and Mean Average Precision (MAP).',
    eval_run_title: 'Query Benchmark Test',
    eval_query_label: 'Test Query:',
    eval_k_label: 'Cutoff Rank (K):',
    btn_compute_metrics: 'Compute Metrics',
    benchmark_suite_label: 'Standard Benchmark Suite:',
    metric_pk_desc: 'Fraction of top-K retrieved recipes that are relevant.',
    metric_rk_desc: 'Fraction of all relevant recipes in corpus retrieved in top-K.',
    metric_ap_desc: 'Area under the Precision-Recall curve considering ranking order.',
    confusion_metrics_title: 'Confusion Metrics',
    total_rel_label: 'Total Relevant in Corpus:',
    history_table_title: 'Session Evaluation History & Mean Average Precision (MAP)',
    history_table_desc: 'MAP is the mean of Average Precision scores computed across all queries in this session.',
    th_query: 'Query',
    empty_history_text: 'No evaluation tests performed in this session yet.',

    // Pipeline Tab
    pipeline_title: 'Data Ingestion Pipeline & Web Scraper',
    pipeline_desc: 'Manage Japanese recipe dataset, trigger live web scraping from Cookpad/Culinary API, clean stopwords, and hot-reload models.',
    stat_recipes_title: 'Total Indexed Recipes',
    stat_vocab_title: 'Vocabulary Size (Tokens)',
    stat_vocab_desc: 'Unique features in TF-IDF Matrix',
    stat_clusters_title: 'Active Clusters (K-Means)',
    stat_clusters_desc: 'Categorized by ingredient traits',
    stat_updated_title: 'Last Updated',
    stat_updated_desc: 'In-memory model timestamp',
    card_reindex_title: 'Quick Clean & Re-Index',
    card_reindex_desc: 'Tokenize with NLTK, remove culinary stopwords, and re-fit TF-IDF & K-Means from local raw files.',
    speed_instant: 'Instant (~1 sec)',
    btn_run_reindex: 'Run Quick Re-Index',
    card_scrape_title: 'Live Cookpad Web Scraper',
    card_scrape_desc: 'Crawl fresh Japanese recipes from Cookpad / Culinary APIs, extract ingredients, and rebuild search index.',
    scrape_amount_label: 'Target Recipes Count:',
    btn_start_scrape: 'Scrape & Rebuild Dataset',
    terminal_header: 'Pipeline Execution Log Terminal',
    btn_clear_logs: 'Clear Logs',

    // Modal & Extras
    modal_ing_title: 'Recipe Ingredients:',
    btn_copy_ing: 'Copy Ingredients',
    btn_copied: 'Copied! ✓',
    modal_tokens_title: 'Cleaned IR Tokens (Indexed Features):',
    btn_view_cookpad: 'View Original Recipe on Cookpad ↗',
    footer_credit: 'Built with Vector Space Model (VSM), TF-IDF Cosine Similarity, Pseudo-Relevance Feedback, K-Means Clustering, and 2D PCA.'
  }
};

// Tooltip educational descriptions
const IR_TOOLTIPS = {
  th: {
    prf_info: {
      title: 'Pseudo-Relevance Feedback (PRF)',
      body: 'อัลกอริทึมขยายคำค้นหาอัตโนมัติ โดยระบบจะถือว่าผลลัพธ์ 10 อันดับแรกที่ดึงมาเป็นเอกสารที่เกี่ยวข้อง (Relevant) และดึงคำศัพท์ที่มีความถี่ร่วมสูงสุดมาต่อท้ายคำค้นหาเดิม เพื่อเพิ่มค่า Recall โดยที่ผู้ใช้ไม่ต้องพิมพ์คำเพิ่มเอง'
    },
    pca_info: {
      title: '2D PCA & K-Means Clustering',
      body: 'สูตรอาหารในระบบมีเวกเตอร์คำศัพท์หลายร้อยมิติ เราใช้ Principal Component Analysis (PCA) ในการลดมิติข้อมูลลงเหลือ 2 มิติหลัก (X, Y) เพื่อนำมาพล็อตแสดงผลบนระนาบ 2D ให้เห็นการเกาะกลุ่มของเมนูอาหารที่มีวัตถุดิบใกล้เคียงกัน'
    },
    inverted_index_info: {
      title: 'Inverted Index (ดัชนีแบบผกผัน)',
      body: 'โครงสร้างข้อมูลหลักในระบบ Information Retrieval ที่แมปคำศัพท์แต่ละคำ (Term) ไปยังรายการเอกสารทั้งหมดที่มีคำนี้ปรากฏอยู่ (Postings List) ช่วยให้ค้นหาเอกสารได้ในเวลา O(1) โดยไม่ต้องสแกนทุกสูตรอาหาร'
    },
    eval_info: {
      title: 'IR Evaluation Metrics',
      body: 'การวัดผลระบบสืบค้นข้อมูล ใช้คำนวณความแม่นยำ (Precision) และความครอบคลุม (Recall) เทียบกับชุดเอกสารที่เกี่ยวข้องจริงในคลังข้อมูล'
    },
    precision_info: {
      title: 'Precision@K (P@K)',
      body: 'สูตร: TP / K\nวัดสัดส่วนว่าในจำนวนผลลัพธ์ K รายการแรกที่ระบบดึงมา มีกี่เปอร์เซ็นต์ที่เป็นเมนูที่ตรงกับความต้องการจริงๆ'
    },
    recall_info: {
      title: 'Recall@K (R@K)',
      body: 'สูตร: TP / Total Relevant\nวัดสัดส่วนว่าในบรรดาสูตรอาหารทั้งหมดที่เกี่ยวข้องในระบบ เราดึงขึ้นมาได้แล้วกี่เปอร์เซ็นต์ใน K ลำดับแรก'
    },
    ap_info: {
      title: 'Average Precision (AP)',
      body: 'คำนวณพื้นที่ใต้กราฟ Precision-Recall โดยให้รางวัลสูงกับระบบที่จัดอันดับเอกสารที่เกี่ยวข้องไว้ในลำดับต้นๆ (Top Ranks)'
    },
    confusion_info: {
      title: 'Confusion Matrix',
      body: 'TP (True Positives): ดึงมาและเกี่ยวข้องจริง\nFP (False Positives): ดึงมาแต่ไม่เกี่ยวข้อง\nFN (False Negatives): เกี่ยวข้องแต่ระบบไม่ได้ดึงมา'
    }
  },
  en: {
    prf_info: {
      title: 'Pseudo-Relevance Feedback (PRF)',
      body: 'An automated query expansion technique that assumes top-10 retrieved documents are relevant. It extracts the most frequent co-occurring culinary concepts and appends them to the original query to improve recall.'
    },
    pca_info: {
      title: '2D PCA & K-Means Clustering',
      body: 'Recipe vectors span hundreds of dimensions. Principal Component Analysis (PCA) reduces these into 2 principal orthogonal components (X, Y) for 2D spatial visualization of culinary groupings.'
    },
    inverted_index_info: {
      title: 'Inverted Index Architecture',
      body: 'Core IR data structure mapping each vocabulary term to a postings list of document IDs. Enables sub-millisecond retrieval without scanning the full corpus.'
    },
    eval_info: {
      title: 'IR Evaluation Metrics',
      body: 'Standard evaluation framework measuring retrieval precision, recall, ranking quality, and Mean Average Precision against ground-truth culinary relevance.'
    },
    precision_info: {
      title: 'Precision@K (P@K)',
      body: 'Formula: TP / K\nMeasures the percentage of relevant recipes within the top-K retrieved results.'
    },
    recall_info: {
      title: 'Recall@K (R@K)',
      body: 'Formula: TP / Total Relevant\nMeasures what percentage of all relevant recipes in the corpus were retrieved within the top-K cutoff.'
    },
    ap_info: {
      title: 'Average Precision (AP)',
      body: 'Area under the Precision-Recall curve, weighting earlier relevant retrievals more heavily than later ones.'
    },
    confusion_info: {
      title: 'Confusion Matrix',
      body: 'TP (True Positives): Retrieved & Relevant\nFP (False Positives): Retrieved but Irrelevant\nFN (False Negatives): Relevant but missed'
    }
  }
};

// ==================== APPLICATION STATE ====================
const state = {
  lang: localStorage.getItem('food_ir_lang') || 'th',
  theme: localStorage.getItem('food_ir_theme') || 'dark',
  currentQuery: '',
  activeCluster: 'all',
  activeCategory: 'all',
  selectedPantryIngredients: new Set(),
  clusterData: [],
  pcaChart: null,
  evalHistory: [],
  debounceTimer: null
};

// Common Japanese Pantry Staples
const COMMON_PANTRY_STAPLES = [
  'chicken', 'pork', 'beef', 'salmon', 'tuna', 'egg', 'tofu',
  'soy sauce', 'sake', 'mirin', 'dashi', 'miso', 'sesame oil',
  'ginger', 'garlic', 'green onion', 'onion', 'carrot', 'potato',
  'nori', 'ramen', 'udon', 'soba', 'rice', 'curry roux', 'cabbage'
];

// Presets Data Mapping
const PANTRY_PRESETS = {
  noodle: ['udon', 'dashi', 'soy sauce', 'green onion', 'egg', 'mirin'],
  izakaya: ['chicken', 'tare sauce', 'sake', 'garlic', 'ginger', 'soy sauce', 'sesame oil'],
  curry: ['curry roux', 'onion', 'carrot', 'potato', 'chicken', 'pork', 'soy sauce'],
  healthy: ['tofu', 'spinach', 'sesame oil', 'miso', 'cucumber', 'dashi'],
  bento: ['rice', 'salmon', 'nori', 'egg', 'mirin', 'soy sauce', 'sesame seeds']
};

// DOM Element Registry
const elements = {};

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', () => {
  cacheDOMElements();
  initLanguage();
  initTheme();
  initNavigation();
  initSearch();
  initPantry();
  initClusterMap();
  initInvertedIndex();
  initEvaluation();
  initPipeline();
  initModal();
  initTooltips();

  // Initial Load
  performSearch('');
  fetchPipelineStatus();
});

function cacheDOMElements() {
  // Navigation & Controls
  elements.langToggleBtn = document.getElementById('lang-toggle-btn');
  elements.langFlagIcon = document.getElementById('lang-flag-icon');
  elements.langTextLabel = document.getElementById('lang-text-label');
  elements.themeToggleBtn = document.getElementById('theme-toggle-btn');
  elements.navTabs = document.querySelectorAll('.nav-tab');
  elements.tabContents = document.querySelectorAll('.tab-content');

  // Search Tab
  elements.searchInput = document.getElementById('recipe-search-input');
  elements.searchBtn = document.getElementById('search-btn');
  elements.searchClearBtn = document.getElementById('search-clear-btn');
  elements.categoryChips = document.querySelectorAll('.category-chip');
  elements.quickTags = document.querySelectorAll('.quick-tag');
  elements.queryExpansionCard = document.getElementById('query-expansion-card');
  elements.expOriginalQuery = document.getElementById('exp-original-query');
  elements.expFinalQuery = document.getElementById('exp-final-query');
  elements.addedTermsRow = document.getElementById('added-terms-row');
  elements.addedTermsContainer = document.getElementById('added-terms-container');
  elements.clusterFilterGroup = document.getElementById('cluster-filter-group');
  elements.clusterPills = document.querySelectorAll('.cluster-pill');
  elements.resultsCountText = document.getElementById('results-count-text');
  elements.searchLoading = document.getElementById('search-loading');
  elements.recipesGrid = document.getElementById('recipes-grid');
  elements.emptyState = document.getElementById('empty-state');

  // Pantry Tab
  elements.commonIngChips = document.getElementById('common-ingredients-chips');
  elements.customIngInput = document.getElementById('custom-ingredient-input');
  elements.addIngBtn = document.getElementById('add-ingredient-btn');
  elements.selectedPantryPills = document.getElementById('selected-pantry-pills');
  elements.selectedIngCount = document.getElementById('selected-ing-count');
  elements.clearPantryBtn = document.getElementById('clear-pantry-btn');
  elements.pantrySearchBtn = document.getElementById('pantry-search-btn');
  elements.pantryResultsBadge = document.getElementById('pantry-results-badge');
  elements.pantryResultsGrid = document.getElementById('pantry-results-grid');
  elements.presetBtns = document.querySelectorAll('.preset-btn');

  // Cluster Tab
  elements.pcaCanvas = document.getElementById('pcaClusterChart');
  elements.clusterCardsList = document.getElementById('cluster-cards-list');

  // Index Tab
  elements.termLookupInput = document.getElementById('term-lookup-input');
  elements.lookupTermBtn = document.getElementById('lookup-term-btn');
  elements.termDetailsBox = document.getElementById('term-details-box');
  elements.metricTermName = document.getElementById('metric-term-name');
  elements.metricTermDf = document.getElementById('metric-term-df');
  elements.metricTermIdf = document.getElementById('metric-term-idf');
  elements.termPostingsList = document.getElementById('term-postings-list');
  elements.termQuickBtns = document.querySelectorAll('.term-quick-btn');

  // Evaluation Tab
  elements.evalQueryInput = document.getElementById('eval-query-input');
  elements.evalKInput = document.getElementById('eval-k-input');
  elements.runEvalBtn = document.getElementById('run-eval-btn');
  elements.benchmarkPills = document.querySelectorAll('.benchmark-pill');
  elements.metricPk = document.getElementById('metric-pk');
  elements.metricRk = document.getElementById('metric-rk');
  elements.metricAp = document.getElementById('metric-ap');
  elements.metricTp = document.getElementById('metric-tp');
  elements.metricFp = document.getElementById('metric-fp');
  elements.metricFn = document.getElementById('metric-fn');
  elements.metricTotalRel = document.getElementById('metric-total-rel');
  elements.evalHistoryTbody = document.getElementById('eval-history-tbody');
  elements.sessionMapScore = document.getElementById('session-map-score');

  // Pipeline Tab
  elements.pipelineTotalRecipes = document.getElementById('pipeline-total-recipes');
  elements.pipelineVocabSize = document.getElementById('pipeline-vocab-size');
  elements.pipelineClustersCount = document.getElementById('pipeline-clusters-count');
  elements.pipelineLastUpdated = document.getElementById('pipeline-last-updated');
  elements.quickReindexBtn = document.getElementById('quick-reindex-btn');
  elements.scrapeAmountSelect = document.getElementById('scrape-amount-select');
  elements.startScrapingBtn = document.getElementById('start-scraping-btn');
  elements.pipelineTerminalBody = document.getElementById('pipeline-terminal-body');
  elements.clearLogsBtn = document.getElementById('clear-logs-btn');

  // Modal
  elements.recipeModal = document.getElementById('recipe-modal');
  elements.modalCloseBtn = document.getElementById('modal-close-btn');
  elements.modalClusterBadge = document.getElementById('modal-cluster-badge');
  elements.modalRecipeTitle = document.getElementById('modal-recipe-title');
  elements.modalRecipeScore = document.getElementById('modal-recipe-score');
  elements.modalIngredientsText = document.getElementById('modal-ingredients-text');
  elements.modalCleanedTokens = document.getElementById('modal-cleaned-tokens');
  elements.modalExternalLink = document.getElementById('modal-external-link');
  elements.copyIngredientsBtn = document.getElementById('copy-ingredients-btn');

  // Tooltip
  elements.irTooltipPopup = document.getElementById('ir-tooltip-popup');
  elements.irTooltipTitle = document.getElementById('ir-tooltip-title');
  elements.irTooltipBody = document.getElementById('ir-tooltip-body');
  elements.irTooltipClose = document.getElementById('ir-tooltip-close');
}

// ==================== BILINGUAL LANGUAGE ENGINE ====================
function initLanguage() {
  setLanguage(state.lang);

  if (elements.langToggleBtn) {
    elements.langToggleBtn.addEventListener('click', () => {
      const nextLang = state.lang === 'th' ? 'en' : 'th';
      setLanguage(nextLang);
    });
  }
}

function setLanguage(lang) {
  state.lang = lang;
  localStorage.setItem('food_ir_lang', lang);
  document.documentElement.lang = lang;

  const dict = I18N[lang] || I18N.th;

  // Update button display
  if (elements.langFlagIcon && elements.langTextLabel) {
    if (lang === 'th') {
      elements.langFlagIcon.textContent = '🇹🇭';
      elements.langTextLabel.textContent = 'ภาษาไทย';
    } else {
      elements.langFlagIcon.textContent = '🇬🇧';
      elements.langTextLabel.textContent = 'English';
    }
  }

  // Update text nodes with [data-i18n]
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  // Update Placeholders
  if (elements.searchInput) elements.searchInput.placeholder = dict.search_placeholder;
  if (elements.customIngInput) elements.customIngInput.placeholder = dict.custom_ing_placeholder;
  if (elements.termLookupInput) elements.termLookupInput.placeholder = dict.term_placeholder;

  // Re-render components with localized text
  if (state.currentQuery !== undefined) {
    performSearch(state.currentQuery, false);
  }
  renderSelectedPantryPills();
}

function t(key, replacements = {}) {
  const dict = I18N[state.lang] || I18N.th;
  let text = dict[key] || key;
  for (const [k, v] of Object.entries(replacements)) {
    text = text.replace(`{${k}}`, v);
  }
  return text;
}

// ==================== THEME MANAGEMENT ====================
function initTheme() {
  applyTheme(state.theme);

  if (elements.themeToggleBtn) {
    elements.themeToggleBtn.addEventListener('click', () => {
      const nextTheme = state.theme === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
    });
  }
}

function applyTheme(theme) {
  state.theme = theme;
  localStorage.setItem('food_ir_theme', theme);
  const sunSvg = `<svg class="svg-icon theme-icon-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
  const moonSvg = `<svg class="svg-icon theme-icon-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

  if (theme === 'light') {
    document.body.classList.remove('theme-dark');
    document.body.classList.add('theme-light');
    if (elements.themeToggleBtn) {
      elements.themeToggleBtn.innerHTML = `<span class="theme-icon" aria-hidden="true">${sunSvg}</span>`;
      elements.themeToggleBtn.setAttribute('aria-label', 'Switch to Dark Mode');
    }
  } else {
    document.body.classList.remove('theme-light');
    document.body.classList.add('theme-dark');
    if (elements.themeToggleBtn) {
      elements.themeToggleBtn.innerHTML = `<span class="theme-icon" aria-hidden="true">${moonSvg}</span>`;
      elements.themeToggleBtn.setAttribute('aria-label', 'Switch to Light Mode');
    }
  }
  if (state.pcaChart) renderPCAChart();
}

// ==================== NAVIGATION TABS & DEEP LINKING ====================
function initNavigation() {
  elements.navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetTabId = tab.getAttribute('data-tab');
      switchTab(targetTabId, true);
    });
  });

  // URL Hash Deep Linking
  window.addEventListener('hashchange', () => {
    const hash = window.location.hash.replace('#', '');
    if (hash && !hash.startsWith('recipe-')) {
      switchTab(`${hash}-tab`, false);
    }
  });

  // Initial tab from URL hash if present
  const initialHash = window.location.hash.replace('#', '');
  if (initialHash && !initialHash.startsWith('recipe-')) {
    switchTab(`${initialHash}-tab`, false);
  }
}

function switchTab(targetTabId, updateHash = true) {
  const tabBtn = document.querySelector(`.nav-tab[data-tab="${targetTabId}"]`);
  const targetContent = document.getElementById(targetTabId);
  if (!tabBtn || !targetContent) return;

  elements.navTabs.forEach(t => {
    t.classList.remove('active');
    t.setAttribute('aria-selected', 'false');
  });
  elements.tabContents.forEach(c => c.classList.remove('active'));

  tabBtn.classList.add('active');
  tabBtn.setAttribute('aria-selected', 'true');
  targetContent.classList.add('active');

  if (updateHash) {
    const hashName = targetTabId.replace('-tab', '');
    history.replaceState(null, '', `#${hashName}`);
  }

  if (targetTabId === 'cluster-tab') {
    setTimeout(fetchClusterData, 100);
  } else if (targetTabId === 'pipeline-tab') {
    setTimeout(fetchPipelineStatus, 100);
  }
}

// ==================== TAB 1: SEARCH & RETRIEVAL ====================
function initSearch() {
  // Input Typing with Debounce
  elements.searchInput.addEventListener('input', (e) => {
    const val = e.target.value;
    elements.searchClearBtn.style.display = val.length > 0 ? 'block' : 'none';
    clearTimeout(state.debounceTimer);
    state.debounceTimer = setTimeout(() => {
      performSearch(val);
    }, 300);
  });

  // Clear Button
  elements.searchClearBtn.addEventListener('click', () => {
    elements.searchInput.value = '';
    elements.searchClearBtn.style.display = 'none';
    elements.searchInput.focus();
    performSearch('');
  });

  // Search Button
  elements.searchBtn.addEventListener('click', () => {
    performSearch(elements.searchInput.value);
  });

  // Quick Suggestion Pills
  elements.quickTags.forEach(tag => {
    tag.addEventListener('click', () => {
      const query = tag.getAttribute('data-query');
      elements.searchInput.value = query;
      elements.searchClearBtn.style.display = 'block';
      performSearch(query);
    });
  });

  // Category Filter Chips
  elements.categoryChips.forEach(chip => {
    chip.addEventListener('click', () => {
      elements.categoryChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const cat = chip.getAttribute('data-cat');
      state.activeCategory = cat;
      
      let q = '';
      if (cat === 'ramen') q = 'ramen noodle';
      else if (cat === 'curry') q = 'curry';
      else if (cat === 'yakitori') q = 'chicken meatball yakitori';
      else if (cat === 'donburi') q = 'rice bowl';
      else if (cat === 'tofu') q = 'tofu salad';
      else if (cat === 'dessert') q = 'sweet matcha sando';

      elements.searchInput.value = q;
      elements.searchClearBtn.style.display = q ? 'block' : 'none';
      performSearch(q);
    });
  });

  // Cluster Filter Buttons
  elements.clusterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      elements.clusterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      state.activeCluster = pill.getAttribute('data-cluster');
      performSearch(elements.searchInput.value);
    });
  });
}

async function performSearch(query, showSpinner = true) {
  state.currentQuery = query;
  if (showSpinner) {
    elements.searchLoading.style.display = 'block';
    elements.recipesGrid.innerHTML = '';
    elements.emptyState.style.display = 'none';
  }

  try {
    const clusterParam = state.activeCluster !== 'all' ? `&cluster=${state.activeCluster}` : '';
    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}&top_k=24${clusterParam}`);
    const data = await res.json();

    elements.searchLoading.style.display = 'none';
    renderSearchResults(data);
  } catch (err) {
    elements.searchLoading.style.display = 'none';
    console.error('Search API Error:', err);
  }
}

function renderSearchResults(data) {
  // Query Expansion Box
  if (data.added_terms && data.added_terms.length > 0 && data.clean_query) {
    elements.queryExpansionCard.style.display = 'block';
    elements.expOriginalQuery.textContent = data.clean_query;
    elements.expFinalQuery.textContent = data.expanded_query;
    elements.addedTermsContainer.innerHTML = data.added_terms.map(t => `<span class="added-term-pill">+ ${escapeHtml(t)}</span>`).join('');
  } else {
    elements.queryExpansionCard.style.display = 'none';
  }

  // Count Text
  elements.resultsCountText.textContent = t('showing_results', { count: data.total_results || 0 });

  if (!data.results || data.results.length === 0) {
    elements.emptyState.style.display = 'block';
    elements.recipesGrid.innerHTML = '';
    return;
  }

  elements.emptyState.style.display = 'none';
  elements.recipesGrid.innerHTML = data.results.map(r => `
    <div class="recipe-card" data-recipe='${JSON.stringify(r).replace(/'/g, "&apos;")}'>
      <div>
        <div class="recipe-card-header">
          <span class="cluster-badge">${escapeHtml(r.cluster_name || `Cluster ${r.cluster_id + 1}`)}</span>
          <span class="score-badge">Sim: ${(r.score || 0).toFixed(4)}</span>
        </div>
        <h3 class="recipe-card-title">${escapeHtml(r.title)}</h3>
        <p class="recipe-card-snippet">${escapeHtml(r.ingredients || r.cleaned_ingredients || 'Japanese culinary recipe.')}</p>
      </div>
      <div class="recipe-card-footer">
        <span class="view-details-link">${t('cook_recipe_link')}</span>
        <span style="font-family: var(--font-mono); color: var(--text-muted); font-size: 0.75rem;">ID: #${r.id}</span>
      </div>
    </div>
  `).join('');

  // Add Click & Keyboard Listener to open Recipe Modal
  elements.recipesGrid.querySelectorAll('.recipe-card').forEach(card => {
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    card.addEventListener('click', () => {
      const recipeData = JSON.parse(card.getAttribute('data-recipe'));
      openRecipeModal(recipeData);
    });
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const recipeData = JSON.parse(card.getAttribute('data-recipe'));
        openRecipeModal(recipeData);
      }
    });
  });
}

// ==================== TAB 2: PANTRY MATCHER ====================
function initPantry() {
  // Render Common Ingredients Chips
  elements.commonIngChips.innerHTML = COMMON_PANTRY_STAPLES.map(ing => `
    <button class="ingredient-chip" data-ing="${ing}">${ing}</button>
  `).join('');

  elements.commonIngChips.querySelectorAll('.ingredient-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const ing = chip.getAttribute('data-ing');
      togglePantryIngredient(ing, chip);
    });
  });

  // Custom Ingredient Add
  elements.addIngBtn.addEventListener('click', addCustomPantryIngredient);
  elements.customIngInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addCustomPantryIngredient();
  });

  // Clear All
  elements.clearPantryBtn.addEventListener('click', () => {
    state.selectedPantryIngredients.clear();
    elements.commonIngChips.querySelectorAll('.ingredient-chip').forEach(c => c.classList.remove('selected'));
    renderSelectedPantryPills();
    elements.pantryResultsGrid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon" aria-hidden="true">
          <svg class="svg-icon svg-icon-lg" style="width:3rem;height:3rem;color:var(--text-muted);" viewBox="0 0 24 24"><path d="M18 2v4c0 .55-.45 1-1 1h-2a1 1 0 0 1-1-1V2"/><path d="M16 7v15"/><path d="M6 2v7a2 2 0 0 0 2 2v11"/><path d="M9 2v4a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V2"/></svg>
        </div>
        <h3>${t('pantry_empty_title')}</h3>
        <p>${t('pantry_empty_desc')}</p>
      </div>
    `;
    elements.pantryResultsBadge.textContent = t('status_ready');
  });

  // Pantry Search Button
  elements.pantrySearchBtn.addEventListener('click', performPantrySearch);

  // Preset Buttons
  elements.presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const presetKey = btn.getAttribute('data-preset');
      const items = PANTRY_PRESETS[presetKey] || [];
      state.selectedPantryIngredients = new Set(items);
      
      // Update chip active states
      elements.commonIngChips.querySelectorAll('.ingredient-chip').forEach(c => {
        const ing = c.getAttribute('data-ing');
        if (state.selectedPantryIngredients.has(ing)) {
          c.classList.add('selected');
        } else {
          c.classList.remove('selected');
        }
      });

      renderSelectedPantryPills();
      performPantrySearch();
    });
  });
}

function togglePantryIngredient(ing, chipEl) {
  if (state.selectedPantryIngredients.has(ing)) {
    state.selectedPantryIngredients.delete(ing);
    if (chipEl) chipEl.classList.remove('selected');
  } else {
    state.selectedPantryIngredients.add(ing);
    if (chipEl) chipEl.classList.add('selected');
  }
  renderSelectedPantryPills();
}

function addCustomPantryIngredient() {
  const val = elements.customIngInput.value.trim().toLowerCase();
  if (val) {
    state.selectedPantryIngredients.add(val);
    elements.customIngInput.value = '';
    renderSelectedPantryPills();
  }
}

function renderSelectedPantryPills() {
  elements.selectedIngCount.textContent = state.selectedPantryIngredients.size;
  if (state.selectedPantryIngredients.size === 0) {
    elements.selectedPantryPills.innerHTML = `<span class="placeholder-text">${t('no_ing_selected')}</span>`;
    return;
  }

  elements.selectedPantryPills.innerHTML = Array.from(state.selectedPantryIngredients).map(ing => `
    <span class="selected-pantry-pill">
      ${escapeHtml(ing)}
      <span class="remove-pantry-ing" data-ing="${escapeHtml(ing)}">&times;</span>
    </span>
  `).join('');

  elements.selectedPantryPills.querySelectorAll('.remove-pantry-ing').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const ing = e.target.getAttribute('data-ing');
      state.selectedPantryIngredients.delete(ing);
      // Remove active class from chip if exists
      const chip = Array.from(elements.commonIngChips.querySelectorAll('.ingredient-chip')).find(c => c.getAttribute('data-ing') === ing);
      if (chip) chip.classList.remove('selected');
      renderSelectedPantryPills();
    });
  });
}

async function performPantrySearch() {
  if (state.selectedPantryIngredients.size === 0) {
    alert(t('no_ing_selected'));
    return;
  }

  elements.pantryResultsBadge.textContent = 'Matching...';
  elements.pantryResultsGrid.innerHTML = `
    <div class="loading-spinner">
      <div class="spinner"></div>
      <p>${t('loading_search')}</p>
    </div>
  `;

  try {
    const res = await fetch('/api/pantry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ingredients: Array.from(state.selectedPantryIngredients),
        top_k: 15
      })
    });
    const data = await res.json();
    renderPantryResults(data.results || []);
  } catch (err) {
    console.error('Pantry search error:', err);
  }
}

function renderPantryResults(results) {
  elements.pantryResultsBadge.textContent = t('showing_results', { count: results.length });
  if (results.length === 0) {
    elements.pantryResultsGrid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon" aria-hidden="true">
          <svg class="svg-icon svg-icon-lg" style="width:3rem;height:3rem;color:var(--text-muted);" viewBox="0 0 24 24"><path d="M18 2v4c0 .55-.45 1-1 1h-2a1 1 0 0 1-1-1V2"/><path d="M16 7v15"/><path d="M6 2v7a2 2 0 0 0 2 2v11"/><path d="M9 2v4a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V2"/></svg>
        </div>
        <h3>${t('empty_search_title')}</h3>
      </div>
    `;
    return;
  }

  elements.pantryResultsGrid.innerHTML = results.map(r => `
    <div class="recipe-card" role="button" tabindex="0" data-recipe='${JSON.stringify(r).replace(/'/g, "&apos;")}'>
      <div>
        <div class="recipe-card-header">
          <span class="cluster-badge">${escapeHtml(r.cluster_name || `Cluster ${r.cluster_id + 1}`)}</span>
          <span class="score-badge">Match: ${Math.round((r.match_ratio || 0) * 100)}%</span>
        </div>
        <h3 class="recipe-card-title">${escapeHtml(r.title)}</h3>
        <div class="overlap-info">
          <div><span class="overlap-tag-matched">${t('have_tag')}</span> ${(r.matched_ingredients || []).join(', ') || 'General overlap'}</div>
          ${r.missing_ingredients && r.missing_ingredients.length > 0 ? `<div><span class="overlap-tag-missing">${t('need_tag')}</span> ${r.missing_ingredients.join(', ')}</div>` : ''}
        </div>
      </div>
      <div class="recipe-card-footer">
        <span class="view-details-link">${t('cook_recipe_link')}</span>
        <span class="score-badge">Sim: ${(r.score || 0).toFixed(4)}</span>
      </div>
    </div>
  `).join('');

  elements.pantryResultsGrid.querySelectorAll('.recipe-card').forEach(card => {
    card.addEventListener('click', () => {
      const recipeData = JSON.parse(card.getAttribute('data-recipe'));
      openRecipeModal(recipeData);
    });
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const recipeData = JSON.parse(card.getAttribute('data-recipe'));
        openRecipeModal(recipeData);
      }
    });
  });
}

// ==================== TAB 3: CLUSTER MAP (PCA) ====================
function initClusterMap() {
  fetchClusterData();
}

async function fetchClusterData() {
  try {
    const res = await fetch('/api/clusters');
    const data = await res.json();
    state.clusterData = data.clusters || [];
    renderClusterCards(state.clusterData);

    const points = data.points || [];
    renderPCAChart(points, state.clusterData);
  } catch (err) {
    console.error('Cluster fetch error:', err);
  }
}

function renderClusterCards(clusters) {
  const colors = ['#ff4d4f', '#f472b6', '#f59e0b', '#10b981', '#06b6d4', '#8b5cf6'];
  elements.clusterCardsList.innerHTML = clusters.map((c, i) => `
    <div class="cluster-summary-item" style="border-left-color: ${colors[i % colors.length]}">
      <div class="cluster-item-title">${escapeHtml(c.name)}</div>
      <div class="cluster-item-count">${t('contains_recipes', { count: c.count })}</div>
      <div style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.3rem;">
        ${t('top_samples')} ${c.sample_recipes.map(r => r.title).slice(0, 3).join(' · ')}
      </div>
    </div>
  `).join('');
}

function renderPCAChart(recipes = [], clusters = []) {
  if (!elements.pcaCanvas) return;
  if (typeof Chart === 'undefined') {
    if (elements.pcaCanvas.parentElement) {
      elements.pcaCanvas.parentElement.innerHTML = `
        <div class="empty-state" style="padding: 2.5rem 1rem;">
          <div class="empty-icon">📊</div>
          <h3>Chart Visualization Mode</h3>
          <p style="color: var(--text-muted); font-size: 0.85rem;">Chart.js library is running in offline mode. 6 culinary clusters with 100 recipes are active.</p>
        </div>
      `;
    }
    return;
  }
  const ctx = elements.pcaCanvas.getContext('2d');

  if (state.pcaChart) {
    state.pcaChart.destroy();
  }

  const clusterColors = [
    'rgba(255, 77, 79, 0.85)',
    'rgba(244, 114, 182, 0.85)',
    'rgba(245, 158, 11, 0.85)',
    'rgba(16, 185, 129, 0.85)',
    'rgba(6, 182, 212, 0.85)',
    'rgba(139, 92, 246, 0.85)'
  ];

  const datasets = [];

  for (let c = 0; c < 6; c++) {
    const clusterRecipes = recipes.filter(r => r.cluster_id === c);
    const clusterName = clusters && clusters[c] ? clusters[c].name : `Cluster ${c+1}`;

    datasets.push({
      label: clusterName,
      data: clusterRecipes.map(r => ({
        x: r.pca_x,
        y: r.pca_y,
        title: r.title,
        id: r.id
      })),
      backgroundColor: clusterColors[c],
      borderColor: state.theme === 'dark' ? '#1e293b' : '#ffffff',
      borderWidth: 1.5,
      pointRadius: 7,
      pointHoverRadius: 10
    });
  }

  // Centroids
  if (clusters && clusters.length > 0 && clusters[0].centroid) {
    datasets.push({
      label: 'Centroids (✖)',
      data: clusters.map(c => ({ x: c.centroid[0], y: c.centroid[1], title: `${c.name} Centroid` })),
      backgroundColor: '#ffffff',
      borderColor: '#ff4d4f',
      borderWidth: 3,
      pointStyle: 'crossRot',
      pointRadius: 12
    });
  }

  state.pcaChart = new Chart(ctx, {
    type: 'scatter',
    data: { datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Principal Component 1 (PCA X)',
            color: state.theme === 'dark' ? '#94a3b8' : '#475569',
            font: { size: 12, weight: 'bold' }
          },
          grid: { color: state.theme === 'dark' ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)' },
          ticks: { color: state.theme === 'dark' ? '#94a3b8' : '#475569' }
        },
        y: {
          title: {
            display: true,
            text: 'Principal Component 2 (PCA Y)',
            color: state.theme === 'dark' ? '#94a3b8' : '#475569',
            font: { size: 12, weight: 'bold' }
          },
          grid: { color: state.theme === 'dark' ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)' },
          ticks: { color: state.theme === 'dark' ? '#94a3b8' : '#475569' }
        }
      },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: state.theme === 'dark' ? '#f8fafc' : '#0f172a',
            usePointStyle: true,
            boxWidth: 8,
            font: { size: 12, family: "'Plus Jakarta Sans', sans-serif" }
          }
        },
        tooltip: {
          backgroundColor: state.theme === 'dark' ? 'rgba(15, 23, 42, 0.95)' : 'rgba(255, 255, 255, 0.95)',
          titleColor: state.theme === 'dark' ? '#f8fafc' : '#0f172a',
          bodyColor: state.theme === 'dark' ? '#94a3b8' : '#475569',
          borderColor: 'rgba(255, 77, 79, 0.3)',
          borderWidth: 1,
          padding: 10,
          callbacks: {
            label: (ctx) => {
              const item = ctx.raw;
              return `${item.title || 'Recipe'} (X: ${item.x.toFixed(3)}, Y: ${item.y.toFixed(3)})`;
            }
          }
        }
      }
    }
  });
}

// ==================== TAB 4: INVERTED INDEX INSPECTOR ====================
function initInvertedIndex() {
  elements.lookupTermBtn.addEventListener('click', () => {
    lookupTerm(elements.termLookupInput.value);
  });

  elements.termLookupInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') lookupTerm(elements.termLookupInput.value);
  });

  elements.termQuickBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const term = btn.getAttribute('data-term');
      elements.termLookupInput.value = term;
      lookupTerm(term);
    });
  });
}

async function lookupTerm(term) {
  if (!term.trim()) return;
  try {
    const res = await fetch(`/api/inverted_index?term=${encodeURIComponent(term.trim())}`);
    const data = await res.json();
    renderTermDetails(data);
  } catch (err) {
    console.error('Inverted index error:', err);
  }
}

function renderTermDetails(data) {
  elements.termDetailsBox.style.display = 'block';
  elements.metricTermName.textContent = data.term || '-';
  elements.metricTermDf.textContent = data.df || 0;
  const ratio = data.total_docs ? ((data.df / data.total_docs) * 100).toFixed(1) + '%' : '0%';
  elements.metricTermIdf.textContent = ratio;

  if (!data.found || data.sample_postings.length === 0) {
    elements.termPostingsList.innerHTML = `<div class="placeholder-text">${t('term_not_found', { term: data.term })}</div>`;
    return;
  }

  elements.termPostingsList.innerHTML = data.sample_postings.map(p => `
    <div class="posting-item">
      <span class="posting-doc-id">Doc #${p.doc_id}</span>
      <span class="posting-doc-title">${escapeHtml(p.title)}</span>
    </div>
  `).join('');
}

// ==================== TAB 5: IR EVALUATION ====================
function initEvaluation() {
  elements.runEvalBtn.addEventListener('click', () => {
    runEvaluation(elements.evalQueryInput.value, parseInt(elements.evalKInput.value) || 10);
  });

  elements.benchmarkPills.forEach(pill => {
    pill.addEventListener('click', () => {
      const q = pill.getAttribute('data-q');
      const k = parseInt(pill.getAttribute('data-k')) || 10;
      elements.evalQueryInput.value = q;
      elements.evalKInput.value = k;
      runEvaluation(q, k);
    });
  });
}

async function runEvaluation(query, k) {
  if (!query.trim()) return;
  try {
    const res = await fetch('/api/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, k })
    });
    const data = await res.json();
    renderEvalMetrics(data, query, k);
  } catch (err) {
    console.error('Evaluation error:', err);
  }
}

function renderEvalMetrics(data, query, k) {
  elements.metricPk.textContent = data.precision_at_k.toFixed(2);
  elements.metricRk.textContent = data.recall_at_k.toFixed(2);
  elements.metricAp.textContent = data.average_precision.toFixed(2);

  elements.metricTp.textContent = data.tp;
  elements.metricFp.textContent = data.fp;
  elements.metricFn.textContent = data.fn;
  elements.metricTotalRel.textContent = data.total_relevant;

  state.evalHistory.unshift({
    query,
    k,
    p: data.precision_at_k,
    r: data.recall_at_k,
    ap: data.average_precision,
    tp: data.tp,
    total: data.total_relevant
  });

  renderEvalHistory();
}

function renderEvalHistory() {
  if (state.evalHistory.length === 0) return;

  elements.evalHistoryTbody.innerHTML = state.evalHistory.map((item, idx) => `
    <tr>
      <td>${idx + 1}</td>
      <td><b>${escapeHtml(item.query)}</b></td>
      <td>${item.k}</td>
      <td>${item.p.toFixed(2)}</td>
      <td>${item.r.toFixed(2)}</td>
      <td><b>${item.ap.toFixed(2)}</b></td>
      <td>${item.tp} / ${item.total}</td>
    </tr>
  `).join('');

  const meanAp = state.evalHistory.reduce((sum, item) => sum + item.ap, 0) / state.evalHistory.length;
  elements.sessionMapScore.textContent = meanAp.toFixed(2);
}

// ==================== TAB 6: DATA PIPELINE ====================
function initPipeline() {
  if (elements.quickReindexBtn) {
    elements.quickReindexBtn.addEventListener('click', triggerQuickReindex);
  }
  if (elements.startScrapingBtn) {
    elements.startScrapingBtn.addEventListener('click', triggerLiveScraping);
  }
  if (elements.clearLogsBtn) {
    elements.clearLogsBtn.addEventListener('click', () => {
      elements.pipelineTerminalBody.innerHTML = '<div class="log-line">[System] Terminal logs cleared.</div>';
    });
  }
}

async function fetchPipelineStatus() {
  try {
    const res = await fetch('/api/pipeline/status');
    const data = await res.json();

    if (elements.pipelineTotalRecipes) elements.pipelineTotalRecipes.textContent = data.total_recipes;
    if (elements.pipelineVocabSize) elements.pipelineVocabSize.textContent = data.vocabulary_size;
    if (elements.pipelineClustersCount) elements.pipelineClustersCount.textContent = data.n_clusters;
    if (elements.pipelineLastUpdated) elements.pipelineLastUpdated.textContent = data.last_updated;

    if (data.recent_logs && data.recent_logs.length > 0) {
      elements.pipelineTerminalBody.innerHTML = data.recent_logs.map(log => `
        <div class="log-line">${escapeHtml(log)}</div>
      `).join('');
      elements.pipelineTerminalBody.scrollTop = elements.pipelineTerminalBody.scrollHeight;
    }
  } catch (err) {
    console.error('Failed to fetch pipeline status:', err);
  }
}

async function triggerQuickReindex() {
  elements.quickReindexBtn.disabled = true;
  elements.quickReindexBtn.textContent = 'Re-Indexing...';
  appendTerminalLog('[System] Initiating local dataset cleaning & re-indexing...');

  try {
    const res = await fetch('/api/pipeline/reindex', { method: 'POST' });
    const data = await res.json();
    appendTerminalLog(`[Success] ${data.message}`);
    await fetchPipelineStatus();
    performSearch(state.currentQuery || '');
    if (state.clusterData) fetchClusterData();
  } catch (err) {
    appendTerminalLog(`[Error] Re-indexing failed: ${err}`);
  } finally {
    elements.quickReindexBtn.disabled = false;
    elements.quickReindexBtn.textContent = t('btn_run_reindex');
  }
}

async function triggerLiveScraping() {
  const amount = parseInt(elements.scrapeAmountSelect.value) || 20;
  const confirmMsg = state.lang === 'th'
    ? `ยืนยันการเริ่มดึงข้อมูลสด ${amount} เมนูจาก Cookpad / Culinary API? ระบบจะทำการสกัดวัตถุดิบและสร้างโมเดลค้นหาใหม่`
    : `Start live web scraping for ${amount} Japanese recipes? The system will extract ingredients and rebuild the IR index.`;

  if (!confirm(confirmMsg)) return;

  elements.startScrapingBtn.disabled = true;
  elements.startScrapingBtn.textContent = '🌐 Scraping in progress...';
  appendTerminalLog(`[Crawler] Starting live scraping pipeline for target: ${amount} recipes...`);

  const logPoller = setInterval(fetchPipelineStatus, 2000);

  try {
    const res = await fetch('/api/pipeline/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount })
    });
    const data = await res.json();
    clearInterval(logPoller);

    if (data.success) {
      appendTerminalLog(`[Complete] ${data.message}`);
      alert(`Scraping finished! Indexed ${data.recipes_count} recipes in ${data.elapsed_seconds}s.`);
    } else {
      appendTerminalLog(`[Error] Scraping failed: ${data.error}`);
    }

    await fetchPipelineStatus();
    performSearch(state.currentQuery || '');
    if (state.clusterData) fetchClusterData();
  } catch (err) {
    clearInterval(logPoller);
    appendTerminalLog(`[Error] Network error during scraping: ${err}`);
  } finally {
    elements.startScrapingBtn.disabled = false;
    elements.startScrapingBtn.textContent = t('btn_start_scrape');
  }
}

function appendTerminalLog(msg) {
  const line = document.createElement('div');
  line.className = 'log-line';
  line.textContent = msg;
  elements.pipelineTerminalBody.appendChild(line);
  elements.pipelineTerminalBody.scrollTop = elements.pipelineTerminalBody.scrollHeight;
}

// ==================== RECIPE MODAL & CLIPBOARD ====================
function initModal() {
  if (elements.modalCloseBtn) {
    elements.modalCloseBtn.addEventListener('click', () => {
      closeRecipeModal();
    });
  }

  if (elements.recipeModal) {
    elements.recipeModal.addEventListener('click', (e) => {
      if (e.target === elements.recipeModal) {
        closeRecipeModal();
      }
    });
  }

  // Keyboard navigation & Focus Trap
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (elements.recipeModal && elements.recipeModal.classList.contains('active')) {
        closeRecipeModal();
      }
      if (elements.irTooltipPopup && elements.irTooltipPopup.style.display !== 'none') {
        elements.irTooltipPopup.style.display = 'none';
      }
    }

    // Modal Focus Trap
    if (e.key === 'Tab' && elements.recipeModal && elements.recipeModal.classList.contains('active')) {
      const focusables = elements.recipeModal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if (focusables.length > 0) {
        const first = focusables[0];
        const last = focusables[focusables.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    }
  });

  // Browser Back Button to close modal
  window.addEventListener('popstate', () => {
    if (elements.recipeModal && elements.recipeModal.classList.contains('active')) {
      closeRecipeModal(false);
    }
  });

  // Copy Ingredients Button with SVG Feedback
  if (elements.copyIngredientsBtn) {
    elements.copyIngredientsBtn.addEventListener('click', () => {
      const text = elements.modalIngredientsText.textContent.trim();
      safeCopyText(text, () => {
        const checkSvg = `<svg class="svg-icon svg-icon-sm" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>`;
        elements.copyIngredientsBtn.innerHTML = `${checkSvg} <span>${t('btn_copied')}</span>`;
        setTimeout(() => {
          const copySvg = `<svg class="svg-icon svg-icon-sm" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>`;
          elements.copyIngredientsBtn.innerHTML = `${copySvg} <span data-i18n="btn_copy_ing">${t('btn_copy_ing')}</span>`;
        }, 2000);
      });
    });
  }
}

function safeCopyText(text, successCallback) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(successCallback).catch(() => {
      fallbackExecCopy(text, successCallback);
    });
  } else {
    fallbackExecCopy(text, successCallback);
  }
}

function fallbackExecCopy(text, callback) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.left = "-9999px";
  textArea.style.top = "-9999px";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
    if (callback) callback();
  } catch (err) {
    console.error('Fallback copy failed:', err);
  }
  document.body.removeChild(textArea);
}

function safeGetStorage(key, defaultVal) {
  try {
    return localStorage.getItem(key) || defaultVal;
  } catch (e) {
    return defaultVal;
  }
}

function safeSetStorage(key, val) {
  try {
    localStorage.setItem(key, val);
  } catch (e) {
    // Graceful fallback for incognito / restricted storage
  }
}

function openRecipeModal(recipe) {
  state.lastFocusedElement = document.activeElement;
  elements.modalClusterBadge.textContent = recipe.cluster_name || `Cluster ${recipe.cluster_id + 1}`;
  elements.modalRecipeTitle.textContent = recipe.title;
  elements.modalRecipeScore.textContent = `Cosine Similarity: ${(recipe.score || 0).toFixed(4)}`;
  elements.modalIngredientsText.textContent = recipe.ingredients || 'Ingredients details not provided.';

  const tokens = (recipe.cleaned_ingredients || '').split(' ').filter(t => t.length > 1);
  elements.modalCleanedTokens.innerHTML = tokens.map(t => `<span class="token-pill">${escapeHtml(t)}</span>`).join('');

  elements.modalExternalLink.href = recipe.url && recipe.url !== 'No URL found' ? recipe.url : 'https://cookpad.com';
  
  elements.recipeModal.style.display = 'flex';
  requestAnimationFrame(() => {
    elements.recipeModal.classList.add('active');
    if (elements.modalCloseBtn) elements.modalCloseBtn.focus();
  });

  if (!window.location.hash.startsWith('#recipe-')) {
    history.pushState({ modalOpen: true, recipeId: recipe.id }, '', `#recipe-${recipe.id || 'view'}`);
  }
}

function closeRecipeModal(popHistory = true) {
  if (!elements.recipeModal) return;
  elements.recipeModal.classList.remove('active');
  setTimeout(() => {
    elements.recipeModal.style.display = 'none';
  }, 220);

  if (popHistory && window.location.hash.startsWith('#recipe-')) {
    history.back();
  }

  if (state.lastFocusedElement && typeof state.lastFocusedElement.focus === 'function') {
    state.lastFocusedElement.focus();
  }
}

// ==================== EDUCATIONAL IR TOOLTIPS ====================
function initTooltips() {
  document.querySelectorAll('.info-tooltip-btn, .info-tooltip-trigger').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      const tooltipKey = trigger.getAttribute('data-tooltip');
      const langTooltips = IR_TOOLTIPS[state.lang] || IR_TOOLTIPS.th;
      const data = langTooltips[tooltipKey];
      if (data) {
        elements.irTooltipTitle.textContent = data.title;
        elements.irTooltipBody.innerText = data.body;
        elements.irTooltipPopup.style.display = 'block';
      }
    });
  });

  elements.irTooltipClose.addEventListener('click', () => {
    elements.irTooltipPopup.style.display = 'none';
  });

  document.addEventListener('click', (e) => {
    if (elements.irTooltipPopup && !elements.irTooltipPopup.contains(e.target) && !e.target.closest('.info-tooltip-btn, .info-tooltip-trigger')) {
      elements.irTooltipPopup.style.display = 'none';
    }
  });
}

// ==================== HELPERS ====================
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
