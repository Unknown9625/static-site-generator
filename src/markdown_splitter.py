from textnode import TextNode, TextType
from markdown_parser import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            result.append(old_node)
            continue
        
        text = old_node.text
        pieces = []
        remaining_text = text

        if delimiter not in remaining_text:
            result.append(old_node)
            continue
        
        while delimiter in remaining_text:
            start_idx = remaining_text.find(delimiter)
            before_text = remaining_text[:start_idx]
            remaining_after_delimiter = remaining_text[start_idx + len(delimiter):]
            end_idx = remaining_after_delimiter.find(delimiter)
            if end_idx == -1:
                raise ValueError(f"Opening delimiter {delimiter} found, but no closing delimiter")
            
            delimited_text = remaining_after_delimiter[:end_idx]
            remaining_text = remaining_after_delimiter[end_idx + len(delimiter):]
            
            if before_text:
                pieces.append(TextNode(before_text, TextType.NORMAL_TEXT))
            pieces.append(TextNode(delimited_text, text_type))

        if remaining_text:
            pieces.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
        result.extend(pieces)

    return result

def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            result.append(old_node)
            continue
            
        text = old_node.text
        images = extract_markdown_images(text)
        
        if not images:
            result.append(old_node)
            continue

        current_text = text
        new_nodes = []

        for alt_text, image_url in images:
            image_markdown = f"![{alt_text}]({image_url})"
            parts = current_text.split(image_markdown, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
            current_text = parts[1] if len(parts) > 1 else ""

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL_TEXT))
        result.extend(new_nodes)

    return result

def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:  
        if old_node.text_type != TextType.NORMAL_TEXT:
            result.append(old_node)
            continue
            
        text = old_node.text
        links = extract_markdown_links(text)
        
        if not links:
            result.append(old_node)
            continue
        
        current_text = text
        new_nodes = []
        
        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            parts = current_text.split(link_markdown, 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            current_text = parts[1] if len(parts) > 1 else ""
        
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL_TEXT))
        result.extend(new_nodes)
    
    return result

def markdown_to_blocks(markdown):
    potential_blocks = markdown.split("\n\n")
    stripped_blocks = [block.strip() for block in potential_blocks]
    non_empty_blocks = [block for block in stripped_blocks if block]

    return non_empty_blocks