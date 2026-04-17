import unittest

from block_markdown import markdown_to_blocks, BlockType, block_to_block_type


class TestFunction(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type(self):
        md = "## heading"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)
    
    def test_block_to_block_type2(self):
        md = """```
code block
```"""
        self.assertEqual(block_to_block_type(md), BlockType.CODE)
    
    def test_block_to_block_type3(self):
        md = """> quote
> quote2"""
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)
    
    def test_block_to_block_type4(self):
        md = """- unordered 1
- unordered 2"""
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type5(self):
        md = """1. order1
2. order2"""
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)
    
    def test_block_to_block_type6(self):
        md = """
        asddsa
        """
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()