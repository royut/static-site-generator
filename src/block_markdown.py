from enum import Enum

from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'


def markdown_to_blocks(text):
    blocks = text.split('\n\n')
    blocks = list(map(lambda block: block.strip(), blocks))
    blocks = list(filter(lambda block: block != '', blocks))
    return blocks


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith('```\n') and block.endswith('\n```'):
        return BlockType.CODE
    lines = block.split('\n')
    qoute_lines = list(filter(lambda line: line.startswith('>'), lines))
    if len(qoute_lines) == len(lines):
        return BlockType.QUOTE
    unordered_lines = list(filter(lambda line: line.startswith('- '), lines))
    if len(unordered_lines) == len(lines):
        return BlockType.UNORDERED_LIST
    ordered_flag = True
    for i in range(len(lines)):
        if not lines[i].startswith(f'{i+1}. '):
            ordered_flag = False
    if ordered_flag:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes


def heading_block_to_html_node(block):
    haeding_num = 0
    for i in range(0, 6):
        if block[i] == '#':
            haeding_num += 1
    tag = f'h{haeding_num}'
    children = text_to_children(block[haeding_num+1:])
    parent_node = ParentNode(tag, children)
    return parent_node


def code_block_to_html_node(block):
    text_node = TextNode(block[4:-3], TextType.TEXT)
    child = text_node_to_html_node(text_node)
    pre_node = ParentNode('code', [child])
    code_node = ParentNode('pre', [pre_node])
    return code_node


def quote_block_to_html_node(block):
    lines = []
    for line in block.split('\n'):
        lines.append(line[1:].strip())
    text = ' '.join(lines)
    children = text_to_children(text)
    node = ParentNode('blockquote', children)
    return node


def unordered_list_block_to_html_node(block):
    list_html_nodes = []
    for line in block.split('\n'):
        line_text = line[1:].strip()
        temp_child = text_to_children(line_text)
        li_html_node = ParentNode('li', temp_child)
        list_html_nodes.append(li_html_node)
    ul_node = ParentNode('ul', list_html_nodes)
    return ul_node


def ordered_list_block_to_html_node(block):
    list_html_nodes = []
    for line in block.split('\n'):
        line_text = line[2:].strip()
        temp_child = text_to_children(line_text)
        li_html_node = ParentNode('li', temp_child)
        list_html_nodes.append(li_html_node)
    ol_node = ParentNode('ol', list_html_nodes)
    return ol_node


def paragraph_block_to_html_node(block):
    text = block.replace('\n', ' ')
    children = text_to_children(text)
    node = ParentNode('p', children)
    return node


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            return heading_block_to_html_node(block)
        case BlockType.CODE:
            return code_block_to_html_node(block)
        case BlockType.QUOTE:
            return quote_block_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_block_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_block_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_block_to_html_node(block)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        node = block_to_html_node(block)
        nodes.append(node)
    return ParentNode('div', nodes)