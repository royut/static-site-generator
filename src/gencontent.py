import os
from pathlib import Path

from block_markdown import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('# '):
            title = line[1:].strip()
            break
    return title


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    final_html_content = template.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(final_html_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        dest_dir_path_html = Path(dest_dir_path).with_suffix('.html')
        generate_page(dir_path_content, template_path, dest_dir_path_html)
        return
    for path in os.listdir(dir_path_content):
        generate_pages_recursive(os.path.join(dir_path_content, path), template_path, os.path.join(dest_dir_path, path))
    return