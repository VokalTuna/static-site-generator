from enum import Enum
import re

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if re.match(r"^#{1,6} ",lines[0]):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(re.match(r"^>\s?.*$", line) for line in lines):
        return BlockType.QUOTE
    if all(re.match(r"^- ", line) for line in lines):
        return BlockType.ULIST
    ordered_list_pattern = [rf"{i}\. " for i in range(1, len(lines) + 1)]
    if all(re.match(rf"^{ordered_list_pattern[i]}.*$", lines[i]) for i in range(len(lines))):
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip() # All whitespace are removed, including newline
    return list(filter(lambda x: x,blocks))
    # If an element only had a newline because of excessive use of it,
    # so will they be empty because of previous step, and removed here.

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level +1 >= len(block):
        # This will only happens is the length of the block is more than characters
        # for the entire block and that there is noe text after the #
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:] # We slice the string from the level plus one and to the end.
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block [4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        # Takes advantage that ordered list starts with three letters in.
        # This solution does not take 10 or more lines in consideration.
        children = text_to_children(text)
        html_items.append(ParentNode("li",children))
        # The li tag is a ParentNode because the subsequent text
        # can also be bold, link, or other.
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li",children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
        # Argh! The lstrip function never came up on search.
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
