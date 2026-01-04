def lu_decomposition(matrix):
    """
    實作 Doolittle 演算法進行 LU 分解
    A = L * U
    L: Lower triangular matrix (對角線為 1)
    U: Upper triangular matrix
    """
    n = len(matrix)
    
    # 初始化 L 為單位矩陣 (對角線為 1)，U 為全 0 矩陣
    # 注意：這裡使用 list comprehension 建立二維陣列
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    U = [[0.0 for j in range(n)] for i in range(n)]
    
    for i in range(n):
        # 1. 計算 U 的第 i 列 (Upper Triangular)
        for k in range(i, n):
            # Summation part: L[i][0]*U[0][k] + ... + L[i][i-1]*U[i-1][k]
            sum_val = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = matrix[i][k] - sum_val
            
        # 2. 計算 L 的第 i 行 (Lower Triangular)
        for k in range(i + 1, n):
            # Summation part: L[k][0]*U[0][i] + ... + L[k][i-1]*U[i-1][i]
            sum_val = sum(L[k][j] * U[j][i] for j in range(i))
            
            # 關鍵檢查：如果 U[i][i] 是 0，會發生除以零錯誤 (Pivot 為 0)
            if U[i][i] == 0:
                raise ValueError("Pivot is zero. 需要使用 PA=LU 分解 (排列矩陣) 才能處理此矩陣。")
                
            L[k][i] = (matrix[k][i] - sum_val) / U[i][i]
            
    return L, U

def determinant_via_lu(matrix):
    """
    透過 LU 分解快速計算行列式
    det(A) = det(L) * det(U) = 1 * product(diagonal of U)
    """
    try:
        L, U = lu_decomposition(matrix)
        
        n = len(U)
        det = 1.0
        for i in range(n):
            det *= U[i][i]  # 累乘 U 的對角線
            
        return det, L, U
    
    except ValueError as e:
        return 0.0, [], [] # Pivot 為 0 代表矩陣奇異，行列式通常為 0 (或需交換列)

def print_matrix(name, M):
    print(f"--- {name} ---")
    for row in M:
        # 格式化輸出，保留 2 位小數
        print([round(x, 2) for x in row])
    print()

# --- 測試區 ---
if __name__ == "__main__":
    #這是一個 3x3 矩陣
    # | 2  -1  -2 |
    # | -4  6   3 |
    # | -4 -2   8 |
    A = [
        [2, -1, -2],
        [-4, 6, 3],
        [-4, -2, 8]
    ]

    print_matrix("原始矩陣 A", A)
    
    det_val, L_matrix, U_matrix = determinant_via_lu(A)
    
    print_matrix("下三角矩陣 L (對角線為1)", L_matrix)
    print_matrix("上三角矩陣 U (對角線乘積即為 Det)", U_matrix)
    
    print("-" * 30)
    print(f"計算出的行列式值: {det_val}")
    
    # 驗證計算
    # U 的對角線應該是: 2, 4, 3.5 (視實作而定)
    # 2 * 4 * 3.5 = 28 (假設值)

    # 簡單驗證：
    # 2*(48 - (-6)) - (-1)*(-32 - (-12)) + (-2)*(8 - (-24))
    # = 2(54) + 1(-20) - 2(32)
    # = 108 - 20 - 64 = 24