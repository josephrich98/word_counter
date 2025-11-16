import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from collections import Counter
import csv
import re
import nltk
import tkinter.font as tkfont
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from .logic import (
    tokenize,
    remove_stopwords,
    lemmatize_words,
    count_frequencies,
    filter_singletons,
    format_table
)

# Ensure NLTK data is available
for pkg in ("stopwords", "wordnet", "omw-1.4", "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng"):
    try:
        nltk.data.find(f"corpora/{pkg}")
    except LookupError:
        nltk.download(pkg)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# POS → WordNet tag converter
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

# Globals
current_results = []
show_singletons = True   # toggle for filtering

def format_table(results):
    if not results:
        return ""
    
    # Determine column widths
    max_word_len = max(len(word) for word, _ in results)
    max_count_len = max(len(str(count)) for _, count in results)

    # Header
    lines = []
    header_word = "WORD"
    header_count = "COUNT"

    word_col = max(max_word_len, len(header_word))
    count_col = max(max_count_len, len(header_count))

    header = f"{header_word:<{word_col}}  {header_count:>{count_col}}"
    sep = f"{'-'*word_col}  {'-'*count_col}"

    lines.append(header)
    lines.append(sep)

    # Rows
    for word, count in results:
        lines.append(f"{word:<{word_col}}  {count:>{count_col}}")

    return "\n".join(lines)

def render_output():
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)

    filtered_results = []
    for word, count in current_results:
        if not show_singletons and count == 1:
            continue
        filtered_results.append((word, count))

    table_text = format_table(filtered_results)
    output_box.insert(tk.END, table_text)

    output_box.config(state="disabled")

def toggle_singletons():
    """Toggle hiding/showing words with count=1."""
    global show_singletons
    show_singletons = not show_singletons

    if show_singletons:
        filter_button.config(text="Hide count=1")
    else:
        filter_button.config(text="Show count=1")

    render_output()

def count_words():
    global current_results
    text = input_box.get("1.0", tk.END)

    # Tokenize
    words = re.findall(r"\b\w+\b", text.lower())

    # Remove stopwords
    filtered = [w for w in words if w not in stop_words]

    # POS tag + lemmatize
    tagged = pos_tag(filtered)
    lemmas = [
        lemmatizer.lemmatize(word, get_wordnet_pos(pos))
        for word, pos in tagged
    ]

    freq = Counter(lemmas)
    current_results = freq.most_common()

    render_output()

def save_csv():
    if not current_results:
        messagebox.showinfo("No data", "You must run Count Words first.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Save Word Frequencies as CSV"
    )

    if not filepath:
        return
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        writer.writerows(current_results)

    messagebox.showinfo("Saved", f"CSV saved to:\n{filepath}")


# ---------- GUI ----------
def main():
    global input_box, output_box, filter_button

    root = tk.Tk()
    root.title("Word Counter (Stopwords + Lemmatization + CSV + Filters)")

    # Allow window resizing
    root.resizable(True, True)

    # Layout config
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(4, weight=1)

    # Input label
    tk.Label(root, text="Paste your text:").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    # Input text box
    input_box = scrolledtext.ScrolledText(root, width=60, height=15)
    input_box.grid(row=1, column=0, sticky="nsew", padx=10)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=2, column=0, pady=10)

    tk.Button(button_frame, text="Count Words", command=count_words).pack(side="left", padx=10)
    tk.Button(button_frame, text="Save CSV", command=save_csv).pack(side="left", padx=10)

    # NEW: toggle filter button
    filter_button = tk.Button(button_frame, text="Hide count=1", command=toggle_singletons)
    filter_button.pack(side="left", padx=10)

    # Output label
    tk.Label(root, text="Word frequencies:").grid(row=3, column=0, sticky="w", padx=10)

    # Output text box
    output_box = scrolledtext.ScrolledText(root, width=60, height=15, state="disabled")
    output_box.grid(row=4, column=0, sticky="nsew", padx=10, pady=(0,10))

    # Text resizing
    app_font = tkfont.Font(family="Courier", size=14)

    input_box.configure(font=app_font)
    output_box.configure(font=app_font)

    def zoom_in(event=None):
        size = app_font['size']
        app_font.configure(size=size + 1)

    def zoom_out(event=None):
        size = app_font['size']
        if size > 4:
            app_font.configure(size=size - 1)

    # macOS bindings (Cmd)
    root.bind("<Command-plus>", zoom_in)
    root.bind("<Command-equal>", zoom_in)
    root.bind("<Command-minus>", zoom_out)

    # Windows/Linux bindings (Ctrl)
    root.bind("<Control-plus>", zoom_in)
    root.bind("<Control-equal>", zoom_in)
    root.bind("<Control-minus>", zoom_out)

    root.mainloop()




if __name__ == "__main__":
    main()