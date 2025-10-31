import numpy as np
import math

def root(c):
    TOL=1e-10
    n = len(c) - 1 
    if n < 0:
        return "輸入列表為空,不是多項式"
    if n == 0: 
        c0 = c[0] 
        if abs(c0) > TOL:
            return"no roots"
        else:
            return "所有x都為根"
    elif n ==1:
        c1 = c[0]
        c0 = c[1]

        if abs(c1) < TOL:
            return "最高次數接近0, 無法除以0"
        return[-c0 / c1]
    else:
        c_n = c[0]
        if abs(c_n) < TOL:
            return f"最高係數接近0, 實際次數為 n={n-1}, 重新輸入係數"

    c_norm=[ci/c_n for ci in c]
    print(f"標準化後的係數: {c_norm}")

    companion = np.zeros((n, n), dtype=complex)
    companion[1:, :-1] = np.eye(n-1)
    companion[0, :] = -np.array(c_norm[1:])

    roots=np.linalg.eigvals(companion)
    return roots

coeffs = [-8, 14, -7, 1]
print(root(coeffs))