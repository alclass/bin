#!/usr/bin/env python3
"""
Converts an html file to its epub equivalent

==============================
The Python same script (perhaps a little bit different) in NodeJS:
------------------------------

  1) libray install
    npm install epub-gen

  2) Node's source code
------------------------------
const Epub = require("epub-gen");
function createEpub(htmlContent, title = "My eBook", filename = "output.epub") {
    const options = {
        title: title,
        author: "Unknown", // You can customize this
        output: filename,
        content: [
            {
                title: "Chapter 1",
                data: htmlContent
            }
        ]
    };
    new Epub(options).promise
        .then(() => console.log(`EPUB created: ${filename}`))
        .catch(error => console.error("Error creating EPUB:", error));
}
// Example usage
const htmlContent = "<h1>Hello, World!</h1><p>This is a sample EPUB file generated from HTML.</p>";
createEpub(htmlContent);
------------------------------
ends NodeJS similar script
==============================

"""
from ebooklib import epub


def create_epub(html_content=None, title="My eBook", filename=None):

  if filename is None:
    filename = "/home/friend/bin/logs/output.epub"
    # filename = "output.epub"

  book = epub.EpubBook()

  # Set metadata
  book.set_title(title)
  book.set_language("en")

  # Create EPUB content
  chapter = epub.EpubHtml(title="Chapter 1", file_name="chap_1.xhtml", content=html_content)
  book.add_item(chapter)

  # Define Table of Contents properly
  book.toc = [
    (epub.Section("Contents"), [chapter])  # Properly structured TOC
  ]

  # Define Spine
  book.spine = ["nav", chapter]

  # Add default navigation files
  book.add_item(epub.EpubNcx())
  book.add_item(epub.EpubNav())

  # Save the EPUB file
  scrmsg = f"Creating epub file {filename}"
  print(scrmsg)
  epub.write_epub(filename, book, {})


def create_example():
  # Example usage
  html_content = "<h1>Hello, World!</h1><p>This is a sample EPUB file generated from HTML.</p>"
  create_epub(html_content)


def process():
  create_example()


if __name__ == '__main__':
  process()
