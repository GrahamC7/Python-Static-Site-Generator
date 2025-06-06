from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode
from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]


def block_to_block_type(block):
    lines = block.split("\n")

    # Heading: starts with 1–6 '#' followed by a space
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Code block: starts and ends with ``` (allowing leading spaces)
    if len(lines) > 1 and lines[0].lstrip().startswith("```") and lines[-1].lstrip().startswith("```"):
        return BlockType.CODE

    # Quote block: every line must start with '>'
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # Unordered list: every line starts with '- '
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    # Ordered list: every line starts with '1. ', '2. ', etc.
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    # Default: paragraph
    return BlockType.PARAGRAPH



def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            level = len(block.split(" ")[0])
            content = block[level + 1:].strip()
            text_nodes = text_to_textnodes(content)
            html_children = [text_node_to_html_node(tn) for tn in text_nodes]
            children.append(ParentNode(f"h{level}", html_children))

        elif block_type == BlockType.PARAGRAPH:
            flat_block = re.sub(r"\s+", " ", block.strip())
            text_nodes = text_to_textnodes(flat_block)
            html_children = [text_node_to_html_node(tn) for tn in text_nodes]
            children.append(ParentNode("p", html_children))

        elif block_type == BlockType.QUOTE:
            quote_text = "\n".join([line[1:].lstrip() for line in block.splitlines()])
            text_nodes = text_to_textnodes(quote_text)
            html_children = [text_node_to_html_node(tn) for tn in text_nodes]
            children.append(ParentNode("blockquote", html_children))

        elif block_type == BlockType.UNORDERED_LIST:
            list_items = []
            for line in block.splitlines():
                content = line[2:]
                text_nodes = text_to_textnodes(content)
                html_children = [text_node_to_html_node(tn) for tn in text_nodes]
                list_items.append(ParentNode("li", html_children))
            children.append(ParentNode("ul", list_items))

        elif block_type == BlockType.ORDERED_LIST:
            list_items = []
            for line in block.splitlines():
                content = line[line.find(". ") + 2:]
                text_nodes = text_to_textnodes(content)
                html_children = [text_node_to_html_node(tn) for tn in text_nodes]
                list_items.append(ParentNode("li", html_children))
            children.append(ParentNode("ol", list_items))

        elif block_type == BlockType.CODE:
            code_lines = [line.strip() for line in block.splitlines()[1:-1]]
            code_text = "\n".join(code_lines) + "\n"
            code_node = text_node_to_html_node(TextNode(code_text, TextType.TEXT))
            children.append(ParentNode("pre", [ParentNode("code", [code_node])]))

    return ParentNode("div", children)
