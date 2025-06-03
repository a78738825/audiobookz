import os
import re

from html2text import html2text


def table_of_contents(html_directory):
    """
    Parses the table-of-contents HTML file, converts it to plain text,
    and returns a list of cleaned TOC entries.

    Args:
        html_directory (str): Path to the folder containing the HTML files.

    Returns:
        list[str]: A list of non-empty lines from the converted TOC markdown.
    """

    # Construct the full path to the TOC HTML file by joining folder path + filename
    toc_path = os.path.join(html_directory, "table-of-contents.html")
    print(f"Looking for TOC at: {toc_path}")

    # Check if the TOC file exists at the expected location
    if os.path.exists(toc_path):
        # Open the TOC file in read mode with UTF-8 encoding (to handle any unicode chars)
        with open(toc_path, "r", encoding="utf-8") as toc_file:
            # Read entire contents of TOC HTML and convert it to markdown-like plain text
            toc_text = html2text(toc_file.read())

        # Split the converted markdown text into individual lines by newline
        # Filter out any empty lines to keep only meaningful TOC entries
        toc_lines = [line for line in toc_text.split("\n") if line]

        # Debug print: show the extracted TOC lines
        print("Parsed TOC entries:", toc_lines)

        # Return the list of TOC lines for further processing
        return toc_lines

    else:
        # If TOC file doesn't exist, inform the user and return an empty list
        print("TOC not found.")
        return []


def text_format(html_directory, file_name):
    """
    Reads the HTML content of a single chapter file and converts it to plain text.

    Args:
        html_directory (str): Path to the folder containing the HTML files.
        file_name (str): Name of the HTML file to read.

    Returns:
        str: The plain text content of the HTML file.
    """
    # Construct full file path of the chapter by combining directory + filename
    file_path = os.path.join(html_directory, file_name)

    # Open the chapter HTML file in read mode with UTF-8 encoding
    with open(file_path, "r", encoding="utf-8") as chapter_file:
        # Read the HTML content and convert it to plain text with html2text
        return html2text(chapter_file.read())


def sanitize_filename(name):
    """
    Cleans a string to make it safe to use as a filename on Windows (and most OSes).

    What it does:
    1. Removes characters that are illegal in filenames such as: < > : " / \ | ? *
    2. Removes any leading or trailing whitespace (spaces, tabs, etc.)
    3. Replaces all sequences of whitespace inside the name with underscores (_)

    Args:
        name (str): The original string, e.g. a chapter title.

    Returns:
        str: A sanitized, safe filename string.
    """

    # Step 1: Remove all illegal characters using a regex substitution.
    # Characters inside the square brackets [] are removed wherever found.
    # This prevents errors or issues when creating files with those characters.
    sanitized_filename = re.sub(r'[<>:"/\\|?*]', "", name)

    # Step 2: Strip whitespace from start and end of the string.
    # This avoids filenames that accidentally start or end with spaces.
    sanitized_filename = sanitized_filename.strip()

    # Step 3: Replace any sequence of one or more whitespace characters (space, tab, newline) inside the string
    # with a single underscore. This makes filenames easier to handle in scripts and shells.
    sanitized_filename = re.sub(r"\s+", "_", sanitized_filename)

    # Return the cleaned-up filename ready for safe use.
    return sanitized_filename


def main(toc_entries, html_directory, output_dir="plain_text_chapters"):
    """
    Converts each chapter listed in the table of contents into a plain text file.

    Args:
        toc_entries (list[str]): List of TOC markdown lines, each with a chapter link.
        html_directory (str): Directory where the chapter HTML files reside.
        output_dir (str, optional): Directory where output text files will be saved.
                                    Defaults to "plain_text_chapters".
    """
    # Create the output directory if it does not exist.
    # exist_ok=True means it won't raise an error if the folder already exists.
    os.makedirs(output_dir, exist_ok=True)

    # Process each line in the TOC entries list
    for entry in toc_entries:
        print(f">>> TOC item: {entry}")

        # Use regex to extract the chapter title and filename from the markdown TOC line.
        # Pattern explanation:
        #   \s*      => match any whitespace at the start (spaces, tabs)
        #   \*       => match a literal asterisk '*', which marks list items in markdown
        #   \s*      => optional whitespace after asterisk
        #   \[(.*?)\] => match anything inside square brackets (chapter title), non-greedy
        #   \( (.*?) \) => match anything inside parentheses (filename), non-greedy
        match = re.match(r"\s*\*\s*\[(.*?)\]\((.*?)\)", entry)

        if match:
            # Unpack the matched groups: chapter title and file name
            chapter_name, file_name = match.groups()

            # Sanitize the chapter title so it can be safely used as a filename
            chapter_name = sanitize_filename(chapter_name)

            # Construct the full path to the chapter HTML file
            file_path = os.path.join(html_directory, file_name)

            # Check if the file actually exists before trying to read it
            if not os.path.exists(file_path):
                print(f"Missing file: {file_path}")
                # Skip this entry and continue with the next
                continue

            # Read the HTML content of the chapter and convert to plain text
            chapter_text = text_format(html_directory, file_name)

            # Construct the output path, saving as a .txt file named after the sanitized chapter title
            output_path = os.path.join(output_dir, f"{chapter_name}.txt")

            # Write the converted plain text to the output file with UTF-8 encoding
            with open(output_path, "w", encoding="utf-8") as out_file:
                out_file.write(chapter_text)

            print(f"Wrote chapter to {output_path}")

        else:
            # If a line doesn't match the expected TOC format, print a debug message and skip it
            print("Skipped non-chapter TOC line:", entry)


def run_conversion(html_directory, output_dir="plain_text_chapters"):
    """
    Wrapper function that runs the entire conversion process:
    1. Parses the TOC
    2. Converts chapters to text files

    Args:
        html_directory (str): Path to the folder with extracted EPUB HTML files.
        output_dir (str, optional): Folder where output text files will be saved.
    """
    # Parse the table of contents from the HTML directory
    toc = table_of_contents(html_directory)

    if toc:
        # If TOC is found and not empty, run the main conversion function
        main(toc, html_directory, output_dir)
    else:
        # If no TOC found, notify the user
        print("No table of contents found.")


if __name__ == "__main__":
    # Ask the user to input the path to the extracted EPUB folder
    book_directory = input("Enter path to extracted EPUB folder: ").strip()

    # If the user inputs nothing (empty string), exit the program
    if not book_directory:
        print("No path provided. Exiting.")
        exit(1)

    # Construct the expected HTML folder path inside the extracted EPUB folder
    html_directory = os.path.join(book_directory, "OEBPS")

    # Check if this directory actually exists before continuing
    if not os.path.exists(html_directory):
        print(f"Directory does not exist: {html_directory}")
        exit(1)

    # Run the full conversion process using the validated HTML directory path
    run_conversion(html_directory)
