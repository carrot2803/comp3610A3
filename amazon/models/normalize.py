import numpy as np


def normalize_scores(scores: np.ndarray, mask_val: float = -np.inf) -> np.ndarray:
    valid: np.ndarray = scores[scores != mask_val]
    if valid.size == 0:
        return np.full_like(scores, 3.0)
    min_s, max_s = valid.min(), valid.max()
    if max_s > min_s:
        scores = 1 + 4 * (scores - min_s) / (max_s - min_s)
    else:
        scores[:] = 3.0
    return scores
