from typing_extensions import Text
from htmlnode import HTMLNode, ParentNode,LeafNode
from textnode import TextType,TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Old nodes is a list.
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        # We only have a valid split if the length of the split is
        # odd numbers
        splitted = node.text.split(delimiter)
        splitted_nodes = []
        if len(splitted) % 2 == 0:
            raise ValueError("Invalid markdown syntax")
        for index in range(len(splitted)):
            if splitted[index] == "":
                continue
            if index % 2 == 0:
                splitted_nodes.append(TextNode(splitted[index],TextType.TEXT))
            else:
                splitted_nodes.append(TextNode(splitted[index],text_type))
        new_nodes.extend(splitted_nodes)
    return new_nodes

def split_nodes_func(old_nodes, extractor, text_to_list, text_type):
    new_nodes = []
    for old_node in old_nodes:
        extracted = extractor(old_node.text)
        if not extracted or old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        process_text = old_node.text
        if len(extracted) == 0:
            new_nodes.append(old_node)
        for text, url in extracted:
            section = text_to_list(process_text, text, url)
            if section[0] != "":
                new_nodes.append(TextNode(section[0],TextType.TEXT))
            new_nodes.append(TextNode(text,text_type,url))
            process_text = section[1]
        if process_text != "":
            new_nodes.append(TextNode(process_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    def text_to_list(original_text, text, url):
        return original_text.split(f"[{text}]({url})", 1)
    text_type = TextType.LINK
    return split_nodes_func(old_nodes, extract_markdown_links, text_to_list, text_type)

def split_nodes_image(old_nodes):
    def text_to_list(original_text, text, url):
        return original_text.split(f"![{text}]({url})", 1)
    text_type = TextType.IMAGE
    return split_nodes_func(old_nodes, extract_markdown_images, text_to_list, text_type)

# If we extract more text or values from a markdown.
# So can it be a good idea to use a higher order function?
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
