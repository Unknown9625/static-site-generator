import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()