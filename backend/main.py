import json
from backend.models.rule_based_model import RuleBasedReasoningModel


def main():
    decision_text = input("Enter your decision: ")

    model = RuleBasedReasoningModel()
    reasoning_paths = model.generate_reasoning(decision_text)

    print("\nGenerated Reasoning:\n")
    print(json.dumps(reasoning_paths, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()