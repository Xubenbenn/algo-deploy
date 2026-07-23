"""多项式求根、微积分 — 基于 numpy 封装"""

import numpy as np
from numpy.typing import ArrayLike, NDArray

def poly_roots(p: ArrayLike) -> NDArray:
    """求多项式所有根 (包括复数): p[0]·x^n + ... + p[n] = 0

    Args:
        p: 多项式系数 (降幂排列)

    Returns:
        根数组 (可能含复数)
    """
    return np.roots(np.asarray(p, dtype=np.float64))
