class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # A string representing an html tag
        self.value = value # A string representing the value of the html tag.
        self.children = children # A list of HTMLNode objects which represent the children of the node
        self.props = props # A dictionary of attributes. An example would be anchor tag will have an href attribute

    def to_html(self):
        raise NotImplementedError("to_html method is not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        attributes = ""
        for val in self.props:
            attributes += f' {val}="{self.props[val]}"'
        return attributes

    def __repr__(self) -> str:
        represent = f"tag: {self.tag} " \
                    f"value: {self.value} " \
                    f"children: {self.children} "\
                    f"props: {self.props} "
        return represent

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no value")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        content = ""
        for child in self.children:
            content += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{content}</{self.tag}>'
