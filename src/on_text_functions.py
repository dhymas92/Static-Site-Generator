from textnode import TextType, TextNode

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
