# 1. 基礎工具：建立子矩陣 (為了算行列式和餘因子)
def get_minor_matrix(matrix, remove_row, remove_col):
    """
    刪除指定的 row 和 col，返回剩下的子矩陣
    """
    new_matrix = []
    for i, row in enumerate(matrix):
        if i == remove_row:
            continue
        # 拼接：跳過指定的 col
        new_row = row[:remove_col] + row[remove_col+1:]
        new_matrix.append(new_row)
    return new_matrix

# 2. 核心：遞迴行列式 (沿用上一段的邏輯，但為了通用性稍作封裝)
def determinant(matrix):
    n = len(matrix)
    if n == 1: return matrix[0][0]
    if n == 2: return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    
    det = 0
    for col in range(n):
        sign = (-1) ** col
        sub_matrix = get_minor_matrix(matrix, 0, col)
        det += sign * matrix[0][col] * determinant(sub_matrix)
    return det

# 3. 運算：矩陣乘法 (Matrix Multiplication)
def matrix_multiply(A, B):
    """
    C = A * B
    """
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("維度不匹配：A 的行數必須等於 B 的列數")
    
    # 初始化結果矩陣 (全 0)
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

# 4. 運算：轉置 (Transpose)
def transpose(matrix):
    """
    行變列，列變行
    """
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[j][i] for j in range(rows)] for i in range(cols)]

# 5. 大魔王：反矩陣 (Inverse) - 使用伴隨矩陣法
def inverse(matrix):
    det = determinant(matrix)
    if det == 0:
        raise ValueError("行列式為 0，此矩陣不可逆 (Singular)！")
    
    n = len(matrix)
    
    # 如果是 1x1 矩陣，反矩陣就是倒數
    if n == 1:
        return [[1/det]]
    
    # A. 計算餘因子矩陣 (Matrix of Cofactors)
    cofactors = []
    for r in range(n):
        cofactor_row = []
        for c in range(n):
            # 取得 minor (刪除 r列 c行)
            minor = get_minor_matrix(matrix, r, c)
            # 計算 minor 的行列式
            minor_det = determinant(minor)
            # 加上正負號 (-1)^(r+c)
            sign = (-1) ** (r + c)
            cofactor_row.append(sign * minor_det)
        cofactors.append(cofactor_row)
    
    # B. 計算伴隨矩陣 (Adjugate) -> 就是餘因子矩陣的「轉置」
    adjugate = transpose(cofactors)
    
    # C. 除以行列式 (1/det * adj)
    inv_matrix = []
    for row in adjugate:
        new_row = [elem / det for elem in row]
        inv_matrix.append(new_row)
        
    return inv_matrix

# --- 測試區 ---
if __name__ == "__main__":
    A = [
        [4, 7],
        [2, 6]
    ]
    
    B = [
        [1, 2, 3],
        [0, 1, 4],
        [5, 6, 0]
    ]

    print(f"原本的矩陣 A: {A}")
    print(f"A 的轉置: {transpose(A)}")
    print("-" * 20)
    
    try:
        inv_B = inverse(B)
        print("矩陣 B 的反矩陣 (Inverse):")
        for row in inv_B:
            # 為了美觀，取小數點後 2 位
            print([round(x, 2) for x in row])
            
        print("-" * 20)
        # 驗證：B * B_inv 應該要接近單位矩陣 I
        identity = matrix_multiply(B, inv_B)
        print("驗證 (B * B_inverse)，應該要是單位矩陣：")
        for row in identity:
            print([round(x, 1) for x in row]) # 使用 round 消除浮點數誤差
            
    except ValueError as e:
        print(e)