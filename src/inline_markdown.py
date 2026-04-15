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


def split_nodes_image(old_nodes):
    new_nodes = []
    for i in range(len(old_nodes)):
        old_node = old_nodes[i]
        # if the type is not text add and pass
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # text type
        image_matches = extract_markdown_images(old_node.text)
        # if no image was found
        if len(image_matches) == 0:
            new_nodes.append(old_node)
            continue
        # spit text and images
        node_text_split = [old_node.text]
        for j in range(len(image_matches)):
            temp_split = node_text_split[-1].split(f'![{image_matches[j][0]}]({image_matches[j][1]})')
            node_text_split.pop()
            node_text_split.extend(temp_split)
        # iterate over splitted nodes and images and append to new node
        image_index = 0
        text_index = 0
        for j in range(len(node_text_split) + len(image_matches)):
            if j % 2 == 1:
                new_text_node = TextNode(image_matches[image_index][0], TextType.IMAGE, image_matches[image_index][1])
                image_index += 1
            else:
                if node_text_split[text_index] == '':
                    text_index += 1
                    continue
                new_text_node = TextNode(node_text_split[text_index], TextType.TEXT)
                text_index += 1
            new_nodes.append(new_text_node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for i in range(len(old_nodes)):
        old_node = old_nodes[i]
        # if the type is not text add and pass
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # text type
        link_matches = extract_markdown_links(old_node.text)
        # if no link was found
        if len(link_matches) == 0:
            new_nodes.append(old_node)
            continue
        # spit text and links
        node_text_split = [old_node.text]
        for j in range(len(link_matches)):
            temp_split = node_text_split[-1].split(f'[{link_matches[j][0]}]({link_matches[j][1]})')
            node_text_split.pop()
            node_text_split.extend(temp_split)
        # iterate over splitted nodes and links and append to new node
        link_index = 0
        text_index = 0
        for j in range(len(node_text_split) + len(link_matches)):
            if j % 2 == 1:
                new_text_node = TextNode(link_matches[link_index][0], TextType.LINK, link_matches[link_index][1])
                link_index += 1
            else:
                if node_text_split[text_index] == '':
                    text_index += 1
                    continue
                new_text_node = TextNode(node_text_split[text_index], TextType.TEXT)
                text_index += 1
            new_nodes.append(new_text_node)
    return new_nodes