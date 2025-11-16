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
    format_table
)

# Globals for storing results
current_results = []
show_singletons = True


def render_output(output_box):
    """Render formatted table into output box."""
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)

    results = current_results
    if not show_singletons:
        results = filter_singletons(results)

    output_box.insert(tk.END, format_table(results))
    output_box.config(state="disabled")


def toggle_singletons(filter_button, output_box):
    """Toggle hiding/showing words with count=1."""
    global show_singletons
    show_singletons = not show_singletons

    filter_button.config(
        text="Hide count=1" if show_singletons else "Show count=1"
    )
    render_output(output_box)


def run_count(input_box, output_box):
    """Process text using logic helpers."""
    global current_results

    text = input_box.get("1.0", tk.END)

    words = tokenize(text)
    words = remove_stopwords(words)
    words = lemmatize_words(words)
    current_results = count_frequencies(words)

    render_output(output_box)


def save_csv():
    """Save current full (unfiltered) results as CSV."""
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
        import csv
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        writer.writerows(current_results)

    messagebox.showinfo("Saved", f"CSV saved to:\n{filepath}")


# -------------------------------------------------------------
#  GUI ENTRY POINT
# -------------------------------------------------------------
def main():
    global current_results

    root = tk.Tk()
    root.title("Word Counter (Stopwords + Lemmatization + CSV + Filters)")

    # Resizable window
    root.resizable(True, True)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(4, weight=1)

    # Input label
    tk.Label(root, text="Paste your text:").grid(
        row=0, column=0, sticky="w", padx=10, pady=5
    )

    # Input box
    input_box = scrolledtext.ScrolledText(root, width=60, height=15)
    input_box.grid(row=1, column=0, sticky="nsew", padx=10)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=2, column=0, pady=10)

    tk.Button(
        button_frame,
        text="Count Words",
        command=lambda: run_count(input_box, output_box)
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Save CSV",
        command=save_csv
    ).pack(side="left", padx=10)

    # Toggle singleton filter
    filter_button = tk.Button(
        button_frame,
        text="Hide count=1",
        command=lambda: toggle_singletons(filter_button, output_box)
    )
    filter_button.pack(side="left", padx=10)

    # Output label
    tk.Label(root, text="Word frequencies:").grid(
        row=3, column=0, sticky="w", padx=10
    )

    # Output box
    output_box = scrolledtext.ScrolledText(root, width=60, height=15, state="disabled")
    output_box.grid(row=4, column=0, sticky="nsew", padx=10, pady=(0, 10))

    # Font for zooming
    app_font = tkfont.Font(family="Courier", size=14)
    input_box.configure(font=app_font)
    output_box.configure(font=app_font)

    # Zoom handlers
    def zoom_in(event=None):
        app_font.configure(size=app_font['size'] + 1)

    def zoom_out(event=None):
        if app_font['size'] > 4:
            app_font.configure(size=app_font['size'] - 1)

    # macOS bindings
    root.bind("<Command-plus>", zoom_in)
    root.bind("<Command-equal>", zoom_in)
    root.bind("<Command-minus>", zoom_out)

    # Windows/Linux bindings
    root.bind("<Control-plus>", zoom_in)
    root.bind("<Control-equal>", zoom_in)
    root.bind("<Control-minus>", zoom_out)

    root.mainloop()


if __name__ == "__main__":
    main()
