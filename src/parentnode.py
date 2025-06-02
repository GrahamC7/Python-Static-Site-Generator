from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, children)
        if children is None:
            children = []
        self.children = children
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        children_html = ''.join(child.to_html() for child in self.children)
        return f'<{self.tag}>{children_html}</{self.tag}>'