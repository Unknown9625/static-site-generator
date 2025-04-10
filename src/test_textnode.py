import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode   
from textnode import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node3 = TextNode("This is a different text node", TextType.NORMAL_TEXT)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
    
    def test_url_parameter(self):
        node1 = TextNode("This is a text node", TextType.LINK, "http://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "http://example.com")
        node3 = TextNode("This is a text node", TextType.LINK, "http://another-example.com")
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)

    def test_normal_text(self):
        node = TextNode("Hello, World!", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello, World!")
    
    def test_bold_text(self):
        node = TextNode("Bold text!", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text!")
    
    def test_italic_text(self):
        node = TextNode("Italic text.", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text.")
    
    def test_code_text(self):
        node = TextNode("Code snippet.", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet.")

    def test_link_text(self):
        node = TextNode("Click me.", TextType.LINK, url="http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me.")
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "http://example.com")

    def test_image_text(self):
        node = TextNode("Alt description.", TextType.IMAGE, url="http://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIn("src", html_node.props)
        self.assertEqual(html_node.props["src"], "http://example.com/image.png")
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["alt"], "Alt description.")
    
    def test_invalid_text_type(self):
        node = TextNode("Invalid type", "INVALID_TYPE")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()