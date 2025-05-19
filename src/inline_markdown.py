from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        sections = old_node.text.split(delimiter)
        if(len(sections) % 2 == 0):
            raise Exception("invalid markdown, formatted section not closed")
        for i in range(0, len(sections)):
            if sections[i] =="":
                continue
            #even indexes are before and after a delimiter block, and thus always plain text
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            #odd indexes are between delimiters, thus always a delimiter type
            if i % 2 == 1:
                new_nodes.append(TextNode(sections[i], text_type))


    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text == None:
            new_nodes.append(old_node)
            continue

        temp_text = old_node.text
        image_touple = extract_markdown_images(temp_text)

        if len(image_touple) == 0:
            new_nodes.append(old_node)
            continue

        for tup in image_touple:
            alt = tup[0]
            link = tup[1]
            result = temp_text.split(f"![{alt}]({link})",1)
            if result[0] != "":
                new_nodes.append(TextNode(result[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            temp_text = result[1]

        if temp_text != "":
            new_nodes.append(TextNode(temp_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        temp_text = old_node.text
        link_touple = extract_markdown_links(temp_text)


        if len(link_touple) == 0:
            new_nodes.append(old_node)
            continue

        for tup in link_touple:
            alt = tup[0]
            link = tup[1]
            result = temp_text.split(f"[{alt}]({link})",1)
            if result[0] != "":
                new_nodes.append(TextNode(result[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, link))
            temp_text = result[1]

        if temp_text != "":
            new_nodes.append(TextNode(temp_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    delimiters = {TextType.BOLD: "**", TextType.ITALIC: "_", TextType.CODE: "`"}

    for type in delimiters:
        symb = delimiters[type]
        nodes = split_nodes_delimiter(nodes, symb, type)

    nodes = split_nodes_link(split_nodes_image(nodes))

    return nodes



def extract_markdown_images(text):
    image_text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_text

def extract_markdown_links(text):
    link_text = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_text


text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
print(text_to_textnodes(text))
