from markdown_to_html_node import *
import inline_markdown


def main():
    md = """
   ```
   This is text that _should_ remain
   the **same** even with inline stuff
   ```
   """
    node = markdown_to_html_node(md)
    html = node.to_html()
    print(html)


main()
