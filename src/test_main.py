import unittest
from main import *
from textnode import *
from htmlnode import *

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node_to_html_node(self):
        start_node = TextNode("blah", text_type=TextType.IMAGE, url="http://pics.com/puppy.jpg")
        end_node = text_node_to_html_node(start_node)
        self.assertEqual(end_node.tag, "img")
        self.assertEqual(end_node.value, "")
        self.assertDictEqual(end_node.props, {"src": "http://pics.com/puppy.jpg", "alt": "blah"})

    def test_split_nodes_delimiter_single(self):
        startnodes = test1 = [TextNode("This is **bold** text", TextType.TEXT)]
        end = split_nodes_delimiter(startnodes, "**", TextType.BOLD)
        print(end)

    def test_split_multiple_w_non_text(self):
        test2 = [
    TextNode("Regular text", TextType.TEXT),
    TextNode("Already bold", TextType.BOLD),
    TextNode("More text with **bold** inside", TextType.TEXT)
]
        end = split_nodes_delimiter(test2, "**", text_type=TextType.BOLD)
        print(f'!! {end} !!')

    def test_edge_case_empty_str(self):
        test3 = [
    TextNode("**Bold at start** then text", TextType.TEXT),
    TextNode("Text then **bold at end**", TextType.TEXT),
    TextNode("**", TextType.TEXT),  # Just delimiters
    TextNode("", TextType.TEXT)     # Empty text
]
        with self.assertRaises(Exception):
            split_nodes_delimiter(test3, "**", TextType.BOLD)
    
    def test_empty_strs(self):
        test_edge = [TextNode("**bold**", TextType.TEXT)]
        result = split_nodes_delimiter(test_edge, "**", TextType.BOLD)
        for node in result:
            print(f"Text: '{node.text}', Type: {node.text_type}")

    def test_skip_empty_nodes(self):
        node = TextNode("  **bold**  ", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)  # Should only create the bold node
        self.assertEqual(new_nodes[0].text, "bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_all_delimiter_types(self):
        # Test each format with text before, target text, and text after
        bold_node = TextNode("before **bold** after", TextType.TEXT)
        italic_node = TextNode("before *italic* after", TextType.TEXT)
        code_node = TextNode("before `code` after", TextType.TEXT)

        # Test each delimiter type
        bold_result = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        italic_result = split_nodes_delimiter([italic_node], "*", TextType.ITALIC)
        code_result = split_nodes_delimiter([code_node], "`", TextType.CODE)
        
        self.assertEqual(len(bold_result), 3)
        self.assertEqual(len(italic_result), 3)
        self.assertEqual(len(code_result), 3)
        self.assertEqual(bold_result[1].text_type, TextType.BOLD)
        self.assertEqual(italic_result[1].text_type, TextType.ITALIC)
        self.assertEqual(code_result[1].text_type, TextType.CODE)

    def test_extract_markdown_images(self):
        string = "She can join ![the rest of the gang](https://www.deviantart.com/michiartem/art/Yellow-raincoat-and-blue-hair-supremacy-907967590)."
        extract = extract_markdown_images(string)
        self.assertEqual(len(extract), 1)
    
    def test_extract_markdown_images(self):
        string = "She can join [the rest of the gang](https://www.deviantart.com/michiartem/art/Yellow-raincoat-and-blue-hair-supremacy-907967590)."
        extract = extract_markdown_links(string)
        self.assertEqual(len(extract), 1)

    def test_split_nodes_image(self):
        node = TextNode(
            "Hello ![alt text](image.png) world ![second](image2.png) end",
            TextType.TEXT
        )
        nodes = split_nodes_image([node])
        # How many nodes would you expect in the result?
        # What should each node contain?
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(nodes[4].text_type, TextType.TEXT)

        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[1].text, "alt text")
        self.assertEqual(nodes[2].text, " world ")
        self.assertEqual(nodes[3].text, "second")
        self.assertEqual(nodes[4].text, " end")

        self.assertEqual(nodes[1].url, "image.png")
        self.assertEqual(nodes[3].url, "image2.png")

    def test_split_nodes_link(self):
        node = TextNode(
            "This is [first link](https://boot.dev) and [second link](https://blog.boot.dev) end",
            TextType.TEXT
        )
        nodes = split_nodes_link([node])
        
        self.assertEqual(len(nodes), 5)
        
        # Check types
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text_type, TextType.LINK)
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        
        # Check text content
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "first link")
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[3].text, "second link")
        self.assertEqual(nodes[4].text, " end")
        
        # Check URLs
        self.assertEqual(nodes[1].url, "https://boot.dev")
        self.assertEqual(nodes[3].url, "https://blog.boot.dev")
    
    def test_markdown_to_blocks(self):
        string ='''
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item    
'''
        blocks = markdown_to_blocks(string)
        self.assertEqual(len(blocks), 3)

    def test_block_to_block_type1(self):
        block = '''1. Valid ordered lists
2. Lists that start with "1. " but don't continue properly
3. Different block types to ensure they're not mistakenly identified as ordered lists'''

        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_block_to_block_type2(self):
        block = '''1. Valid ordered lists
2.Lists that start with "1. " but don't continue properly
3. Different block types to ensure they're not mistakenly identified as ordered lists'''

        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type3(self):
        block = '''* Valid ordered lists
- Lists that start with "1. " but don't continue properly
* Different block types to ensure they're not mistakenly identified as ordered lists'''

        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type4(self):
        block = """```Valid ordered lists
2. Lists that start with "1. " but don't continue properly
3. Different block types to ensure they're not mistakenly identified as ordered lists```"""

        self.assertEqual(block_to_block_type(block), "code")

    def test_block_to_block_type5(self):
        block = """###### ```1. Valid ordered lists
2. Lists that start with "1. " but don't continue properly
3. Different block types to ensure they're not mistakenly identified as ordered lists```"""

        self.assertEqual(block_to_block_type(block), "heading")

    def test_block_to_block_type6(self):
        block = """># ```1. Valid ordered lists
>2. Lists that start with "1. " but don't continue properly
>3. Different block types to ensure they're not mistakenly identified as ordered lists```"""

        self.assertEqual(block_to_block_type(block), "quote")

    def test_markdown_to_html_node(self):
        markdown = """# Heading
    
This is a paragraph.

> This is a quote.

* List item 1
* List item 2

1. Numbered item 1
2. Numbered item 2

```Code block here```"""

        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[1].tag, "p")
        self.assertEqual(html_node.children[2].tag, "blockquote")
        self.assertEqual(html_node.children[3].tag, "ul")
        self.assertEqual(html_node.children[4].tag, "ol")
        self.assertEqual(html_node.children[5].tag, "pre")

if __name__ == "__main__":
    unittest.main()