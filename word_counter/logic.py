import re
from collections import Counter
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from .nltk_setup import ensure_nltk

ensure_nltk()

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    elif treebank_tag.startswith("V"):
        return wordnet.VERB
    elif treebank_tag.startswith("N"):
        return wordnet.NOUN
    elif treebank_tag.startswith("R"):
        return wordnet.ADV
    return wordnet.NOUN


def tokenize(text: str):
    return re.findall(r"\b\w+\b", text.lower())


def remove_stopwords(words):
    return [w for w in words if w not in stop_words]


def lemmatize_words(words):
    tagged = pos_tag(words)
    return [
        lemmatizer.lemmatize(word, get_wordnet_pos(pos))
        for word, pos in tagged
    ]


def count_frequencies(words):
    return Counter(words).most_common()


def filter_singletons(freqs):
    return [(w, c) for w, c in freqs if c > 1]


def format_table(results):
    if not results:
        return ""

    max_word_len = max(len(word) for word, _ in results)
    max_count_len = max(len(str(count)) for _, count in results)

    header = f"{'WORD':<{max_word_len}}  {'COUNT':>{max_count_len}}"
    sep = f"{'-'*max_word_len}  {'-'*max_count_len}"

    lines = [header, sep]

    for word, count in results:
        lines.append(f"{word:<{max_word_len}}  {count:>{max_count_len}}")

    return "\n".join(lines)
