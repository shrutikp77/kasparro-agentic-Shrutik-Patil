"""
Data Schemas Module

Pydantic models for data validation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class FAQItem(BaseModel):
    """Schema for FAQ items."""
    question: str = Field(..., description="The FAQ question")
    answer: str = Field(..., description="The FAQ answer")


class ProductInfo(BaseModel):
    """Schema for product information."""
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
