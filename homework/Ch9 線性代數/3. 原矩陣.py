import numpy as np
from scipy.linalg import lu

# 設定顯示精度，避免看到像 0.000000001 這種數字
np.set_printoptions(precision=4, suppress=True)

def verify_matrix_equality(A, A_reconstructed, name):
    """
    輔助函數：比較兩個矩陣是否相等 (允許浮點數極小誤差)
    """
    # np.allclose 檢查兩個陣列是否在誤差範圍內相等
    is_equal = np.allclose(A, A_reconstructed)
    
    # 計算誤差 (Frobenius Norm)
    error = np.linalg.norm(A - A_reconstructed)
    
    print(f"--- 驗證 {name} ---")
    if is_equal:
        print(f"✅ 成功還原！(誤差: {error:.2e})")
    else:
        print(f"❌ 還原失敗。(誤差: {error:.2e})")
    print("-" * 30)

# 1. 準備一個 3x3 的隨機矩陣 (方陣才能做特徵值分解)
np.random.seed(42) # 固定種子，保證每次跑結果一樣
A = np.random.rand(3, 3) * 10
print(f"原始矩陣 A:\n{A}\n")
print("=" * 40 + "\n")

# ==========================================
# 2. 驗證 LU 分解 (A = P * L * U)
# ==========================================
# SciPy 的 lu 函數會回傳三個矩陣：P(排列), L(下三角), U(上三角)
P, L, U = lu(A)

print("LU 分解結果:")
print(f"P (排列矩陣):\n{P}")
print(f"L (下三角):\n{L}")
print(f"U (上三角):\n{U}\n")

# 驗證：相乘回去
A_lu = P @ L @ U
verify_matrix_equality(A, A_lu, "LU 分解")


# ==========================================
# 3. 驗證 特徵值分解 (A = V * D * V_inv)
# ==========================================
# eigenvalues: 特徵值陣列
# eigenvectors: 特徵向量矩陣 (V)
eigenvalues, V = np.linalg.eig(A)

# 建立對角矩陣 D
D = np.diag(eigenvalues)

# 計算 V 的反矩陣
V_inv = np.linalg.inv(V)

print("特徵值分解結果:")
print(f"特徵值 (Lambda):\n{eigenvalues}")
print(f"特徵向量矩陣 (V):\n{V}\n")

# 驗證：相乘回去 V * D * V^(-1)
# 注意：如果是實數矩陣但有複數特徵值，這裡會顯示複數，但虛部通常極小
A_eig = V @ D @ V_inv
verify_matrix_equality(A, A_eig, "特徵值分解")


# ==========================================
# 4. 驗證 SVD 分解 (A = U * Sigma * Vt)
# ==========================================
# U: 左奇異向量
# s: 奇異值 (一維陣列)
# Vt: 右奇異向量的轉置 (V^T)
U, s, Vt = np.linalg.svd(A)

# 將一維的奇異值 s 轉成對角矩陣 Sigma
Sigma = np.diag(s)

print("SVD 分解結果:")
print(f"U (左奇異向量):\n{U}")
print(f"Sigma (奇異值):\n{Sigma}")
print(f"Vt (右奇異向量轉置):\n{Vt}\n")

# 驗證：相乘回去 U * Sigma * Vt
A_svd = U @ Sigma @ Vt
verify_matrix_equality(A, A_svd, "SVD 分解")