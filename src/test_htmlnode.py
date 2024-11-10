import unittest
from functions import *
from htmlnode import *

# HTMLNODE TESTS
class TestHTMLNode(unittest.TestCase):
    def test_eq_empty_all(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_diff_props(self):
        node = HTMLNode(props={"href": "http://reddit.com/r/gonewildaudio",
                               "target": "_blank"})
        node2 = HTMLNode(props={"href": "http://reddit.com/r/gonewildaudio",
                               "target": "poop"})
        print(node2.props_to_html())
        self.assertNotEqual(node, node2)

    def test_diff_tag(self):
        node = HTMLNode(tag="hash")
        node2 = HTMLNode(tag="tag")
        self.assertNotEqual(node, node2)

    def test_diff_value(self):
        node = HTMLNode(value="heehee haw haw")
        node2 = HTMLNode(value="lmao")
        self.assertNotEqual(node, node2)

    def test_children(self):
        node = HTMLNode(children="bob")
        node2 = HTMLNode(children="stacy and steve")
        self.assertNotEqual(node, node2)

    def test_self_report(self):
        node = HTMLNode()
        print(node)


# LEAFNODE TESTS
    def test_leaf_self_report(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        print(node)
        print(node2)

    def test_leaf_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        print(node.to_html())
        print(node2.to_html())


# PARENTNODE TESTS
    def test_parent_alone(self):
        parent1 = ParentNode("div", [
    LeafNode("span", "Hello"),
    LeafNode("br", None),
    LeafNode(None, "World")
])
        print(parent1)

    def test_parent_nesting(self):
        parent2 = ParentNode("section", [
    ParentNode("article", [
        LeafNode("h1", "Title"),
        LeafNode("p", "Content")
    ]),
    LeafNode("footer", "Copyright 2024")
])
        print(parent2)

    def test_deeper_parent(self):
        parent3 = ParentNode("nav", [
    ParentNode("ul", [
        ParentNode("li", [
            LeafNode("a", "Home")
        ]),
        ParentNode("li", [
            LeafNode("a", "About")
        ])
    ]),
    LeafNode("span", "Menu")
])
        print(parent3)

    def test_parent_eq(self):
        parent3 = ParentNode("nav", [
    ParentNode("ul", [
        ParentNode("li", [
            LeafNode("a", "Home")
        ]),
        ParentNode("li", [
            LeafNode("a", "About")
        ])
    ]),
    LeafNode("span", "Menu")
])
        parent2 = ParentNode("section", [
    ParentNode("article", [
        LeafNode("h1", "Title"),
        LeafNode("p", "Content")
    ]),
    LeafNode("footer", "Copyright 2024")
])
        print(parent3 == parent2)

    def test_parent_to_html(self):
        parent3 = ParentNode("nav", [
    ParentNode("ul", [
        ParentNode("li", [
            LeafNode("a", "Home")
        ]),
        ParentNode("li", [
            LeafNode("a", "About")
        ])
    ]),
    LeafNode("span", "Menu")
])
        parent2 = ParentNode("section", [
    ParentNode("article", [
        LeafNode("h1", "Title"),
        LeafNode("p", "Content")
    ]),
    LeafNode("footer", "Copyright 2024")
])
        print(parent3.to_html())
        print(parent2.to_html())

    def test_broken_parent(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [
    LeafNode("p", "This won't work")
])


    def test_busted_parent_kids(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])


    def test_None_kids(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)


    
    def test_busted_family_tree(self):
        with self.assertRaises(ValueError):
            ParentNode("section", [
    ParentNode(None, [
        LeafNode("p", "Nested invalid parent")
    ])
])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("* This is *italic* text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        assert len(nodes) == 3
        assert nodes[0].text == "This is "
        assert nodes[1].text == "italic"
        assert nodes[1].text_type == TextType.ITALIC
        assert nodes[2].text == " text"


if __name__ == "__main__":
    unittest.main()