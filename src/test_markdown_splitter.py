import unittest 

from textnode import TextNode, TextType
from markdown_splitter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_delimiter(self):
        node = TextNode("This is a **bolded phrase** text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL_TEXT)
        
        self.assertEqual(new_nodes[1].text, "bolded phrase")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD_TEXT)
        
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL_TEXT)
    
    def test_code_delimiter(self):
        node = TextNode("This is a `code block` text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL_TEXT)
        
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)
        
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL_TEXT)

    def test_italic_delimiter(self):
        node = TextNode("This is a _italic phrase_ text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL_TEXT)
        
        self.assertEqual(new_nodes[1].text, "italic phrase")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC_TEXT)
        
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL_TEXT)

    def test_multiple_delimiter_pairs(self):
        node = TextNode("This has **two** bold **words**", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
    
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[1].text, "two")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[3].text, "words")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD_TEXT)

    def test_non_text_node_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
    
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Already bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD_TEXT)

    def test_missing_closing_delimiter(self):
        node = TextNode("This has **unclosed bold", TextType.NORMAL_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
    