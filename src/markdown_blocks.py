from textwrap import dedent
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE= "quote"
    ULIST = "unordered_list"
    OLIST= "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    filtered_blocks = [dedent(block).strip() for block in blocks if block.strip() != ""]
    return filtered_blocks



def block_to_block_type(block):
    if block[0] == "#":
        count = 0
        for char in block:
            if char != "#":
                break
            count += 1
        if len(block) == count:
            return BlockType.PARAGRAPH
        elif count <= 6 and block[count] == " ":
            return BlockType.HEADING
    if block[:3] == "```" and block[-3:] == "```" and len(block) >=6:
        return BlockType.CODE

    items = block.split("\n")

    #check for quote lines
    if block[0] == ">":
        for item in items:
            if item[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    #check for unordered list
    if block[0] == "-":
        for item in items:
            if item[:2] != "- ":
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    #check for ordered list
    if block[:3] == "1. ":
        for i, item in enumerate(items):
            expected = f"{i+1}. "
            if item[:len(expected)] != expected:
                return BlockType.PARAGRAPH
        return BlockType.OLIST
    return BlockType.PARAGRAPH
