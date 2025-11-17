import os
import nltk

NLTK_DATA_DIR = os.path.expanduser("~/.local/share/nltk_data")
os.makedirs(NLTK_DATA_DIR, exist_ok=True)

# Ensure NLTK searches here *first*
if NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.insert(0, NLTK_DATA_DIR)

def nltk_resource_exists(pkg: str) -> bool:
    """
    Returns True if the NLTK resource exists in ANY nltk.data.path location.
    Checks both corpora and taggers namespaces.
    """
    # 1. Direct filesystem check in all nltk.data.path directories
    for base in nltk.data.path:
        # We look for a directory named exactly pkg anywhere inside base
        candidate = os.path.join(base, pkg)
        if os.path.exists(candidate):
            return True

    # 2. Check NLTK's own resource lookup under both corpora and taggers
    for namespace in ("corpora", "taggers"):
        try:
            nltk.data.find(f"{namespace}/{pkg}")
            return True
        except LookupError:
            pass

    return False


def ensure_nltk():
    packages = [
        "stopwords",
        "wordnet",
        "omw-1.4",
        "averaged_perceptron_tagger",
        "averaged_perceptron_tagger_eng",
    ]

    for pkg in packages:
        if not nltk_resource_exists(pkg):
            print(f"[word_counter] Downloading NLTK package: {pkg}")
            nltk.download(pkg, download_dir=NLTK_DATA_DIR, quiet=True)