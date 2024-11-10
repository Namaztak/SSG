from textnode import *

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return f' href="{self.props["href"]}" target="{self.props["target"]}"'
    
    def __repr__(self):
        return f'HTMLNode(tag: {self.tag}, val: {self.value}, children: {self.children}, props: {self.props})'
    
    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
        return False

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.value = value


    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
            
        # Handle props if they exist
        props_str = ''
        if self.props:
            props_str = ' ' + ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        
        # Convert value to HTML string
        if isinstance(self.value, list):
            inner_html = ""
            for node in self.value:
                if isinstance(node, HTMLNode):  # This includes LeafNode
                    inner_html += node.to_html()
                else:
                    inner_html += str(node)
        else:
            # Handle string values as before
            inner_html = self.value
            
        return f'<{self.tag}{props_str}>{inner_html}</{self.tag}>'
    
    def __repr__(self):
        return f'LeafNode(tag: {self.tag}, val: {self.value}, props: {self.props})'
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if tag == None:
            raise ValueError("Parent with no tag?")

    def to_html(self):
        if self.children is None:
            raise ValueError("Parent needs children")
            
        child_html = []
        for child in self.children:
            child_html.append(child.to_html())
            
        # Handle props if they exist
        props_str = ''
        if self.props:
            props_str = ' ' + ' '.join(f'{key}="{value}"' for key, value in self.props.items())
            
        return f'<{self.tag}{props_str}>{"".join(child_html)}</{self.tag}>'
    
    def __repr__(self):
        return f'ParentNode(tag: {self.tag}, val: {self.value}, children: {self.children}, props: {self.props})'