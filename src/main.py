# src/main.py

import os
import shutil

print("Hello, World!")

from textnode import TextNode, TextType
from generate import generate_page

def copy_static_to_public():
    print("Starting to copy static files")

    if not os.path.exists("static"):
        print("Error: static directory does not exist.")
        return
    
    print(f"Contents of static directory: {os.listdir('static')}")

    if os.path.exists("public"):
        print("Removing existing public directory.")
        shutil.rmtree("public")
    
    print("Creating public directory.")
    os.mkdir("public")
    
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

    recursive_copy("static", "public")
    print("Static files copied to public directory.")
    print(f"Contents of public directory: {os.listdir('public')}")


def main():
    # Create a TextNode instance
    text_node = TextNode("Hello, World!", TextType.BOLD_TEXT, None)
    
    copy_static_to_public()

    content_path = "content/index.md"
    template_path = "template.html"
    dest_path = "public/index.html"

    print("Starting HTML page generation")
    generate_page(content_path, template_path, dest_path)
    print("HTML page generation completed")

if __name__ == "__main__":
    main()