class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    # def props_to_html(self):
    #     prop_string = ""
    #     if self.props != None:
    #         for key in self.props:
    #             prop_string+= " " + key + '=\"'+self.props[key]+'\"'
    #     else:
    #         raise ValueError("this HTML tag has no attributes")
    #     return prop_string
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value == None:
            raise ValueError("all leaf nodes must have a value")

        if self.tag == None:
            return self.value
        prop_string = ""
        if self.props is not None:
            prop_string = self.props_to_html()
        return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNodes must have a TAG")
        if self.children is None:
            raise ValueError("ParentsNodes must have CHILDREN")
        if self.children == []:
            raise ValueError("ParentsNodes must have CHILDREN")
        # prop_string =""
        # if self.props is not None:
        #     prop_string = self.props_to_html()
        children_strings = ""
        for child in self.children:
            children_strings += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_strings}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
