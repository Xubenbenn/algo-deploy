"""多项式拟合模块 — 拟合、插值与求根"""

from .fitting import (
    polyfit_ls,
    polyval,
    poly_residual,
    r2_score,
)
from .interpolation import cubic_spline
from .roots import poly_roots
