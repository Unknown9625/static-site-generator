import unittest 

from textnode import TextNode, TextType
from markdown_splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link, markdown_to_blocks

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
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is text without images", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_at_beginning(self):
        node = TextNode("![image](https://example.com/image.png) at the beginning", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" at the beginning", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL_TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("This is text without links", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_at_beginning(self):
        node = TextNode("[link](https://example.com) at the beginning", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" at the beginning", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

def test_markdown_to_blocks(self):
    markdown = """
    This is a **bolded phrase** text

    This is another paragraph with _italic_ text and `code block` text.
    This is the same paragraph on a new line

    - This is a list
    - with several items
    """
    
    blocks = markdown_to_blocks(markdown)
    self.assertEqual(
        blocks,
        [
            "This is a **bolded phrase** text",
            "This is another paragraph with _italic_ text and `code block` text.\nThis is the same paragraph on a new line",
            "- This is a list\n- with several items"
        ]
    )