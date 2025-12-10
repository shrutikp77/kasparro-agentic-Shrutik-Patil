"""
FAQ Agent Module

Agent responsible for generating FAQ content from product and question data using LLM.
"""

from typing import Any, Dict, List
from src.agents.base_agent import BaseAgent
from src.models.schemas import Product, Question
from src.templates.template_definitions import FAQTemplate
from src.llm_client import llm_client


class FAQGenerationAgent(BaseAgent):
    """
    Agent that generates FAQ entries from product and question data using LLM.
    Depends on parser and questions agents.
    """
    
    def __init__(self):
        """Initialize the FAQGenerationAgent with agent_id 'faq'."""
        super().__init__(agent_id="faq")
        self.dependencies: List[str] = ["parser", "questions"]
    
    def can_execute(self, completed_agents: List[str]) -> bool:
        """
        Check if this agent can execute.
        Returns True only if all dependencies have completed.
        
        Args:
            completed_agents: List of agent IDs that have completed execution
            
        Returns:
            True if all dependencies are in completed_agents
        """
        return all(dep in completed_agents for dep in self.dependencies)
    
    def execute(self, shared_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate FAQ content using LLM.
        
        Args:
            shared_data: Shared data dictionary with 'parser' and 'questions' keys
            
        Returns:
            Structured FAQ dictionary built using FAQTemplate
        """
        self.status = "running"
        
        product: Product = shared_data["parser"]
        questions: List[Question] = shared_data["questions"]
        
        # Format questions for LLM
        questions_text = "\n".join([f"{i+1}. [{q.category}] {q.text}" for i, q in enumerate(questions)])
        
        system_prompt = """You are a skincare product expert and customer service specialist.
Generate helpful, accurate, and engaging FAQ answers based on product data.
Answers should be informative yet concise (2-4 sentences each)."""
        
        user_prompt = f"""Generate FAQ answers for this product:

Product Data:
Name: {product.name}
Concentration: {product.concentration}
Skin Type: {', '.join(product.skin_type)}
Ingredients: {', '.join(product.key_ingredients)}
Benefits: {', '.join(product.benefits)}
Usage: {product.how_to_use}
Side Effects: {product.side_effects}
Price: {product.price}

Questions to answer:
{questions_text}

Return a JSON array with this structure:
[
  {{"question": "exact question text", "answer": "helpful answer based on product data"}},
  ...
]

Base all answers on the product data provided. Be helpful and accurate. Return ONLY valid JSON."""
        
        faq_items = llm_client.generate_json(system_prompt, user_prompt, max_tokens=2000)
        
        # Use FAQTemplate to build final output
        faq_output = FAQTemplate.build(faq_items)
        
        self.output = faq_output
        self.mark_complete()
        
        return faq_output

