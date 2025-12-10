"""
Base Agent Module

Abstract base class for all agents in the content generation system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    """
    
    def __init__(self, name: str):
        """
        Initialize the base agent.
        
        Args:
            name: The agent's identifier
        """
        self.name = name
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return output.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Processed output data
        """
        pass
