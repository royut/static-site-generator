import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class testParentNode(unittest.TestCase):
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
    
    def test_to_html_with_many_children(self):
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
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        )
    
    def test_to_html_without_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode('p', None)
            node.to_html()
    
    def test_to_html_without_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("b", "Bold text")])
            node.to_html()


if __name__ == "__main__":
    unittest.main()