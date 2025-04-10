import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_constructor_requires_tag_and_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=[])
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=None)

    def test_to_html_with_leaf_children(self):
        node = ParentNode(
            "div",
            [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]
        )
        self.assertEqual(node.to_html(), "<div><b>Bold text</b>Normal text</div>")

    def test_to_html_with_nested_parentnodes(self):
        child = ParentNode("span", [LeafNode("b", "Bold text")])
        node = ParentNode("div", [child])
        self.assertEqual(node.to_html(), "<div><span><b>Bold text</b></span></div>")
    