import pathlib
import re

import fitz  # PyMuPDF
import pymupdf4llm

path = "C:/Users/Sensei/Downloads/Documents/nflx-20241231.pdf"


def PDFToMarkdown(output_md_path=None):
    doc = fitz.open(path)
    markdown_content = []

    # Configuration for header detection
    # header_font_sizes = set()
    font_info = {}  # {font_size: count}
    header_sizes = []

    # First pass: collect font statistics to identify headers
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for line in b["lines"]:
                    for span in line["spans"]:
                        size = round(span["size"], 1)
                        font_info[size] = font_info.get(size, 0) + 1

    # Determine likely header font sizes (top 2 largest sizes with sufficient occurrences)
    if font_info:
        sorted_sizes = sorted(font_info.keys(), reverse=True)
        header_sizes = [size for size in sorted_sizes if font_info[size] > 2][:2]

    # Second pass: convert content to markdown
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]

        for b in blocks:
            if "lines" in b:
                block_text = ""
                is_header = False
                font_size = None

                for line in b["lines"]:
                    line_text = ""
                    for span in line["spans"]:
                        # Detect header based on font size
                        current_size = round(span["size"], 1)
                        if font_info and current_size in header_sizes:
                            is_header = True
                            font_size = current_size

                        # Clean the text
                        text = span["text"]
                        # Escape special Markdown characters
                        text = re.sub(r"([_*\[\]()~`>#+\-|{}.!])", r"\\\1", text)
                        line_text += text

                    block_text += line_text + " "

                block_text = block_text.strip()

                if not block_text:
                    continue

                # Determine Markdown formatting
                if is_header:
                    # Calculate header level based on relative font size
                    if len(header_sizes) > 1:
                        header_level = 1 if font_size == max(header_sizes) else 2
                    else:
                        header_level = 1
                    markdown_content.append(f"{'#' * header_level} {block_text}\n")
                else:
                    # Handle lists (simple detection)
                    if block_text.startswith(("•", "-", "*", "◦")):
                        markdown_content.append(f"* {block_text[1:].strip()}\n")
                    else:
                        # Regular paragraph
                        markdown_content.append(f"{block_text}\n\n")

        # Add page break if not last page
        if page_num < len(doc) - 1:
            markdown_content.append("\n---\n\n")

    # Combine all content
    markdown_text = "".join(markdown_content)

    # Post-processing cleanup
    markdown_text = re.sub(
        r"\n{3,}", "\n\n", markdown_text
    )  # Remove excessive newlines
    markdown_text = markdown_text.strip()

    # Output to file or return text
    if output_md_path:
        with open(output_md_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_text)
        print(f"Successfully converted PDF to Markdown: {output_md_path}")
    else:
        return markdown_text


# Example usage


# Or get the Markdown as a string
# markdown_text = pdf_to_markdown(input_pdf)
# print(markdown_text[:500])  # Print first 500 characters    # markdown_text = pdf_to_markdown(input_pdf)
# print(markdown_text[:500])  # Print first 500 characters
# print(markdown_text[:500])  # Print first 500 characters


def Con():
    md_text = pymupdf4llm.to_markdown(path)
    pathlib.Path("output.md").write_bytes(md_text.encode())
    pathlib.Path("output.md").write_bytes(md_text.encode())
