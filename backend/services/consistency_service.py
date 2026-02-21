from typing import List, Dict
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# Load MNLI model once
_model_name = "roberta-large-mnli"
_tokenizer = AutoTokenizer.from_pretrained(_model_name)
_model = AutoModelForSequenceClassification.from_pretrained(_model_name)
_model.eval()


def _predict_nli(premise: str, hypothesis: str) -> str:
    inputs = _tokenizer(premise, hypothesis, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = _model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1).numpy()[0]

    # MNLI label order: contradiction, neutral, entailment
    labels = ["contradiction", "neutral", "entailment"]
    return labels[int(np.argmax(probs))]


def compute_consistency(reasoning_paths: List[Dict]) -> Dict:
    """
    Computes contradiction matrix and consistency score.
    consistency = 1 - contradiction_ratio
    """
    n = len(reasoning_paths)
    if n < 2:
        return {
            "consistency_score": 1.0,
            "contradiction_ratio": 0.0,
            "matrix": []
        }

    matrix = [[None] * n for _ in range(n)]
    contradictions = 0
    total_pairs = 0

    for i in range(n):
        for j in range(i + 1, n):
            premise = reasoning_paths[i]["text"]
            hypothesis = reasoning_paths[j]["text"]

            label = _predict_nli(premise, hypothesis)
            matrix[i][j] = label
            matrix[j][i] = label

            if label == "contradiction":
                contradictions += 1

            total_pairs += 1

    contradiction_ratio = contradictions / total_pairs if total_pairs else 0.0
    consistency_score = 1.0 - contradiction_ratio

    return {
        "consistency_score": consistency_score,
        "contradiction_ratio": contradiction_ratio,
        "matrix": matrix
    }