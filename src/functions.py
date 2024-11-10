from textnode import *
from htmlnode import *
import re
import os
import shutil

#recursive function to copy all files from static directory to public directory
def copy_static_to_public(src_dir="static", dest_dir="public", first_call=True):
    #delete everything in the public directory
    if os.path.exists(dest_dir) and first_call:
        print(f"Deleting directory: {dest_dir}, and all of these files: {os.listdir(dest_dir)}")
        shutil.rmtree(dest_dir)
    elif not os.path.exists(dest_dir) and first_call:
        print(f"Creating directory: {dest_dir}")
        os.makedirs(dest_dir)            
    #copy everything from static to public        
    for filename in os.listdir(src_dir):
        file_path = os.path.join(src_dir, filename)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        if os.path.isdir(file_path):
            print(f"Copying directory: {file_path}")
            copy_static_to_public(file_path, os.path.join(dest_dir, filename), first_call=False)
        else:
            print(f"Copying file: {file_path}")
            shutil.copy(file_path, dest_dir)

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value = text_node.text, props={})
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value = text_node.text, props={})
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value = text_node.text, props={})
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value = text_node.text, props={})
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value = text_node.text, props={"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    raise Exception("Invalid TextType")

def text_to_html_node(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    # Instead of returning the list directly, wrap it in a span
    return ParentNode("span", children=html_nodes)

def is_meaningful_text(text):
    return bool(text) and not text.isspace()

def extract_markdown_images(text):
    return list(re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text))

def extract_markdown_links(text):
    return list(re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text))

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            remainder = node.text
            image_tuples = extract_markdown_images(node.text)
            if not image_tuples:
                new_nodes.append(TextNode(remainder, TextType.TEXT))
                continue
            for alt_text, url in image_tuples:
                delimiter = f'![{alt_text}]({url})'
                split_texts = remainder.split(delimiter, 1)
                if split_texts[0].strip():
                    new_nodes.append(TextNode(split_texts[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

                if len(split_texts) > 1:
                    remainder = split_texts[-1]
            if remainder.strip():
                new_nodes.append(TextNode(remainder, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            remainder = node.text
            link_tuples = extract_markdown_links(node.text)
            if not link_tuples:
                new_nodes.append(TextNode(remainder, TextType.TEXT))
                continue
            for text, url in link_tuples:
                delimiter = f'[{text}]({url})'
                split_texts = remainder.split(delimiter, 1)
                if split_texts[0].strip():
                    new_nodes.append(TextNode(split_texts[0], TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.LINK, url))

                if len(split_texts) > 1:
                    remainder = split_texts[-1]
            if remainder.strip():
                new_nodes.append(TextNode(remainder, TextType.TEXT))
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = old_nodes.copy()
    new_nodes = []
    for node in nodes:
        print(f"Processing node: {node.text} with type: {node.text_type}")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            first_delimiter_pos = node.text.find(f"{delimiter}")
            if first_delimiter_pos == -1:
                new_nodes.append(node)
            else:
                remainder_text = node.text[first_delimiter_pos + len(delimiter):]

                if remainder_text.find(f'{delimiter}') == -1:
                    raise Exception("Need matching pairs of delimiters, bozo.")
                else:
                    second_delimiter_pos = remainder_text.find(f"{delimiter}") + first_delimiter_pos + len(delimiter)
                    str_to_format = node.text[first_delimiter_pos + len(delimiter):second_delimiter_pos]
                    first_string = node.text[:first_delimiter_pos]
                    last_string = node.text[second_delimiter_pos + len(delimiter):]
                    new_nodes.extend([
    node for node in [
        TextNode(first_string, TextType.TEXT),
        TextNode(str_to_format.strip(), text_type),
        TextNode(last_string.lstrip(), TextType.TEXT)
    ] if node.text.strip()
])
    return new_nodes
                
def text_to_textnodes(text):
    print(f"Processing text: {text}")
    tempnode = TextNode(text, TextType.TEXT)
    old_node = [tempnode]
    step0 = split_nodes_image(old_node)
    step1 = split_nodes_link(step0)
    step2 = split_nodes_delimiter(step1, "**", TextType.BOLD)
    print(f"After bold: {[node.text for node in step2]}")
    step3 = split_nodes_delimiter(step2, "*", TextType.ITALIC)
    print(f"After italic: {[node.text for node in step3]}")
    step4 = split_nodes_delimiter(step3, "`", TextType.CODE)
    return step4

def markdown_to_blocks(markdown):
    # First normalize all whitespace
    markdown = markdown.replace('\r\n', '\n')
    # Split into lines
    lines = markdown.splitlines()
    
    current_block = []
    blocks = []
    
    # Process line by line
    for line in lines:
        if line.strip() == "":
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line)
    
    # Don't forget the last block
    if current_block:
        blocks.append("\n".join(current_block))
    
    return [block.strip() for block in blocks if is_meaningful_text(block)]

def block_to_block_type(block):    
    split_block = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if all(line.startswith(">") for line in split_block):
        return "quote"
    if all(line.startswith(("* ", "- ")) for line in split_block):
        return "unordered_list"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if block.startswith("1. ") and all(line.startswith(f"{i+1}. ") for i, line in enumerate(split_block)):
        return "ordered_list"            
    return "paragraph"
        

def create_list_items(block):
    items = []
    for line in block.split("\n"):
        if line.startswith("* ") or line.startswith("- "):
            text_content = line[2:]
        else:
            text_content = line[line.index(" ")+1:]
        
        print(f"List item text content before processing: '{text_content}'")
        text_nodes = text_to_textnodes(text_content)
        html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        items.append(LeafNode("li", html_nodes))
    return items
def format_heading(block):
    level = block[:block.index(" ")].count("#")
    text = block[block.index(" ")+1:]
    return LeafNode(f"h{level}", text)

def format_quote(block):
    holder = []
    for line in block.split("\n"):
        holder.append(line.lstrip("> "))
    return LeafNode("blockquote", "\n".join(holder))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_html_node = ParentNode("div", children=[])    
    for block in blocks:
        block_type = block_to_block_type(block)
        print(f"Block: '{block}'")
        print(f"Type: {block_type}")
        if block_type == "heading":
            parent_html_node.children.append(format_heading(block))
        elif block_type == "quote":
            parent_html_node.children.append(format_quote(block))
        elif block_type == "ordered_list":
            list_items = create_list_items(block)
            parent_html_node.children.append(ParentNode("ol", children=list_items))
        elif block_type == "unordered_list":
            list_items = create_list_items(block)
            parent_html_node.children.append(ParentNode("ul", children=list_items))
        elif block_type == "code":
            parent_html_node.children.append(ParentNode("pre", children=[ParentNode("code", children=[text_to_html_node(block)])]))
        elif block_type == "paragraph":
            parent_html_node.children.append(ParentNode("p", children=[text_to_html_node(block)]))
    return parent_html_node

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    with open(from_path, "r") as f:
        markdown = f.read()
    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    with open(template_path, "r") as f:
        template = f.read()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_node.to_html())
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, entry))
        else:
            # preserve folder structure
            os.makedirs(dest_dir_path, exist_ok=True)
            if entry.endswith(".md"):
                generate_page(entry_path, template_path, os.path.join(dest_dir_path, entry.replace(".md", ".html")))