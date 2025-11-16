# Word counter

A simple command-line tool to count the frequency of words in a file.

Features:
- case-insensitive
- removes stop words (NLTK)
- stems words (singular vs plural, tense, etc)
- button for filtering counts=1
- resizable window with text size adjustments
- button for saving to csv

## Installation

```bash
pip install word_counter
```

## Usage

### GUI
```bash
word_counter
```

### Provide text input directly from command line, with streaming to stdout
```bash
word_counter "This is a sample text. This text is for testing."
```

### Provide text input directly from command line, with output to a file
```bash
word_counter -o output.csv "This is a sample text. This text is for testing."
```

### Provide a text file as input
```bash
word_counter -i input.txt
```

### Print help
```bash
word_counter -h
```