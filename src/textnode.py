from enum import Enum

from leafnode import LeafNode

class TextType(Enum):
    """
    Enum to represent different types of text nodes.
    """
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        return (f"TextNode(text={self.text}, text_type={self.text_type.value}, "
            f"url={self.url if self.url else 'None'})")

def text_node_to_html_node(text_node):
    if TextType.NORMAL_TEXT == text_node.text_type:
        return LeafNode(tag=None, value=text_node.text)
    if TextType.BOLD_TEXT == text_node.text_type:
        return LeafNode(tag="b", value=text_node.text)
    if TextType.ITALIC_TEXT == text_node.text_type:
        return LeafNode(tag="i", value=text_node.text)
    if TextType.CODE_TEXT == text_node.text_type:   
        return LeafNode(tag="code", value=text_node.text)
    if TextType.LINK == text_node.text_type:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if TextType.IMAGE == text_node.text_type:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Unknown text type: {text_node.text_type}")