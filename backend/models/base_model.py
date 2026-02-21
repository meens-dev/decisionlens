from abc import ABC, abstractmethod
from typing import List, Dict


class BaseReasoningModel(ABC):
    """
    Abstract base class for all reasoning models.
    Every model must implement generate_reasoning().
    """

    @abstractmethod
    def generate_reasoning(self, decision_text: str) -> List[Dict]:
        """
        Given a decision text, return a list of reasoning paths.

        Each reasoning path must be a dictionary with:
            - id (int)
            - type (str)
            - text (str)

        Example:
        [
            {"id": 1, "type": "Financial Impact", "text": "..."},
            {"id": 2, "type": "Risk Exposure", "text": "..."},
        ]
        """
        pass