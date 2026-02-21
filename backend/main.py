from backend.services.strength_service import compute_strength
from backend.services.cohesion_service import compute_cohesion
import json
from backend.models.rule_based_model import RuleBasedReasoningModel


def main():
    decision_text = input("Enter your decision: ")

    model = RuleBasedReasoningModel()
    reasoning_paths = model.generate_reasoning(decision_text)
    strength = compute_strength(reasoning_paths)
    print(f"\nStrength score: {strength:.3f}\n")
    cohesion = compute_cohesion(reasoning_paths)
    print(f"Cohesion score: {cohesion:.3f}\n")

    print("\nGenerated Reasoning:\n")
    print(json.dumps(reasoning_paths, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()