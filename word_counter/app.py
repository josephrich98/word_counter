import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import tkinter.font as tkfont
import csv

from .logic import (
    tokenize,
    remove_stopwords,
    lemmatize_words,
    count_frequencies,
    filter_singletons,
    format_table,
)
from .nltk_setup import ensure_nltk


def run_count(input_box, output_box, show_singletons_var, current_results):
    """Compute word frequencies and update result list."""
    text = input_box.get("1.0", tk.END)

    words = tokenize(text)
    words = remove_stopwords(words)
    words = lemmatize_words(words)
    results = count_frequencies(words)

    current_results.clear()
    current_results.extend(results)

    render_output(output_box, show_singletons_var.get(), current_results)


def render_output(output_box, show_singletons, current_results):
    """Render table in output box."""
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)

    if not show_singletons:
        results = filter_singletons(current_results)
    else:
        results = current_results

    output_box.insert(tk.END, format_table(results))
    output_box.config(state="disabled")


def save_csv(current_results):
    """Save current results to CSV file."""
    if not current_results:
        messagebox.showinfo("No data", "Run Count Words first.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Save Word Frequencies"
    )

    if not filepath:
        return

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        writer.writerows(current_results)

    messagebox.showinfo("Saved", f"Saved CSV → {filepath}")


def main():
    ensure_nltk()
    
    # Mutable “global” state held in an object
    current_results = []

    root = tk.Tk()
    root.title("Word Counter")

    # Resizing behavior
    root.resizable(True, True)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(4, weight=1)

    # Label
    tk.Label(root, text="Paste your text:").grid(
        row=0, column=0, sticky="w", padx=10, pady=5
    )

    # Input text widget
    input_box = scrolledtext.ScrolledText(root, width=60, height=15)
    input_box.grid(row=1, column=0, sticky="nsew", padx=10)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=2, column=0, pady=10)

    # Singleton toggle state
    show_singletons_var = tk.BooleanVar(value=True)

    # Count button
    tk.Button(
        button_frame,
        text="Count Words",
        command=lambda: run_count(input_box, output_box, show_singletons_var, current_results)
    ).pack(side="left", padx=10)

    # CSV button
    tk.Button(
        button_frame,
        text="Save CSV",
        command=lambda: save_csv(current_results)
    ).pack(side="left", padx=10)

    # Toggle button
    def toggle_singletons():
        current = show_singletons_var.get()
        show_singletons_var.set(not current)
        filter_button.config(text="Hide count=1" if not current else "Show count=1")
        render_output(output_box, show_singletons_var.get(), current_results)

    filter_button = tk.Button(
        button_frame,
        text="Hide count=1",
        command=toggle_singletons
    )
    filter_button.pack(side="left", padx=10)

    # Output label
    tk.Label(root, text="Word frequencies:").grid(
        row=3, column=0, sticky="w", padx=10
    )

    # Output widget
    output_box = scrolledtext.ScrolledText(root, width=60, height=15, state="disabled")
    output_box.grid(row=4, column=0, sticky="nsew", padx=10, pady=(0, 10))

    # Font with zoom
    app_font = tkfont.Font(family="Courier", size=14)
    input_box.configure(font=app_font)
    output_box.configure(font=app_font)

    def zoom_in(event=None):
        app_font.configure(size=app_font['size'] + 1)

    def zoom_out(event=None):
        if app_font['size'] > 4:
            app_font.configure(size=app_font['size'] - 1)

    # Bindings
    root.bind("<Command-plus>", zoom_in)
    root.bind("<Command-equal>", zoom_in)
    root.bind("<Command-minus>", zoom_out)
    root.bind("<Control-plus>", zoom_in)
    root.bind("<Control-equal>", zoom_in)
    root.bind("<Control-minus>", zoom_out)

    root.mainloop()


if __name__ == "__main__":
    main()
