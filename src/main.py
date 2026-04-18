import sys

from textnode import TextNode
from copystatic import copy_files
from gencontent import generate_pages_recursive


def main():
    basepath = '/'
    if sys.argv and len(sys.argv) >= 2:
        basepath = sys.argv[1]
    print(basepath)
    source = 'static'
    destination = 'docs'
    copy_files(source, destination)
    generate_pages_recursive('content', 'template.html', 'docs', basepath)


if __name__ == '__main__':
    main()