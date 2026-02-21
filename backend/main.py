import json
from backend.models.rule_based_model import RuleBasedReasoningModel
from backend.pipeline.scoring_pipeline import run_scoring_pipeline


def main():
    decision_text = input("Enter your decision: ")

    model = RuleBasedReasoningModel()
    reasoning_paths = model.generate_reasoning(decision_text)

    analysis = run_scoring_pipeline(reasoning_paths)

    print("\n=== Decision Analysis ===\n")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()