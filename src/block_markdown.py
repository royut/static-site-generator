def markdown_to_blocks(text):
    blocks = text.split('\n\n')
    blocks = list(map(lambda block: block.strip(), blocks))
    blocks = list(filter(lambda block: block != '', blocks))
    return blocks