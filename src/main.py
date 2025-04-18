# src/main.py

import os
import shutil
import sys

print("Hello, World!")

from textnode import TextNode, TextType
from generate import generate_page_recursive

def copy_static_to_docs():
    print("Starting to copy static files")

    if not os.path.exists("static"):
        print("Error: static directory does not exist.")
        return
    
    print(f"Contents of static directory: {os.listdir('static')}")

    if os.path.exists("docs"):
        print("Removing existing docs directory.")
        shutil.rmtree("docs")
    
    print("Creating docs directory.")
    os.mkdir("docs")
    
    def recursive_copy(src, dst):
        print(f"Copying from {src} to {dst}")
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)

            if os.path.isfile(s):
                print(f"Copying file: {s} to {d}")
                shutil.copy(s, d)
            elif os.path.isdir(s):
                print(f"Creating directory: {d}")
                os.mkdir(d)
                recursive_copy(s, d)

    recursive_copy("static", "docs")
    print("Static files copied to docs directory.")
    print(f"Contents of docs directory: {os.listdir('docs')}")


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
    print(f"Using basepath: {basepath}")

    text_node = TextNode("Hello, World!", TextType.BOLD_TEXT, None)
    
    copy_static_to_docs()

    dir_path_content = "content"
    template_path = "template.html"
    dest_dir_path = "docs"

    print("Starting HTML generation for all pages")
    generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath)
    print("HTML generation for all pages completed")

if __name__ == "__main__":
    main()