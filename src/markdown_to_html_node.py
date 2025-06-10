from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from textnode import TextNode, text_node_to_html_node, TextType

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        html_nodes.append(block_to_html_node(block))

    return ParentNode("div", html_nodes)


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)

    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)

    if block_type == BlockType.CODE:
        return code_to_html_node(block)

    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)

    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)

    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)

    raise  ValueError("Not a valid block type")


def text_to_children(text):
    children = list(map(text_node_to_html_node,
    text_to_textnodes(text)
    )
    )
    return children

def paragraph_to_html_node(block):
    paragraph = block.replace("\n", " ")
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    head_level = 0

    for char in block:
        if char != "#":
            break
        head_level += 1

    text = block[head_level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{head_level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")

    text = block[4: -3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [child])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []

    for line in lines:
        if not line.startswith(">"):  /
        new_lines.append(line.lstrip(">").strip())

    paragraph = " ".join(new_lines)
    children = text_to_children(paragraph)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []

    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul", html_items)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []

    for i, item in enumerate(items):
        expected = f"{i+1}. "
        text = item[len(expected):]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


# #only called for unordered_list and ordered_list found by block_to_block_type
# def markdown_list_to_nodes(markdown_block):
#     list_children_nodes = []
#     items = markdown_block.split("\n")
#     if markdown_block[:2] == "- ":
#         for item in items:
#             list_children_nodes.append(LeafNode("li", item.lstrip("- ")))
#     if markdown_block[:3] == "1. ":
#         for i, item in enumerate(items):
#             list_children_nodes.append(LeafNode("li", item.lstrip(f"{i+1} ")))
#     else:
#         raise Exception("not a valid list")
#     return list_children_nodes
