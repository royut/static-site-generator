import unittest

from htmlnode import HTMLNode


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