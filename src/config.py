"""
Configuration Module

Centralized configuration for the content generation system.
"""

from typing import Dict, Any

# Sample product data - single source of truth
# Modify this to generate content for different products
SAMPLE_PRODUCT_DATA: Dict[str, Any] = {
    "name": "GlowBoost Vitamin C Serum",
    "concentration": "10% Vitamin C",
    "skin_type": ["Oily", "Combination"],
    "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
    "benefits": ["Brightening", "Fades dark spots"],
    "how_to_use": "Apply 2-3 drops in the morning before sunscreen",
    "side_effects": "Mild tingling for sensitive skin",
    "price": "₹699"
}
