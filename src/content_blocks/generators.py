"""
Content Generators Module

Utility functions for deterministic content operations.
LLM handles intelligent content generation; these are fallback/utility functions.
"""

import re
from typing import Dict, Any, List
from src.models.schemas import Product


def extract_product_summary(product: Product) -> str:
    """
    Quick summary extraction without LLM (deterministic).
    
    Args:
        product: Product instance
        
    Returns:
        Brief product summary string
    """
    return f"{product.name} - {product.concentration} for {', '.join(product.skin_type)} skin"


def calculate_price_difference(price_a: str, price_b: str) -> Dict[str, str]:
    """
    Pure math calculation for price comparison (deterministic).
    
    Args:
        price_a: First price string (e.g., "₹1299")
        price_b: Second price string (e.g., "₹899")
        
    Returns:
        Dictionary with difference amount and percentage
    """
    match_a = re.search(r'\d+', price_a)
    match_b = re.search(r'\d+', price_b)
    
    if not match_a or not match_b:
        return {"difference": "N/A", "percentage": "N/A"}
    
    a = int(match_a.group())
    b = int(match_b.group())
    diff = abs(a - b)
    percent = round((diff / min(a, b)) * 100, 1) if min(a, b) > 0 else 0
    
    return {"difference": f"₹{diff}", "percentage": f"{percent}%"}


def extract_common_ingredients(product_a: Product, product_b: Product) -> List[str]:
    """
    Find common ingredients between two products (deterministic).
    
    Args:
        product_a: First product
        product_b: Second product
        
    Returns:
        List of common ingredients
    """
    return list(set(product_a.key_ingredients) & set(product_b.key_ingredients))


def extract_unique_ingredients(product: Product, other_product: Product) -> List[str]:
    """
    Find ingredients unique to a product (deterministic).
    
    Args:
        product: Product to find unique ingredients for
        other_product: Product to compare against
        
    Returns:
        List of unique ingredients
    """
    return list(set(product.key_ingredients) - set(other_product.key_ingredients))


def generate_content_block(block_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a content block based on type and data.
    
    Args:
        block_type: Type of content block to generate
        data: Data to use for generation
        
    Returns:
        Generated content block
    """
    return {"type": block_type, "content": data}


def merge_content_blocks(blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge multiple content blocks into a single output.
    
    Args:
        blocks: List of content blocks to merge
        
    Returns:
        Merged content
    """
    return {"blocks": blocks}

