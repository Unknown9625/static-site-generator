import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_with_tag_and_props(self):
        leaf = LeafNode("a", "Click here", {"href": "https://example.com"})
        self.assertEqual(leaf.to_html(), '<a href="https://example.com">Click here</a>')

    def test_leaf_with_tag_no_props(self):
        leaf = LeafNode("p", "This is a paragraph")
        self.assertEqual(leaf.to_html(), '<p>This is a paragraph</p>')
    
    def test_leaf_with_no_tag(self):
        leaf = LeafNode(None, "Just text")
        self.assertEqual(leaf.to_html(), 'Just text')

    def test_leaf_with_no_valie_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)
    
    def test_leaf_with_empty_props(self):
        leaf = LeafNode("span", "No props here", {})
        self.assertEqual(leaf.to_html(), '<span>No props here</span>')

if __name__ == "__main__":
    unittest.main()