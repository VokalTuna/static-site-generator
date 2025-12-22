import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_has_child(self):
        node = HTMLNode("p","hello folks!")
        node2 = HTMLNode("body",children=[node])
        self.assertEqual(node2.children[0], node)

    def test_if_no_children(self):
        node = HTMLNode("p","hello folks!")
        self.assertEqual(node.children, None)
    def test_repr_includes_fields(self):
        child = HTMLNode(tag="span", value="inside")
        node = HTMLNode(
            tag="p",
            value="outer",
            children=[child],
            props={"class": "para"},
        )
        rep = repr(node)
        self.assertIn("tag: ", rep)
        self.assertIn("value: ", rep)
        self.assertIn("children: ", rep)
        self.assertIn("props: ", rep)

    def test_props_to_html_multiple(self):
        node = HTMLNode(
            tag="a",
            value="Boot.dev",
            props={"href": "https://www.boot.dev", "target": "_blank"},
        )
        result = node.props_to_html()
        # order might differ
        valid_options = {
            ' href="https://www.boot.dev" target="_blank"',
            ' target="_blank" href="https://www.boot.dev"',
        }
        self.assertIn(result, valid_options)

    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="hi", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_tag_returns_raw_text(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

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

    def test_no_children(self):
        with self.assertRaises(ValueError):
            test = ParentNode("div", None).to_html()

    def test_no_tags(self):
        with self.assertRaises(ValueError):
            node = LeafNode("b","child")
            test = ParentNode(None, [node]).to_html()

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )



if __name__ == "__main__":
    unittest.main()
