import unittest
from markdown_parser import extract_markdown_images, extract_markdown_links, text_to_textnodes, extract_title
from textnode import TextNode, TextType

class TestMarkdownParser(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

if __name__ == "__main__":
    unittest.main()

class TestTextToTextNodes(unittest.TestCase):
    def test_simple_text(self):
        text = "Hello, world!"
        expected = [TextNode("Hello, world!", TextType.NORMAL_TEXT)]
        actual = text_to_textnodes(text)
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0].text, actual[0].text)
        self.assertEqual(expected[0].text_type, actual[0].text_type)

    def test_bold_text(self):
        text = "Hello, **world**!"
        expected = [
            TextNode("Hello, ", TextType.NORMAL_TEXT),
            TextNode("world", TextType.BOLD_TEXT),
            TextNode("!", TextType.NORMAL_TEXT)
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEqual(expected[i].text, actual[i].text)
            self.assertEqual(expected[i].text_type, actual[i].text_type)
    
    def test_italic_text(self):
        text = "Hello, _world_!"
        expected = [
            TextNode("Hello, ", TextType.NORMAL_TEXT),
            TextNode("world", TextType.ITALIC_TEXT),
            TextNode("!", TextType.NORMAL_TEXT)
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEqual(expected[i].text, actual[i].text)
            self.assertEqual(expected[i].text_type, actual[i].text_type)

    def test_code_text(self):
        text = "Hello, `world`!"
        expected = [
            TextNode("Hello, ", TextType.NORMAL_TEXT),
            TextNode("world", TextType.CODE_TEXT),
            TextNode("!", TextType.NORMAL_TEXT)
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEqual(expected[i].text, actual[i].text)
            self.assertEqual(expected[i].text_type, actual[i].text_type)
 
    def test_image(self):
        text = "Hello, ![alt text](image.jpg)!"
        expected = [
            TextNode("Hello, ", TextType.NORMAL_TEXT),
            TextNode("alt text", TextType.IMAGE, "image.jpg"),
            TextNode("!", TextType.NORMAL_TEXT)
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEqual(expected[i].text, actual[i].text)
            self.assertEqual(expected[i].text_type, actual[i].text_type)
            if expected[i].text_type == TextType.IMAGE:
                self.assertEqual(expected[i].url, actual[i].url)

    def test_link(self):
        text = "Hello, [link text](https://example.com)!"
        expected = [
            TextNode("Hello, ", TextType.NORMAL_TEXT),
            TextNode("link text", TextType.LINK, "https://example.com"),
            TextNode("!", TextType.NORMAL_TEXT)
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEqual(expected[i].text, actual[i].text)
            self.assertEqual(expected[i].text_type, actual[i].text_type)
            if expected[i].text_type == TextType.LINK:
                self.assertEqual(expected[i].url, actual[i].url)

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title\n\nThis is some text."
        expected = "Title"
        actual = extract_title(markdown)
        self.assertEqual(expected, actual)

    def test_no_title(self):
        markdown = "This is some text."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown")

    def test_valid_title(self):
        markdown = "# My Title\nSome content here."
        expected = "My Title"
        self.assertEqual(extract_title(markdown), expected)
    
    def test_title_with_extra_spaces(self):
        markdown = "#      My Title With Spaces     \nContent here."
        expected = "My Title With Spaces"
        self.assertEqual(extract_title(markdown), expected)