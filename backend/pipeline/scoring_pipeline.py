from typing import List, Dict
import time

from backend.services.strength_service import compute_strength
from backend.services.cohesion_service import compute_cohesion
from backend.services.consistency_service import compute_consistency
from backend.services.confidence_service import compute_confidence


def run_scoring_pipeline(reasoning_paths: List[Dict]) -> Dict:
    """
    Orchestrates all scoring services and returns structured analysis.
    """

    start_time = time.time()

    strength = compute_strength(reasoning_paths)
    cohesion = compute_cohesion(reasoning_paths)
    consistency_data = compute_consistency(reasoning_paths)

    confidence_data = compute_confidence(
        consistency=consistency_data["consistency_score"],
        strength=strength,
        cohesion=cohesion,
    )

    end_time = time.time()

    return {
        "reasoning_paths": reasoning_paths,
        "strength_score": strength,
        "cohesion_score": cohesion,
        "consistency": consistency_data,
        "confidence": confidence_data,
        "runtime_seconds": round(end_time - start_time, 3),
    }