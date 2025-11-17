import nltk

def ensure_nltk():
    """
    Ensures necessary NLTK data packages are installed.
    Downloads missing ones automatically.
    """
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
            nltk.download(pkg, quiet=True)
