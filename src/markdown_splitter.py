from textnode import TextNode, TextType

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