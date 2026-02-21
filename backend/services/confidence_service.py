from backend.services.scoring_config import (
    WEIGHT_CONSISTENCY,
    WEIGHT_STRENGTH,
    WEIGHT_COHESION,
    LOW_THRESHOLD,
    HIGH_THRESHOLD,
)


def compute_confidence(consistency: float, strength: float, cohesion: float) -> dict:
    """
    Computes final confidence score using weighted aggregation.
    Returns:
        {
            "confidence_score": float,
            "confidence_label": str,
            "breakdown": {...}
        }
    """

    confidence_score = (
        WEIGHT_CONSISTENCY * consistency
        + WEIGHT_STRENGTH * strength
        + WEIGHT_COHESION * cohesion
    )

    # Clamp safety
    confidence_score = max(0.0, min(1.0, confidence_score))

    if confidence_score < LOW_THRESHOLD:
        label = "Low"
    elif confidence_score < HIGH_THRESHOLD:
        label = "Moderate"
    else:
        label = "High"

    return {
        "confidence_score": confidence_score,
        "confidence_label": label,
        "breakdown": {
            "consistency": consistency,
            "strength": strength,
            "cohesion": cohesion,
            "weights": {
                "consistency": WEIGHT_CONSISTENCY,
                "strength": WEIGHT_STRENGTH,
                "cohesion": WEIGHT_COHESION,
            },
        },
    }