# src/main.py

print("Hello, World!")

from textnode import TextNode, TextType

def main():
    # Create a TextNode instance
    text_node = TextNode("Hello, World!", TextType.BOLD_TEXT, None)
    
    # Print the TextNode instance
    print(text_node)

if __name__ == "__main__":
    main()