import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_tag(self):
        node = HTMLNode("p", "test text")
        node2 = HTMLNode("p", "test text")
        self.assertEqual(node.tag, node2.tag)

    def test_eq_text(self):
        node = HTMLNode("p", "test text")
        node2 = HTMLNode("p", "test text")
        self.assertEqual(node.value, node2.value)

    def test_props_to_html(self):
        test_prop = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("p", "test text", None, test_prop)
        node2 = HTMLNode("h1", "test text", None, test_prop)
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_not_eq_tag(self):
        node = HTMLNode("h1", "test text")
        node2 = HTMLNode("p", "test text")
        self.assertNotEqual(node.tag, node2.tag)

    def test_not_eq_value(self):
        node = HTMLNode("h1", "test text")
        node2 = HTMLNode("p", "test text2")
        self.assertNotEqual(node.value, node2.value)

    def test_repr(self):
            node = HTMLNode(
                "p",
                "What a strange world",
                None,
                {"class": "primary"},
            )
            self.assertEqual(
                node.__repr__(),
                "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
            )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        # Tag with properties
        node = LeafNode("a", "Click me!",
            {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),
            '<a href="https://www.google.com">Click me!</a>')
    def test_leaf_to_html_no_tag(self):
            # No tag (just raw text)
            node = LeafNode(None, "Just some text")
            self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_no_value(self):
        # Should raise ValueError when value is None
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_leaf_constructor_no_value(self):
        # Should raise ValueError when created with None value
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_to_html_empty_value(self):
        # Empty string is valid
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_to_html_multiple_props(self):
        # Multiple properties
        node = LeafNode("input", "", {"type": "text", "name": "username", "required": "required"})
        # The order of attributes might vary, so we check for each attribute individually
        html = node.to_html()
        self.assertIn('<input', html)
        self.assertIn('type="text"', html)
        self.assertEqual(node.to_html(), '<input type="text" name="username" required="required"></input>')

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
    def test_parent_node_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_parent_node_none_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
        )


if __name__ == "__main__":
    unittest.main()
