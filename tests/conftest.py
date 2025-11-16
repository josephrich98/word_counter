import nltk
import pytest

@pytest.fixture(scope="session", autouse=True)
def ensure_nltk():
    for pkg in ("stopwords", "wordnet", "omw-1.4", "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng"):
        try:
            nltk.data.find(f"corpora/{pkg}")
        except LookupError:
            print(f"Downloading NLTK package: {pkg}")
            nltk.download(pkg)
