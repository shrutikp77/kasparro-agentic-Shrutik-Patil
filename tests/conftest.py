"""
Pytest configuration and fixtures for tests.

Provides mocked LLM client and test data fixtures.
"""

import pytest
from unittest.mock import MagicMock
from typing import Dict, Any


@pytest.fixture
def mock_llm_client():
    """Provide a mocked LLM client for tests."""
    mock = MagicMock()
    
    # Default JSON response for generate_json
    mock.generate_json.return_value = [
        {"id": "q1", "text": "Sample question 1?", "category": "INFORMATIONAL"},
        {"id": "q2", "text": "Sample question 2?", "category": "SAFETY"}
    ]
    
    # Default text response for generate
    mock.generate.return_value = "Sample response"
    
    return mock


@pytest.fixture
def sample_product_data():
    """Provide sample product data for tests (not hardcoded in code)."""
    return {
        "name": "Test Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_type": ["Oily", "Combination"],
        "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"],
        "how_to_use": "Apply 2-3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price": "₹699"
    }


@pytest.fixture
def mock_faq_response():
    """Provide mock FAQ response with 15+ questions."""
    return [
        {"question": f"Question {i}?", "answer": f"Answer {i}."}
        for i in range(1, 16)
    ]


@pytest.fixture(autouse=True)
def reset_llm_client():
    """Reset LLM client before each test."""
    from src.llm_client import reset_llm_client
    reset_llm_client()
    yield
    reset_llm_client()
