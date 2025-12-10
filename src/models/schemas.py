"""
Data Schemas Module

Pydantic models for data validation.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum


class QuestionCategory(str, Enum):
    """Enum for question categories."""
    INFORMATIONAL = "Informational"
    SAFETY = "Safety"
    USAGE = "Usage"
    PURCHASE = "Purchase"
    COMPARISON = "Comparison"


class Product(BaseModel):
    """Schema for product information."""
    name: str = Field(..., description="Product name")
    concentration: str = Field(..., description="Product concentration")
    skin_type: List[str] = Field(..., description="Suitable skin types")
    key_ingredients: List[str] = Field(..., description="Key ingredients")
    benefits: List[str] = Field(..., description="Product benefits")
    how_to_use: str = Field(..., description="Usage instructions")
    side_effects: str = Field(..., description="Potential side effects")
    price: str = Field(..., description="Product price")


class Question(BaseModel):
    """Schema for question items."""
    id: str = Field(..., description="Question ID")
    text: str = Field(..., description="Question text")
    category: str = Field(..., description="Question category (Informational, Safety, Usage, Purchase, Comparison)")
    answer: Optional[str] = Field(default=None, description="Question answer")


class PageOutput(BaseModel):
    """Schema for page output."""
    page_type: str = Field(..., description="Type of page")
    content: dict = Field(..., description="Page content")


class FAQItem(BaseModel):
    """Schema for FAQ items."""
    question: str = Field(..., description="The FAQ question")
    answer: str = Field(..., description="The FAQ answer")


class ProductInfo(BaseModel):
    """Schema for product information (legacy)."""
    title: str = Field(..., description="Product title")
    description: str = Field(..., description="Product description")
    features: List[str] = Field(default_factory=list, description="Product features")


class ComparisonItem(BaseModel):
    """Schema for comparison items."""
    name: str = Field(..., description="Item name")
    attributes: dict = Field(default_factory=dict, description="Item attributes")


class ContentOutput(BaseModel):
    """Schema for content output."""
    content_type: str = Field(..., description="Type of content")
    data: dict = Field(default_factory=dict, description="Content data")
    metadata: Optional[dict] = Field(default=None, description="Optional metadata")
