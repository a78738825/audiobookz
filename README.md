# 📖 EPUB to Plain Text Converter

This Python script extracts **chapters from an EPUB file** (already unzipped) and converts them from HTML into clean, readable plain text files — one per chapter.

It relies on a valid **table-of-contents HTML file** (`table-of-contents.html`) inside the `OEBPS/` directory of the unzipped EPUB.

---

## 🚀 Features

- Parses the **table of contents** from HTML and identifies chapter files.
- Converts each chapter to plain text using `html2text`.
- **Cleans up chapter titles** to create safe filenames (Windows/Linux compatible).
- Saves all chapters in a `text_output/` folder by default.

---

## 📦 Requirements

Make sure you have the following Python module installed:

```bash
pip install html2text
````

---

## 📁 Folder Structure Expected

You should extract your EPUB file (it's just a ZIP!) and run the script against the folder that looks like this:

```
your-epub-folder/
└── OEBPS/
    ├── table-of-contents.html
    ├── page-0.html
    ├── page-1.html
    └── ... other chapter files
```

---

## 🧠 How It Works

1. It looks for a file called `table-of-contents.html` inside `OEBPS/`.
2. Converts that file into markdown-like text.
3. Parses the markdown links to get:

   * Chapter title
   * HTML file name (e.g. `page-3.html`)
4. Cleans the chapter title to make a safe filename (replacing spaces with underscores, etc).
5. Converts the corresponding HTML chapter to plain text.
6. Writes each chapter into its own `.txt` file in the `text_output/` folder.

---

## 📌 How to Run

```bash
python your_script.py
```

You'll be prompted to enter the **path to the extracted EPUB folder**, like:

```
Enter path to extracted EPUB folder: my-books/The-Hobbit/
```

Make sure `my-books/The-Hobbit/OEBPS/table-of-contents.html` exists!

---

## 📂 Output

All `.txt` files will be saved in a folder named:

```
text_output/
├── Chapter_1_A_Long_Expected_Party.txt
├── Chapter_2_Roast_Mutton.txt
└── ... and so on
```

---

## 🛠 Customizing

* Change the `output_dir="text_output"` argument in `main()` or `run_conversion()` if you want the output elsewhere.
* The `sanitize_filename()` function handles all the cleanup to make filenames safe. Modify it if needed.

---

## 🧹 Cleanup Tips

You can zip the final text files or copy them into your note-taking tool, e-reader, or backup archive.

---

## 💡 Bonus

If you're unsure how to unzip an EPUB:

```bash
unzip my-book.epub -d my-book/
```

---

## 📬 Questions?

This script was written to be **simple, readable, and robust**, but if you're lost or need enhancements, feel free to tweak it or ask for help.

Happy reading! 🌟
