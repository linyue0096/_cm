import numpy as np

# 設定顯示精度
np.set_printoptions(precision=4, suppress=True)

def svd_from_eigen(A):
    """
    使用特徵值分解 (Eigendecomposition) 來實作 SVD
    回傳: U, Sigma_diag, Vt
    """
    m, n = A.shape
    
    # ---------------------------------------------------------
    # 步驟 1: 計算 A^T A (這是一個 n x n 的對稱矩陣)
    # ---------------------------------------------------------
    ATA = A.T @ A
    
    # ---------------------------------------------------------
    # 步驟 2: 對 A^T A 進行特徵值分解
    # 這裡得到的 eigenvectors 就是 SVD 中的 V
    # ---------------------------------------------------------
    eigenvalues, eigenvectors = np.linalg.eig(ATA)
    
    # ---------------------------------------------------------
    # 步驟 3: 排序 (SVD 要求奇異值從大到小排列)
    # ---------------------------------------------------------
    # argsort 預設是小到大，所以我們要反轉 [::-1]
    sorted_indices = np.argsort(eigenvalues)[::-1]
    
    eigenvalues = eigenvalues[sorted_indices]
    V = eigenvectors[:, sorted_indices] # 重新排列特徵向量
    
    # ---------------------------------------------------------
    # 步驟 4: 計算奇異值 Sigma (特徵值的平方根)
    # ---------------------------------------------------------
    # 過濾掉極小的負數 (數值誤差導致)
    singular_values = np.sqrt(np.abs(eigenvalues))
    
    # ---------------------------------------------------------
    # 步驟 5: 推導 U (左奇異向量)
    # 關鍵公式: A * v_i = sigma_i * u_i  =>  u_i = (A * v_i) / sigma_i
    # ---------------------------------------------------------
    U = np.zeros((m, m))
    
    # 我們只處理非零的奇異值
    rank = np.sum(singular_values > 1e-10)
    
    for i in range(rank):
        sigma = singular_values[i]
        v = V[:, i]  # 第 i 個右奇異向量
        
        # 計算 u
        u = (A @ v) / sigma
        U[:, i] = u
        
    # 如果 m > n (矩陣是瘦長的)，U 剩下的欄位需要填補正交向量 (Gram-Schmidt)
    # 但為了簡化 demo，這裡我們主要關注前 r 個主要成分
    
    # ---------------------------------------------------------
    # 步驟 6: 構建 Sigma 矩陣 (為了矩陣相乘驗證)
    # ---------------------------------------------------------
    Sigma_mat = np.zeros((m, n))
    # 填入對角線
    min_dim = min(m, n)
    Sigma_mat[:min_dim, :min_dim] = np.diag(singular_values[:min_dim])
    
    return U, singular_values, V.T, Sigma_mat

# ==========================================
# 測試區
# ==========================================
# 1. 建立一個長方形矩陣 (4x3)，證明這不只適用於方陣
np.random.seed(42)
A = np.random.rand(4, 3)

print(f"原始矩陣 A (4x3):\n{A}\n")

# 2. 執行我們手寫的 SVD
U_custom, s_custom, Vt_custom, Sigma_mat_custom = svd_from_eigen(A)

print("--- 手寫 SVD 結果 ---")
print(f"奇異值 (Sigma):\n{s_custom}")
# 這裡只印出前幾行避免版面太亂
print(f"V^T (前3列):\n{Vt_custom[:, :3]}\n") 

# 3. 驗證還原
A_reconstructed = U_custom @ Sigma_mat_custom @ Vt_custom

# 計算誤差
error = np.linalg.norm(A - A_reconstructed)
print(f"還原矩陣誤差: {error:.2e}")

if np.allclose(A, A_reconstructed):
    print("✅ 成功！利用特徵值分解完成了 SVD。")
else:
    print("❌ 還原失敗。")

print("-" * 30)

# 4. 對照組：NumPy 內建 SVD
U_np, s_np, Vt_np = np.linalg.svd(A)
print("--- NumPy 內建 SVD 對照 ---")
print(f"奇異值 (Sigma):\n{s_np}")

# 比較奇異值是否一致
if np.allclose(s_custom[:3], s_np[:3]): # 只比對有效的部分
    print("✅ 奇異值計算與 NumPy 一致！")