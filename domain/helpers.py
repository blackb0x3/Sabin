import logging

import numpy as np


def round_to_multiple(number: int, multiple: int):
    return multiple * round(number / multiple)


def cosine_similarity(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    logging.debug({'msg': 'cosine_similarity debug stuff', 'a': a, 'b': b})
    if a is None or b is None:
        return 0
    dot_prod = np.dot(a, b)
    norm_prod = np.linalg.norm(a) * np.linalg.norm(b)
    return dot_prod / norm_prod
