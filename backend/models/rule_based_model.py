from typing import List, Dict
from .base_model import BaseReasoningModel


class RuleBasedReasoningModel(BaseReasoningModel):
    """
    Deterministic baseline reasoning model.
    Generates structured reasoning across fixed dimensions.
    """

    def generate_reasoning(self, decision_text: str) -> List[Dict]:
        decision_text = decision_text.strip()

        return [
            {
                "id": 1,
                "type": "Financial Impact",
                "text": f"From a financial perspective, the decision '{decision_text}' may influence income stability, expenses, or long-term monetary growth."
            },
            {
                "id": 2,
                "type": "Risk Exposure",
                "text": f"The decision '{decision_text}' involves uncertainty and potential risks that could affect short-term and long-term outcomes."
            },
            {
                "id": 3,
                "type": "Long-Term Growth",
                "text": f"In terms of long-term development, '{decision_text}' may create opportunities for skill growth, experience, and future advancement."
            },
            {
                "id": 4,
                "type": "Emotional Impact",
                "text": f"Emotionally, the decision '{decision_text}' could influence stress levels, motivation, and overall personal satisfaction."
            },
            {
                "id": 5,
                "type": "Opportunity Cost",
                "text": f"Choosing '{decision_text}' may mean giving up alternative opportunities, which should be evaluated carefully."
            },
        ]