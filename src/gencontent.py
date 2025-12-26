import os
from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    markdown = markdown.split("\n")
    title = markdown[0]
    if not title.startswith("# "):
        raise Exception("This is not a title.")

    return markdown[0].lstrip("#").strip()

def generate_page(from_path, template_path,dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ''
    with open(from_path, "r") as file:
        markdown = file.read()

    template = ''
    with open(template_path, "r") as file:
        template = file.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for content in contents:
        full_path = os.path.join(dir_path_content, content)
        if os.path.isfile(full_path) and content.endswith(".md"):
            # give the markdown file an html ending
            content_html = content[:-3] + ".html"
            generate_page(
                full_path,
                template_path,
                os.path.join(dest_dir_path, content_html)
            )
        elif os.path.isdir(full_path):
            generate_pages_recursive(
                full_path,
                template_path,
                os.path.join(dest_dir_path, content)
            )
