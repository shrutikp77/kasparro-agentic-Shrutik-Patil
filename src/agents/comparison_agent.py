"""
Comparison Agent Module

Agent responsible for generating comparison content between products using LLM.
"""

from typing import Any, Dict, List
from src.agents.base_agent import BaseAgent
from src.models.schemas import Product
from src.templates.template_definitions import ComparisonTemplate
from src.llm_client import llm_client


class ComparisonAgent(BaseAgent):
    """
    Agent that generates comparison content between products using LLM.
    Depends on parser agent for product data.
    """
    
    def __init__(self):
        """Initialize the ComparisonAgent with agent_id 'comparison'."""
        super().__init__(agent_id="comparison")
        self.dependencies: List[str] = ["parser"]
    
    def can_execute(self, completed_agents: List[str]) -> bool:
        """
        Check if this agent can execute.
        Returns True only if the parser agent has completed.
        
        Args:
            completed_agents: List of agent IDs that have completed execution
            
        Returns:
            True if 'parser' is in completed_agents
        """
        return "parser" in completed_agents
    
    def execute(self, shared_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comparison page using LLM.
        
        Args:
            shared_data: Shared data dictionary with 'parser' key containing Product
            
        Returns:
            Structured comparison dictionary built using ComparisonTemplate
        """
        self.status = "running"
        
        product_a: Product = shared_data["parser"]
        
        # Step 1: Generate fictional competitor using LLM
        system_prompt = """You are a product data specialist. Create realistic fictional competitor products for comparison."""
        
        user_prompt = f"""Given this real product:
Name: {product_a.name}
Concentration: {product_a.concentration}
Skin Type: {', '.join(product_a.skin_type)}
Ingredients: {', '.join(product_a.key_ingredients)}
Benefits: {', '.join(product_a.benefits)}
Price: {product_a.price}

Create a fictional competitor product (Product B) with this exact JSON structure:
{{
  "name": "fictional product name (similar category but different brand)",
  "concentration": "different concentration of similar active ingredient",
  "skin_type": ["different skin types"],
  "key_ingredients": ["3-4 ingredients, some overlapping, some unique"],
  "benefits": ["2-3 benefits, some similar, some different"],
  "how_to_use": "usage instructions",
  "side_effects": "potential side effects",
  "price": "price in ₹ (make it 15-30% different)"
}}

Make it realistic and competitive. Return ONLY valid JSON."""
        
        product_b_data = llm_client.generate_json(system_prompt, user_prompt, max_tokens=800)
        
        # Ensure all required fields exist with defaults
        product_b_data.setdefault("name", "Competitor Vitamin C Serum")
        product_b_data.setdefault("concentration", "15% Vitamin C")
        product_b_data.setdefault("skin_type", ["Normal", "Dry"])
        product_b_data.setdefault("key_ingredients", ["Vitamin C", "Vitamin E"])
        product_b_data.setdefault("benefits", ["Brightening", "Anti-aging"])
        product_b_data.setdefault("how_to_use", "Apply 2-3 drops daily")
        product_b_data.setdefault("side_effects", "May cause mild irritation")
        product_b_data.setdefault("price", "₹799")
        
        product_b = Product(**product_b_data)
        
        # Step 2: Generate comparison analysis using LLM
        system_prompt = """You are a product comparison expert. Analyze and compare skincare products objectively."""
        
        user_prompt = f"""Compare these two products:

Product A: {product_a.name}
- Concentration: {product_a.concentration}
- Ingredients: {', '.join(product_a.key_ingredients)}
- Benefits: {', '.join(product_a.benefits)}
- Price: {product_a.price}
- Skin Type: {', '.join(product_a.skin_type)}

Product B: {product_b.name}
- Concentration: {product_b.concentration}
- Ingredients: {', '.join(product_b.key_ingredients)}
- Benefits: {', '.join(product_b.benefits)}
- Price: {product_b.price}
- Skin Type: {', '.join(product_b.skin_type)}

Generate a JSON comparison with:
{{
  "ingredient_comparison": {{
    "common": ["shared ingredients"],
    "unique_to_a": ["ingredients only in A"],
    "unique_to_b": ["ingredients only in B"],
    "analysis": "2 sentence comparison of ingredient profiles"
  }},
  "price_comparison": {{
    "price_difference": "₹ amount and percentage",
    "value_assessment": "which offers better value and why (2 sentences)"
  }},
  "effectiveness_comparison": {{
    "concentration_analysis": "comparison of active ingredient concentrations",
    "benefit_overlap": ["shared benefits"],
    "unique_benefits_a": ["benefits unique to A"],
    "unique_benefits_b": ["benefits unique to B"]
  }},
  "recommendation": "1-2 sentences on which product suits which skin type/concern better"
}}

Return ONLY valid JSON."""
        
        comparison_metrics = llm_client.generate_json(system_prompt, user_prompt, max_tokens=1200)
        
        # Structure using template
        template = ComparisonTemplate()
        comparison_output = template.build(
            product_a.model_dump(),
            product_b.model_dump(),
            [comparison_metrics]
        )
        
        self.output = comparison_output
        self.mark_complete()
        
        return comparison_output

