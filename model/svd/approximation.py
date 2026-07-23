"""低秩逼近与矩阵分析 — 基于 SVD"""

import numpy as np
from numpy.typing import ArrayLike
from scipy import linalg

def condition_number(a: ArrayLike) -> float:
    """矩阵条件数 (2-范数): κ₂(A) = σ_max / σ_min

    Args:
        a: 输入矩阵

    Returns:
        条件数, ∞ 表示奇异 (不可逆)
    """
    s = linalg.svdvals(np.asarray(a, dtype=np.float64))
    if len(s) == 0 or s[-1] == 0:
        return float("inf")
    return float(s[0] / s[-1])
