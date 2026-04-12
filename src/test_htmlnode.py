import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode('a', 'link', [], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html2(self):
        node = HTMLNode('a', 'link')
        self.assertEqual(node.props_to_html(), '')
    
    def test_props_to_html3(self):
        node = HTMLNode('a', 'link', [], {})
        self.assertEqual(node.props_to_html(), '')
    
    def test_repr(self):
        node = HTMLNode('a', 'link')
        self.assertEqual(repr(node), 'HTMLNode(a, link, None, None)')


class testLeafNode(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            node = LeafNode('a', 'link', [], {})
    
    def test_init2(self):
        with self.assertRaises(TypeError):
            node = LeafNode('a')
    
    def test_init3(self):
        with self.assertRaises(TypeError):
            node = LeafNode()

    def test_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_to_html2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_to_html3(self):
        with self.assertRaises(ValueError):
            node = LeafNode('a', None)
            node.to_html()
    
    def test_to_html4(self):
        node = LeafNode(None, 'raw text')
        self.assertEqual(node.to_html(), 'raw text')


if __name__ == "__main__":
    unittest.main()