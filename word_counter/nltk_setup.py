import os
import nltk

NLTK_DATA_DIR = os.path.expanduser("~/.local/share/nltk_data")
os.makedirs(NLTK_DATA_DIR, exist_ok=True)

# Tell NLTK to search here
nltk.data.path.append(NLTK_DATA_DIR)

def ensure_nltk():
    packages = [
        "stopwords",
        "wordnet",
        "omw-1.4",
        "averaged_perceptron_tagger",
        "averaged_perceptron_tagger_eng",
    ]

    for pkg in packages:
        try:
            nltk.data.find(f"corpora/{pkg}")
        except LookupError:
            print(f"[word_counter] Downloading NLTK package: {pkg}")
            nltk.download(pkg, download_dir=NLTK_DATA_DIR, quiet=True)
