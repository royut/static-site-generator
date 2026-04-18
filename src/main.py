from textnode import TextNode
from copystatic import copy_files
from gencontent import generate_page


def main():
    source = 'static'
    destination = 'public'
    copy_files(source, destination)
    generate_page('content/index.md', 'template.html', 'public/index.html')


if __name__ == '__main__':
    main()