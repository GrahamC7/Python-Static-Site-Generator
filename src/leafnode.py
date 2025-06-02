from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)
        if value is None:
            raise ValueError("LeafNode must have a value")
        
    def to_html(self):
        if self.tag is None:
            return self.value
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        

            