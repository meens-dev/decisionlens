from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load embedding model once (module-level singleton)
_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_cohesion(reasoning_paths: List[Dict]) -> float:
    """
    Computes average pairwise cosine similarity between reasoning texts.
    Returns score in [0, 1].
    """
    if not reasoning_paths or len(reasoning_paths) < 2:
        return 0.0

    texts = [str(rp.get("text", "")).strip() for rp in reasoning_paths]
    embeddings = _embedding_model.encode(texts)

    sim_matrix = cosine_similarity(embeddings)

    # Exclude diagonal (self-similarity)
    n = len(sim_matrix)
    pair_sims = []
    for i in range(n):
        for j in range(i + 1, n):
            pair_sims.append(sim_matrix[i][j])

    if not pair_sims:
        return 0.0

    # Normalize similarity from [-1,1] to [0,1]
    pair_sims = [(s + 1) / 2 for s in pair_sims]

    return float(np.mean(pair_sims))