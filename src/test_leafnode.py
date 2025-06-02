import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "This is a span.")
        self.assertEqual(node.to_html(), "<span>This is a span.</span>")

    def test_leaf_to_html_text(self):
        node = LeafNode(value="Just some text.")
        self.assertEqual(node.to_html(), "Just some text.")