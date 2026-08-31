import re
from pathlib import Path
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    lemmatizer = WordNetLemmatizer()
    base_stopwords = set(stopwords.words('english'))
except Exception:
    # Offline / No-internet / Corpora missing fallback
    lemmatizer = None
    base_stopwords = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
        'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
        'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
        'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
        'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
        'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
        'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
        'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
        'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', "now"
    }

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "Japan_Food_Ingredients_Full.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "Japan_Food_Ingredients_Cleaned.csv"

CUSTOM_CULINARY_STOPWORDS = {
    'cup', 'cups', 'teaspoon', 'teaspoons', 'tsp', 'tablespoon', 'tablespoons', 'tbsp', 'tbs', 'tb',
    'ounce', 'ounces', 'oz', 'gram', 'grams', 'g', 'gr', 'ml', 'liter', 'liters', 'kg', 'lb', 'pound', 'pounds',
    'pinch', 'dash', 'piece', 'pieces', 'pcs', 'slice', 'slices', 'clove', 'cloves',
    'package', 'packages', 'packet', 'packets', 'pack', 'packs', 'bag', 'bags', 'box', 'boxes',
    'chunk', 'chunks', 'drop', 'drops', 'handful',
    'serving', 'servings', 'people', 'yield', 'yields',
    'minute', 'minutes', 'min', 'mins', 'hour', 'hours', 'hr', 'hrs',
    'chopped', 'minced', 'sliced', 'diced', 'peeled', 'grated', 'shredded', 'crushed', 'mashed',
    'cut', 'ground', 'fresh', 'dried', 'frozen', 'cooked', 'fried', 'steamed', 'roasted', 'baked',
    'pickled', 'marinated', 'finely', 'thinly', 'lightly', 'beaten', 'melted', 'softened',
    'room', 'temp', 'temperature', 'cold', 'hot', 'warm', 'boiling',
    'large', 'small', 'medium', 'whole', 'half', 'quarter', 'thick', 'thin',
    'optional', 'divided', 'substitute', 'taste', 'needed', 'used', 'required',
    'purpose', 'all', 'instant', 'quality', 'extra', 'plus', 'pure', 'raw',
    'ingredient', 'ingredients', 'recipe', 'recipes', 'direction', 'directions',
    'instruction', 'instructions', 'method', 'step', 'steps',
    'garnish', 'topping', 'toppings', 'base', 'cooking', 'baking', 'food'
}

ALL_STOPWORDS = base_stopwords.union(CUSTOM_CULINARY_STOPWORDS)


def safe_tokenize(text: str):
    """Tokenizes text with NLTK or regex fallback"""
    try:
        return word_tokenize(text)
    except Exception:
        return re.findall(r'\b[a-z]{2,}\b', text.lower())


def safe_lemmatize(token: str) -> str:
    """Lemmatizes token with WordNet or pass-through fallback"""
    if lemmatizer is not None:
        try:
            return lemmatizer.lemmatize(token)
        except Exception:
            return token
    return token


def clean_title(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    tokens = safe_tokenize(text)
    cleaned = [safe_lemmatize(t) for t in tokens if t not in base_stopwords and len(t) > 1]
    return ' '.join(cleaned)


def clean_ingredients(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    tokens = safe_tokenize(text)
    cleaned = [safe_lemmatize(t) for t in tokens if t not in ALL_STOPWORDS and len(t) > 1]
    return ' '.join(cleaned)


def clean_recipe_dataset(input_file: Path = DEFAULT_INPUT, output_file: Path = DEFAULT_OUTPUT, progress_callback=None) -> int:
    input_path = Path(input_file)
    output_path = Path(output_file)

    # Self-healing fallback if input file is missing
    if not input_path.exists() or input_path.stat().st_size == 0:
        if progress_callback:
            progress_callback("Raw file missing or empty. Invoking self-healing dataset creator...")
        try:
            from ..default_data import ensure_data_files
            ensure_data_files()
        except Exception:
            from src.default_data import ensure_data_files
            ensure_data_files()
        input_path = DEFAULT_INPUT

    if not input_path.exists():
        input_path = PROJECT_ROOT / "Japan_Food_Ingredients_Full.csv"

    if not input_path.exists():
        # Fallback to authentic 100 catalog
        from src.default_data import ensure_data_files
        ensure_data_files()
        input_path = DEFAULT_INPUT

    if progress_callback:
        progress_callback(f"Reading raw dataset from: {input_path.name}")

    try:
        df = pd.read_csv(input_path, encoding='utf-8-sig')
    except Exception:
        df = pd.read_csv(input_path, encoding='latin1')

    if len(df) == 0:
        from src.default_data import ensure_data_files
        ensure_data_files()
        df = pd.read_csv(input_path, encoding='utf-8-sig')

    df['Cleaned Title'] = df['Recipe Title'].apply(clean_title)
    df['Cleaned Ingredients'] = df['Ingredients'].apply(clean_ingredients)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    if progress_callback:
        progress_callback(f"Data cleaning completed. Processed {len(df)} rows saved to: {output_path.name}")

    return len(df)


if __name__ == '__main__':
    clean_recipe_dataset()
