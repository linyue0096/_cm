import numpy as np
from collections import Counter

def solve_ode_general(coefficients):
    """
    求解常係數齊次常微分方程 (ODE)。
    輸入: coefficients (list) - 從最高階到最低階的係數，例如 y'' - 3y' + 2y = 0 為 [1, -3, 2]
    輸出: 通解的字串格式 y(x) = ...
    """
    
    # 1. 求解特徵方程的根 (使用 numpy 的數值解法)
    roots = np.roots(coefficients)
    
    # 2. 根的清洗與標準化 (關鍵步驟)
    # numpy 計算出的根會有浮點數誤差 (例如 2 可能變成 1.9999999999 或 2 + 1e-15j)
    # 我們需要四捨五入到特定小數位數，以便正確分類重根和實根
    cleaned_roots = []
    tolerance = 5  # 小數點後保留位數，用於分組判斷
    
    for r in roots:
        # 取實部和虛部，並四捨五入
        real_part = round(r.real, tolerance)
        imag_part = round(r.imag, tolerance)
        
        # 如果虛部極小，視為 0 (處理實數根帶有極小虛部雜訊的情況)
        if abs(imag_part) == 0.0:
            cleaned_roots.append(complex(real_part, 0))
        else:
            cleaned_roots.append(complex(real_part, imag_part))

    # 3. 統計根的重數 (Multiplicity)
    # Counter 會將清洗後數值相同的根歸類在一起
    root_counts = Counter(cleaned_roots)
    
    # 4. 生成通解字串
    terms = []
    c_index = 1 # 常數編號 C_1, C_2...
    
    # 為了輸出順序穩定，先處理實根，再處理複數根，並按數值排序
    # 排序鍵值: (是否為複數, 實部大小, 虛部大小)
    sorted_unique_roots = sorted(root_counts.keys(), key=lambda x: (abs(x.imag) > 0, x.real, x.imag))
    
    processed_conjugates = set() # 用於追蹤已處理過的共軛複數對
    
    for r in sorted_unique_roots:
        m = root_counts[r] # 重根數
        
        # --- 情況 A: 實數根 ---
        if r.imag == 0:
            alpha = r.real
            # 格式化指數部分 (處理 e^0 = 1 和 e^1x)
            exp_str = f"e^({alpha}x)"
            if alpha == 0: exp_str = ""
            elif alpha == 1: exp_str = "e^(x)"
            
            for k in range(m):
                # 處理 x 的冪次 (x^0, x^1, x^2...)
                x_str = ""
                if k == 1: x_str = "x"
                elif k > 1: x_str = f"x^{k}"
                
                # 組合: C_i * x^k * e^(rx)
                term = f"C_{c_index}{x_str}{exp_str}"
                # 如果兩者都空 (例如 C_1 * 1 * 1)，補回常數
                if term == f"C_{c_index}": term = f"C_{c_index}"
                
                terms.append(term)
                c_index += 1

        # --- 情況 B: 複數根 (alpha +/- beta i) ---
        else:
            # 如果這個根的共軛已經處理過，則跳過 (避免重複輸出)
            if r in processed_conjugates:
                continue
            
            # 標記共軛對
            processed_conjugates.add(r)
            processed_conjugates.add(r.conjugate())
            
            alpha = r.real
            beta = abs(r.imag) # 取正值放入 sin/cos
            
            # 格式化部分
            exp_str = f"e^({alpha}x)"
            if alpha == 0: exp_str = ""
            elif alpha == 1: exp_str = "e^(x)"
            
            cos_str = f"cos({beta}x)"
            sin_str = f"sin({beta}x)"
            
            for k in range(m):
                x_str = ""
                if k == 1: x_str = "x"
                elif k > 1: x_str = f"x^{k}"
                
                # C_a * x^k * e^(ax)cos(bx)
                term1 = f"C_{c_index}{x_str}{exp_str}{cos_str}"
                c_index += 1
                
                # C_b * x^k * e^(ax)sin(bx)
                term2 = f"C_{c_index}{x_str}{exp_str}{sin_str}"
                c_index += 1
                
                terms.append(term1)
                terms.append(term2)
    
    # 5. 組合最終結果
    result = " + ".join(terms)
    # 美化輸出：處理 "+ -" 變成 "- " (若 alpha 為負數時可能發生)
    result = result.replace("+ -", "- ")
    return f"y(x) = {result}"

# --- 以下是測試主程式 (與您提供的一致) ---
if __name__ == "__main__":
    # 範例測試 (1): 實數單根
    print("--- 實數單根範例 ---")
    coeffs1 = [1, -3, 2]
    print(f"方程係數: {coeffs1}")
    print(solve_ode_general(coeffs1))

    # 範例測試 (2): 實數重根
    print("\n--- 實數重根範例 ---")
    coeffs2 = [1, -4, 4]
    print(f"方程係數: {coeffs2}")
    print(solve_ode_general(coeffs2))

    # 範例測試 (3): 複數共軛根
    print("\n--- 複數共軛根範例 ---")
    coeffs3 = [1, 0, 4]
    print(f"方程係數: {coeffs3}")
    print(solve_ode_general(coeffs3))

    # 範例測試 (4): 複數重根 (二重)
    print("\n--- 複數重根範例 ---")
    coeffs4 = [1, 0, 2, 0, 1]
    print(f"方程係數: {coeffs4}")
    print(solve_ode_general(coeffs4))

    # 範例測試 (5): 高階重根
    print("\n--- 高階重根範例 ---")
    coeffs5 = [1, -6, 12, -8]
    print(f"方程係數: {coeffs5}")
    print(solve_ode_general(coeffs5))