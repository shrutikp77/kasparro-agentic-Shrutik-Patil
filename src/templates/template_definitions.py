"""
Template Definitions Module

Defines templates for various content types.
"""

from typing import Dict, Any


# Template definitions
TEMPLATES: Dict[str, Dict[str, Any]] = {
    "faq": {
        "name": "FAQ Template",
        "fields": ["question", "answer"],
    },
    "product": {
        "name": "Product Template",
        "fields": ["title", "description", "features"],
    },
    "comparison": {
        "name": "Comparison Template",
        "fields": ["items", "criteria"],
    },
}


def get_template(template_name: str) -> Dict[str, Any]:
    """
    Get a template by name.
    
    Args:
        template_name: Name of the template
        
    Returns:
        Template definition
    """
    return TEMPLATES.get(template_name, {})


def list_templates() -> list:
    """
    List all available templates.
    
    Returns:
        List of template names
    """
    return list(TEMPLATES.keys())
