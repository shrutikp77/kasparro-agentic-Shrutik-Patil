"""
Validators Module

Validation functions for output quality and schema enforcement.
Ensures hard requirements are met (e.g., FAQ count >= 15).
"""

from typing import Dict, Any
from src.config import MIN_FAQ_COUNT


def validate_faq_count(faq_output: Dict[str, Any]) -> None:
    """
    Validate that FAQ output contains minimum required questions.
    
    Args:
        faq_output: FAQ output dictionary with 'faqs' key
        
    Raises:
        ValueError: If FAQ count is less than MIN_FAQ_COUNT
    """
    if not faq_output:
        raise ValueError("FAQ output is None or empty")
    
    if "faqs" not in faq_output:
        raise ValueError("FAQ output missing 'faqs' key")
    
    faqs = faq_output["faqs"]
    if not isinstance(faqs, list):
        raise ValueError(f"'faqs' must be a list, got {type(faqs)}")
    
    faq_count = len(faqs)
    if faq_count < MIN_FAQ_COUNT:
        raise ValueError(
            f"FAQ count ({faq_count}) is less than required minimum ({MIN_FAQ_COUNT}). "
            f"Assignment requires at least {MIN_FAQ_COUNT} FAQs."
        )


def validate_output_schema(output: Dict[str, Any], schema_type: str) -> None:
    """
    Validate that output has expected schema structure.
    
    Args:
        output: Output dictionary to validate
        schema_type: One of 'faq', 'product', 'comparison'
        
    Raises:
        ValueError: If schema validation fails
    """
    if not output:
        raise ValueError(f"{schema_type} output is None or empty")
    
    if "page_type" not in output:
        raise ValueError(f"{schema_type} output missing 'page_type' key")
    
    if output["page_type"] != schema_type:
        raise ValueError(
            f"Expected page_type '{schema_type}', got '{output['page_type']}'"
        )
    
    # Schema-specific validations
    if schema_type == "faq":
        validate_faq_count(output)
        
    elif schema_type == "product":
        if "sections" not in output:
            raise ValueError("Product output missing 'sections' key")
            
    elif schema_type == "comparison":
        if "products" not in output:
            raise ValueError("Comparison output missing 'products' key")
        if len(output["products"]) != 2:
            raise ValueError(
                f"Comparison must have exactly 2 products, got {len(output['products'])}"
            )
