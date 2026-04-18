from textnode import TextNode
from copystatic import copy_files


def main():
    textnode = TextNode('This is some anchor text', 'link', 'https://www.boot.dev')
    print(textnode)
    source = 'static'
    destination = 'public'
    copy_files(source, destination)


if __name__ == '__main__':
    main()