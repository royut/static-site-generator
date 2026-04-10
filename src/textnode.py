from enum import Enum


class TextType(Enum):
    PLAIN_TEXTTYPE = 'plain'
    BOLD_TEXTTYPE = 'bold'
    ITALIC_TEXTTYPE = 'italic'
    CODE_TEXTTYPE = 'code'
    LINK_TEXTTYPE = 'link'
    IMAGE_TEXTTYPE = 'image'


class TextNode:
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url
    
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'