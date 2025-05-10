class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_string = ""
        if self.props != None:
            for key in self.props:
                prop_string+= " " + key + '=\"'+self.props[key]+'\"'
        else:
            raise ValueError("this HTML tag has no attributes")
        return prop_string

    def __repr__(self):
        return f"HTMLNode(tag:\"{self.tag}\", value:\"{self.value}\", children: {self.children} , Attributes:{self.props_to_html()})"


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

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNodes must have a TAG")
        if self.children == []:
            raise ValueError("ParentsNoes must have CHILDREN")
        prop_string =""
        if self.props is not None:
            prop_string = self.props_to_html()
        children_strings =""
        for child in self.children:
            children_strings += child.to_html()
        return f"<{self.tag}{prop_string}>{children_strings}</{self.tag}>"
