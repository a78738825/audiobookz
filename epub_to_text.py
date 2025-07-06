import re
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import epub

from load_config import CHAPTER_OUTPUT_DIR


def sanitize_filename(name):
    """
    Cleans a string to make it safe for use as a filename.

    Steps:
    - Removes characters not allowed in filenames on most OSes (like < > : " / \ | ? *)
    - Trims whitespace from both ends
    - Replaces internal whitespace with underscores to make filenames shell-friendly

    Args:
        name (str): Raw string to be used as a filename

    Returns:
        str: Sanitized and filesystem-safe version of the name
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', "", name)  # remove illegal characters
    sanitized = sanitized.strip()  # trim whitespace
    sanitized = re.sub(r"\s+", "_", sanitized)  # replace whitespace with underscores
    return sanitized


def extract_chapter_text(content_item):
    """
    Extracts plain text from an EPUB content item using BeautifulSoup.

    Explanation:
    - content_item is an object representing a single file from inside the EPUB archive,
      such as a chapter's HTML content.
    - The `get_content()` method returns the raw HTML byte content of that file.
    - BeautifulSoup parses the HTML so we can extract plain text.

    Args:
        content_item (epub.EpubHtml): HTML content object from the EPUB book

    Returns:
        str: Extracted plain text from the HTML
    """
    html_content = content_item.get_content()  # Returns bytes
    soup = BeautifulSoup(html_content, "html.parser")  # Parse HTML

    lines = []

    # Collect visible text from each block-level element, one line per paragraph
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "blockquote"]):
        text = tag.get_text(strip=True)
        if text:
            lines.append(text)

    # Separate paragraphs with double newlines for readability
    return "\n\n".join(lines)


def convert_epub(epub_path, output_dir=CHAPTER_OUTPUT_DIR):
    """
    Converts an EPUB book into plain text files — one per chapter.

    Steps:
    1. Load the EPUB file using ebooklib
    2. Iterate over the table of contents (TOC)
    3. For each chapter:
        - Get the title and href (internal path to content)
        - Locate the actual HTML file by matching href
        - Extract text and save to a .txt file

    Args:
        epub_path (Path or str): Path to the .epub file to convert
        output_dir (Path or str, optional): Directory where text files will be saved.
            Defaults to value from config.json ("chapter_output_directory").
    """

    # Load the EPUB book into memory using ebooklib
    book = epub.read_epub(str(epub_path))

    # Ensure the output folder exists to save chapter text files
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Saving extracted chapters to: {output_dir}")

    # EPUB TOC (table of contents) is a list of `Link` objects or nested tuples
    for toc_entry in book.toc:
        # Handle flat and shallow-nested TOC formats (deeper nesting needs recursion)

        # Case 1: Direct link to a chapter
        if isinstance(toc_entry, epub.Link):
            title = toc_entry.title  # Displayed chapter title (e.g. "Chapter 1")
            href = toc_entry.href  # Internal path (e.g. "Text/ch1.xhtml")

        # Case 2: Nested TOC (common in structured EPUBs)
        elif isinstance(toc_entry, tuple):
            # The first element is the main TOC entry, the second is a list of sub-entries
            title = toc_entry[0].title
            href = toc_entry[0].href

        else:
            # If TOC format is unknown, skip it (defensive coding)
            continue

        # Clean the title so we can safely use it as a filename
        safe_title = sanitize_filename(title)

        # Initialize a variable to hold the content item that matches the TOC href
        content_item = None

        # Iterate through all the "items" (files) inside the EPUB archive
        for item in book.get_items():
            # `item.get_name()` gives the internal path of the file in the EPUB
            # For example: "Text/ch1.xhtml" or "OEBPS/Text/ch1.xhtml"
            if item.get_name() == href:
                content_item = item
                break  # Stop after the first match

        if not content_item:
            # If we couldn’t find the content item for this TOC entry, report and skip
            print(f"⚠️  Missing content for: {href}")
            continue

        # Extract visible text from the HTML content of this chapter
        plain_text = extract_chapter_text(content_item)

        # Build the output path for the .txt file (one per chapter)
        output_path = output_dir / f"{safe_title}.txt"

        # Write the plain text content to a UTF-8 encoded file
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(plain_text)

        print(f"✅ Wrote chapter: {output_path}")


if __name__ == "__main__":
    # Prompt the user to enter the path to the EPUB file
    epub_file_path = Path(input("Enter path to .epub file: ").strip())

    # Validate the file path: must not be empty and must exist as a file
    if not epub_file_path.is_file():
        print("❌ Invalid EPUB file path. Exiting.")
        exit(1)

    # Start the EPUB-to-text conversion process
    convert_epub(epub_file_path)
