import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestFunction(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_split_nodes_delimiter2(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is code block", TextType.CODE)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is code block", TextType.CODE),
        ])
    
    def test_split_nodes_delimiter3(self):
        node = TextNode("This is text with a `code block`, **bold word** and _italic word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic word", TextType.ITALIC),
        ])    

    def test_split_nodes_delimiter4(self):
        with self.assertRaises(Exception):
            node = TextNode("This is text with a `code block`, **bold word** and _italic word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
            new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
            new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
            self.assertEqual(new_nodes, [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(", ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic word", TextType.ITALIC),
            ])
    
    def test_split_nodes_delimiter5(self):
        node = TextNode("`code block` and word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code block", TextType.CODE),
            TextNode(" and word", TextType.TEXT),
        ])
    
    def test_split_nodes_delimiter6(self):
        node = TextNode("word and `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("word and ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ])


if __name__ == "__main__":
    unittest.main()