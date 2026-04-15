import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


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
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    
    def test_extract_markdown_images3(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif")], matches)
    
    def test_extract_markdown_images4(self):
        matches = extract_markdown_images(
            "This is text without a valid image !notanimage()"
        )
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    def test_extract_markdown_links2(self):
        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_links3(self):
        matches = extract_markdown_links(
            "This is text without a valid link [not a link]"
        )
        self.assertListEqual([], matches)
    
    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_image_links(self):
        node = TextNode(
            "This is text with ![image](https://i.imgur.com/zjjcJKZ.png) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()