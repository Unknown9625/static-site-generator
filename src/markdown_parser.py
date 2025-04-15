import re
from textnode import TextNode, TextType


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    text_match = re.findall(pattern, text)
    return text_match

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    text_match = re.findall(pattern, text)
    return text_match

def text_to_textnodes(text):
    from markdown_splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link
    
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    return nodes