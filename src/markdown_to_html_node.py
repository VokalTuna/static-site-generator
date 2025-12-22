from inline_markdown import text_to_textnodes
from textnode import TextType, TextNode,text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type is BlockType.CODE:
            sanitize = block.strip().split('\n')
            sanitize = '\n'.join(sanitize[1:-1]) if len(sanitize) > 2 else ""
            text_node = TextNode(sanitize,TextType.CODE)
            code_node = [text_node_to_html_node(text_node)]
            html_nodes.append(ParentNode("pre",code_node))
        if block_type is BlockType.PARAGRAPH:
            block = " ".join(block.strip().split('\n'))
            html_nodes.append(ParentNode("p",text_to_children(block)))
        if block_type is BlockType.ULIST:
            html_nodes.append(ParentNode("ul",text_to_list_items(block)))
    test = ParentNode("div",html_nodes)
    return test

# Forgot a text should be a text.
# A li tag can be a parent tag instead.
# Just pass the text value to
# text node to html node
def to_child_node(value):
    return LeafNode("li",value)

def text_to_list_items(text):
    list_items = text.strip().split('\n')
    nodes = map(to_child_node,list_items)
    return list(nodes)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
