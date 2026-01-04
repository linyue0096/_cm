import math
import cmath
from typing import List, Complex

def dft(x: List[float]) -> List[Complex]:
    """
    離散傅立葉轉換 (DFT) - 優化版
    數學式: X[k] = Σ x[n] * exp(-j * 2π * k * n / N)
    """
    N = len(x)
    X = []
    
    # 預先計算常數係數，減少迴圈內的除法運算
    # -1j 代表數學上的 -i
    coefficient = -2j * math.pi / N
    
    for k in range(N):
        # 使用 Generator Expression 配合 sum()
        # 這行程式碼幾乎完全對應數學公式的 Σ
        value = sum(x[n] * cmath.exp(coefficient * k * n) for n in range(N))
        X.append(value)
        
    return X

def idft(X: List[Complex]) -> List[float]:
    """
    逆離散傅立葉轉換 (IDFT) - 優化版
    數學式: x[n] = (1/N) * Σ X[k] * exp(j * 2π * k * n / N)
    """
    N = len(X)
    x = []
    
    # 逆轉換係數 (注意這裡是正的 1j)
    coefficient = 2j * math.pi / N
    
    for n in range(N):
        # 同樣使用 sum() 進行累加
        value = sum(X[k] * cmath.exp(coefficient * k * n) for k in range(N))
        
        # 最後除以 N (正規化)，並只取實部 (理論上虛部應為0)
        # 這裡直接轉回 real 是為了方便後續處理，嚴謹數學上應保留 complex
        x.append(value.real / N)
        
    return x

# --- 優化後的驗證與測試工具 ---

def generate_signal(N: int) -> List[float]:
    """產生一個測試用的混合波形"""
    # f(n) = 1.0*sin(2πn/N) + 0.5*cos(4πn/N)
    return [
        1.0 * math.sin(2 * math.pi * n / N) + 
        0.5 * math.cos(4 * math.pi * n / N) 
        for n in range(N)
    ]

def print_comparison(original, reconstructed):
    """美化輸出比較結果"""
    print(f"{'Index':<5} | {'Original':<10} | {'Reconstructed':<15} | {'Status'}")
    print("-" * 50)
    
    all_passed = True
    for i, (orig, recon) in enumerate(zip(original, reconstructed)):
        # 使用 math.isclose 進行專業的浮點數比對
        is_match = math.isclose(orig, recon, abs_tol=1e-9)
        status = "✅ OK" if is_match else "❌ Fail"
        if not is_match: all_passed = False
        
        print(f"{i:<5} | {orig:<10.4f} | {recon:<15.4f} | {status}")
    
    print("-" * 50)
    if all_passed:
        print("🎉 完美驗證：轉換再逆轉換後數值一致！")
    else:
        print("⚠️ 驗證警告：部分數值存在誤差。")

if __name__ == "__main__":
    # 1. 準備數據
    N = 8
    x = generate_signal(N)
    
    # 2. 執行轉換
    X = dft(x)     # 時域 -> 頻域
    x_recon = idft(X) # 頻域 -> 時域
    
    # 3. 驗證結果
    print_comparison(x, x_recon)
    
    # 額外展示：觀察頻域能量 (Magnitude)
    print("\n--- 頻域能量分析 (Magnitude) ---")
    magnitudes = [abs(val) for val in X]
    print([round(m, 2) for m in magnitudes])
    # 預期：在 index 1 (sin波) 和 index 2 (cos波的一半頻率?) 會有數值