"""SVD 模块 — 奇异值分解及其应用"""

from .decompose import (
    svd_full,
    svd_economy,
    singular_values,
    svd_rank,
)
from .pseudo_inverse import (
    pseudo_inverse,
    solve_via_svd,
)
from .approximation import condition_number
