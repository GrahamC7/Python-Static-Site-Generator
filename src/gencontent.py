import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, base_path="/"):
    print(f" * {from_path} {template_path} -> {dest_path}")
    with open(from_path, "r") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as to_file:
        to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if not file.endswith(".md"):
                continue

            md_path = os.path.join(root, file)
            relative_path = os.path.relpath(md_path, dir_path_content)
            html_path = os.path.join(dest_dir_path, relative_path).replace(".md", ".html")

            os.makedirs(os.path.dirname(html_path), exist_ok=True)
            print(f" * {md_path} {template_path} -> {html_path}")
            generate_page(md_path, template_path, html_path, base_path)
