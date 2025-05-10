import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from on_text_functions import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test__eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is test node", TextType.LINK)
        node2 = TextNode("This is text node2", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url = "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, url = "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(\"This is a text node\", TextType.TEXT, https://www.boot.dev)", repr(node)
        )



class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestSplitNodesDelim(unittest.TestCase):
    def test_code_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    def test_bold_eq(self):
        node = TextNode("This is text with **bold text** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
        ])
    def test_italic_eq(self):
        node = TextNode("This is text with _italic text_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it", TextType.TEXT),
        ])
    def test_multiple_types(self):
        node = TextNode("This is text with _italic text_ and **bold text** with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    [node], "_", TextType.ITALIC),
                "**", TextType.BOLD),
            "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ])


if __name__ == "__main__":
    unittest.main()
