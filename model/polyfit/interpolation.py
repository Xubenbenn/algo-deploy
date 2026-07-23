"""插值 — 基于 scipy 封装"""

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import interpolate
from typing import Callable

def cubic_spline(
    x: ArrayLike, y: ArrayLike, kind: str = "cubic"
) -> Callable[[ArrayLike], NDArray]:
    """三次样条插值 (C² 连续)

    Args:
        x: 插值节点 (严格递增)
        y: 节点值
        kind: 'cubic' (三次) / 'linear' (线性) / 'quadratic' (二次)

    Returns:
        样条插值函数 f(xx)
    """
    x_arr = np.asarray(x, dtype=np.float64)
    y_arr = np.asarray(y, dtype=np.float64)
    spline = interpolate.interp1d(
        x_arr, y_arr, kind=kind, fill_value="extrapolate"
    )

    def interp_func(xx: ArrayLike) -> NDArray:
        return spline(np.asarray(xx))

    return interp_func
