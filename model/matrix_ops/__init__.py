"""矩阵运算模块 — 基础矩阵操作与线性代数"""

from .basic import (
    matrix_multiply,
    matrix_add,
    matrix_transpose,
    matrix_trace,
    matrix_norm,
    elementwise_multiply,
)
from .solve import (
    linear_solve,
    matrix_inverse,
    matrix_det,
    least_squares,
    solve_triangular,
)
