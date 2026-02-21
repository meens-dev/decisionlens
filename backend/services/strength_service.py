import re
from typing import List, Dict


_CAUSAL_CONNECTORS = {
    "because", "due to", "therefore", "hence", "thus", "so that", "as a result",
    "consequently", "leads to", "results in"
}

_CERTAINTY_STRONG = {
    "will", "clearly", "definitely", "highly likely", "very likely", "almost certainly",
    "strongly", "significantly"
}

_CERTAINTY_WEAK = {
    "might", "maybe", "possibly", "could", "uncertain", "not sure", "perhaps"
}


def _count_phrase_hits(text: str, phrases: set) -> int:
    t = text.lower()
    hits = 0
    for p in phrases:
        if p in t:
            hits += 1
    return hits


def _specificity_proxy(text: str) -> float:
    """
    Very lightweight specificity heuristic:
    - reward presence of numbers
    - reward presence of concrete-looking words (length >= 7)
    """
    numbers = len(re.findall(r"\d", text))
    long_words = len([w for w in re.findall(r"[A-Za-z]+", text) if len(w) >= 7])
    # Normalize roughly (cap to avoid rewarding verbosity)
    score = min(1.0, (numbers * 0.15) + (min(long_words, 6) * 0.1))
    return score


def compute_strength(reasoning_paths: List[Dict]) -> float:
    """
    Returns a strength score in [0, 1] based on simple heuristics.
    Avoids direct length reward; uses capped signals.
    """
    if not reasoning_paths:
        return 0.0

    per_arg_scores = []
    for rp in reasoning_paths:
        text = str(rp.get("text", "")).strip()
        if not text:
            per_arg_scores.append(0.0)
            continue

        causal = _count_phrase_hits(text, _CAUSAL_CONNECTORS)  # 0..n
        strong = _count_phrase_hits(text, _CERTAINTY_STRONG)   # 0..n
        weak = _count_phrase_hits(text, _CERTAINTY_WEAK)       # 0..n
        spec = _specificity_proxy(text)                        # 0..1

        # Map to bounded contributions (caps prevent verbosity bias)
        causal_score = min(1.0, causal * 0.35)
        certainty_score = max(0.0, min(1.0, (strong * 0.3) - (weak * 0.2) + 0.5))
        # spec already [0,1]

        # Weighted blend per argument
        arg_score = (0.4 * causal_score) + (0.35 * certainty_score) + (0.25 * spec)
        per_arg_scores.append(max(0.0, min(1.0, arg_score)))

    return sum(per_arg_scores) / len(per_arg_scores)