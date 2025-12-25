

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    markdown = markdown.split("\n")
    title = markdown[0]
    if title[0] != "#":
        raise Exception("This is not a header.")

    return markdown[0].lstrip("#").strip()

def generate_page(from_path, template_path,dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read the markdown at from_path
    markdown = ''
    with open(from_path, "r") as file:
        markdown = file.read()
    # Read the template at template_path
    template = ''
    with open(template_path, "r") as file:
        template = file.read()
    # We pass the string through a function.
    # This function returns an object instance.
    # This object instance has to_html() function
    # which we invoke.
    html_string = markdown_to_html_node(markdown)
    html_string = html_string.to_html()
    title = extract_title(markdown)
    html_page = template.replace("{{ Title }}", title)
    html_final = html_page.replace("{{ Content }}", html_string)
    try:
        with open(dest_path, "w") as f:
            f.write(html_final)
    except Exception as e:
        print( f"Error: writing to file: {e}")
