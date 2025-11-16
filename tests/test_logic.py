from word_counter.logic import (
    tokenize,
    remove_stopwords,
    lemmatize_words,
    count_frequencies,
    filter_singletons,
    format_table
)

def test_tokenize():
    assert tokenize("Hello, world! Test.") == ["hello", "world", "test"]


def test_remove_stopwords():
    words = ["this", "is", "test"]
    out = remove_stopwords(words)
    assert out == ["test"]


def test_lemmatize_words():
    words = ["running", "dogs", "went"]
    lemmas = lemmatize_words(words)
    # running -> run, dogs -> dog, went -> go
    assert "run" in lemmas
    assert "dog" in lemmas
    assert "go" in lemmas


def test_count_frequencies():
    words = ["a", "b", "a", "c", "a"]
    counts = count_frequencies(words)
    assert counts[0] == ("a", 3)


def test_filter_singletons():
    freqs = [("dog", 4), ("cat", 1), ("bird", 2)]
    out = filter_singletons(freqs)
    assert out == [("dog", 4), ("bird", 2)]


def test_format_table():
    data = [("apple", 3), ("banana", 1)]
    table = format_table(data)
    assert "apple" in table
    assert "banana" in table
    assert "COUNT" in table
