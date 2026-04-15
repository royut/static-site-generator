import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for i in range(len(old_nodes)):
        old_node = old_nodes[i]
        # if the type is not text add and pass
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # text type
        node_text_split = old_node.text.split(delimiter)
        # no closing delimiter
        if len(node_text_split) % 2 == 0:
            raise Exception('invalid markdown syntax')
        for j in range(len(node_text_split)):
            if node_text_split[j] == '':
                continue
            if j % 2 == 1:
                new_text_node = TextNode(node_text_split[j], text_type)
            else:
                new_text_node = TextNode(node_text_split[j], TextType.TEXT)
            new_nodes.append(new_text_node)
    return new_nodes


def extract_markdown_images(text):
    re_match = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(re_match, text)


def extract_markdown_links(text):
    re_match = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(re_match, text)