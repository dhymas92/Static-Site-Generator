from textnode import *

def main():
    test_node = TextNode("This is some test text",
                        TextType.LINK,
                        "https://www.boot.dev")
    print(test_node)

main()
