"""
Content Generators Module

Reusable content generation logic and utilities.
"""

from typing import Dict, Any, List
from src.models.schemas import Product, Question


def generate_benefits_block(product: Product) -> str:
    """
    Generate a formatted string describing product benefits.
    
    Args:
        product: Product instance with benefits information
        
    Returns:
        Formatted string describing product benefits
    """
    benefits_list = ", ".join(product.benefits)
    return f"{product.name} offers the following benefits: {benefits_list}. Formulated with {product.concentration} for optimal results."


def generate_usage_block(product: Product) -> str:
    """
    Generate formatted usage instructions.
    
    Args:
        product: Product instance with usage information
        
    Returns:
        Formatted usage instructions string
    """
    skin_types = ", ".join(product.skin_type)
    return f"How to use {product.name}: {product.how_to_use}. Best suited for {skin_types} skin types."


def generate_safety_block(product: Product) -> str:
    """
    Generate safety and side effects information.
    
    Args:
        product: Product instance with safety information
        
    Returns:
        Formatted safety information string
    """
    return f"Safety Information for {product.name}: {product.side_effects}. Please perform a patch test before regular use."


def generate_ingredients_block(product: Product) -> str:
    """
    Generate formatted ingredients description.
    
    Args:
        product: Product instance with ingredients information
        
    Returns:
        Formatted ingredients description string
    """
    ingredients_list = ", ".join(product.key_ingredients)
    return f"{product.name} contains the following key ingredients: {ingredients_list}. Concentration: {product.concentration}."


def compare_ingredients_block(product_a: Product, product_b: Product) -> Dict[str, Any]:
    """
    Compare ingredients between two products.
    
    Args:
        product_a: First product to compare
        product_b: Second product to compare
        
    Returns:
        Dictionary with comparison of ingredients between two products
    """
    common_ingredients = list(set(product_a.key_ingredients) & set(product_b.key_ingredients))
    unique_to_a = list(set(product_a.key_ingredients) - set(product_b.key_ingredients))
    unique_to_b = list(set(product_b.key_ingredients) - set(product_a.key_ingredients))
    
    return {
        "product_a_name": product_a.name,
        "product_b_name": product_b.name,
        "product_a_ingredients": product_a.key_ingredients,
        "product_b_ingredients": product_b.key_ingredients,
        "common_ingredients": common_ingredients,
        "unique_to_product_a": unique_to_a,
        "unique_to_product_b": unique_to_b,
        "product_a_concentration": product_a.concentration,
        "product_b_concentration": product_b.concentration
    }


def compare_price_block(product_a: Product, product_b: Product) -> Dict[str, Any]:
    """
    Compare prices and value proposition between two products.
    
    Args:
        product_a: First product to compare
        product_b: Second product to compare
        
    Returns:
        Dictionary comparing prices and value proposition
    """
    return {
        "product_a_name": product_a.name,
        "product_b_name": product_b.name,
        "product_a_price": product_a.price,
        "product_b_price": product_b.price,
        "product_a_benefits_count": len(product_a.benefits),
        "product_b_benefits_count": len(product_b.benefits),
        "product_a_ingredients_count": len(product_a.key_ingredients),
        "product_b_ingredients_count": len(product_b.key_ingredients),
        "comparison_summary": f"{product_a.name} ({product_a.price}) vs {product_b.name} ({product_b.price})"
    }


def generate_answer_block(question: Question, product: Product) -> str:
    """
    Generate an answer based on question category and content.
    Analyzes question text to provide unique, relevant answers.
    
    Args:
        question: Question instance with category and text information
        product: Product instance with relevant data
        
    Returns:
        Unique, relevant answer string based on question content
    """
    question_text = question.text.lower()
    category = question.category.upper()
    
    # First, check for specific keywords in question text for unique answers
    if "ingredient" in question_text:
        ingredients_list = ", ".join(product.key_ingredients)
        return f"{product.name} contains these key ingredients: {ingredients_list}. These are carefully selected to provide {', '.join(product.benefits).lower()}."
    
    if "concentration" in question_text:
        return f"The concentration of {product.name} is {product.concentration}. This concentration is optimized for effectiveness while being suitable for {', '.join(product.skin_type).lower()} skin types."
    
    if "benefit" in question_text:
        benefits_list = ", ".join(product.benefits)
        return f"The key benefits of {product.name} include: {benefits_list}. With {product.concentration}, it delivers visible results."
    
    if "side effect" in question_text or "warning" in question_text:
        return f"Possible side effects of {product.name}: {product.side_effects}. If irritation persists, discontinue use and consult a dermatologist."
    
    if "avoid" in question_text or "who should" in question_text:
        return f"People with extremely sensitive skin should patch test {product.name} first. {product.side_effects}. Pregnant or nursing women should consult a doctor before use."
    
    if "how" in question_text and ("apply" in question_text or "use" in question_text):
        return f"To apply {product.name}: {product.how_to_use}. For best results, use consistently as part of your skincare routine."
    
    if "when" in question_text or "time" in question_text:
        return f"The best time to use {product.name}: {product.how_to_use}. Vitamin C serums are most effective when applied in the morning for antioxidant protection."
    
    if "often" in question_text or "frequency" in question_text:
        return f"For {product.name}, daily use is recommended. {product.how_to_use}. Start with once daily and increase as your skin adjusts."
    
    if "price" in question_text or "cost" in question_text:
        return f"{product.name} is priced at {product.price}. This includes {product.concentration} with key ingredients like {', '.join(product.key_ingredients)}."
    
    if "buy" in question_text or "where" in question_text:
        return f"You can purchase {product.name} at {product.price} from authorized retailers, the official website, or major e-commerce platforms."
    
    if "worth" in question_text or "value" in question_text:
        return f"At {product.price}, {product.name} offers excellent value with {product.concentration} and benefits including {', '.join(product.benefits).lower()}. It's suitable for {', '.join(product.skin_type).lower()} skin."
    
    if "compare" in question_text or "alternative" in question_text or "vs" in question_text:
        return f"{product.name} stands out with {product.concentration} and unique ingredients: {', '.join(product.key_ingredients)}. Key differentiators include: {', '.join(product.benefits)}."
    
    if "does" in question_text and "do" in question_text:
        benefits_list = ", ".join(product.benefits)
        return f"{product.name} is designed to provide: {benefits_list}. It's formulated with {product.concentration} for optimal effectiveness."
    
    # Fall back to category-based answers
    if category == "INFORMATIONAL":
        benefits_list = ", ".join(product.benefits)
        return f"{product.name} is formulated with {product.concentration}. Key benefits include: {benefits_list}."
    
    elif category == "SAFETY":
        return f"Regarding safety for {product.name}: {product.side_effects}. Always perform a patch test before regular use."
    
    elif category == "USAGE":
        skin_types = ", ".join(product.skin_type)
        return f"Usage instructions for {product.name}: {product.how_to_use}. This product is suitable for {skin_types} skin types."
    
    elif category == "PURCHASE":
        return f"{product.name} is available at {product.price}. It contains {', '.join(product.key_ingredients)} and is suitable for {', '.join(product.skin_type)} skin."
    
    elif category == "COMPARISON":
        ingredients_list = ", ".join(product.key_ingredients)
        return f"{product.name} features {product.concentration} with key ingredients: {ingredients_list}. Benefits include: {', '.join(product.benefits)}."
    
    else:
        return f"For more information about {product.name}, please refer to the product details or contact customer support."


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
