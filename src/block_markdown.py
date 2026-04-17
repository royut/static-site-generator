from enum import Enum


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
    if block.startswith('# ') or block.startswith('## ') or block.startswith('### ') or block.startswith('#### ') or block.startswith('##### ') or block.startswith('###### '):
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