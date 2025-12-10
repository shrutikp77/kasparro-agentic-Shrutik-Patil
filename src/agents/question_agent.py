"""
Question Agent Module

Agent responsible for generating questions from product content using LLM.
"""

from typing import Any, Dict, List
from src.agents.base_agent import BaseAgent
from src.models.schemas import Product, Question, QuestionCategory
from src.llm_client import llm_client


class QuestionGenerationAgent(BaseAgent):
    """
    Agent that generates categorized questions based on product information.
    Uses LLM to generate diverse, natural questions.
    Depends on the parser agent to provide product data.
    """
    
    def __init__(self):
        """Initialize the QuestionGenerationAgent with agent_id 'questions'."""
        super().__init__(agent_id="questions")
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
    
    def execute(self, shared_data: Dict[str, Any]) -> List[Question]:
        """
        Generate questions using LLM.
        
        Args:
            shared_data: Shared data dictionary with 'parser' key containing Product
            
        Returns:
            List of Question objects
        """
        self.status = "running"
        
        product: Product = shared_data["parser"]
        
        system_prompt = """You are a product content specialist. Generate diverse, natural user questions about skincare products.
Questions should cover multiple categories: Informational, Safety, Usage, Purchase, and Comparison."""
        
        user_prompt = f"""Given this product data:
Name: {product.name}
Concentration: {product.concentration}
Skin Type: {', '.join(product.skin_type)}
Ingredients: {', '.join(product.key_ingredients)}
Benefits: {', '.join(product.benefits)}
Usage: {product.how_to_use}
Side Effects: {product.side_effects}
Price: {product.price}

Generate EXACTLY 15 user questions across these categories:
- 4 INFORMATIONAL questions (about benefits, ingredients, what it does, concentration)
- 3 SAFETY questions (side effects, who should avoid, warnings, allergies)
- 3 USAGE questions (how to apply, when to use, frequency, routine placement)
- 3 PURCHASE questions (price, value, where to buy, alternatives)
- 2 COMPARISON questions (vs other products, how it differs)

Return ONLY a JSON array with this structure:
[
  {{"id": "q1", "text": "question text here", "category": "INFORMATIONAL"}},
  {{"id": "q2", "text": "question text here", "category": "SAFETY"}},
  ...
]

Use natural language. Make questions realistic and varied."""
        
        response = llm_client.generate_json(system_prompt, user_prompt)
        
        # Convert to Question objects
        questions: List[Question] = []
        for q_data in response:
            questions.append(Question(
                id=q_data["id"],
                text=q_data["text"],
                category=q_data["category"]
            ))
        
        self.output = questions
        self.mark_complete()
        
        return questions
