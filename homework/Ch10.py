import cmath
import math
import numpy as np # 僅用於生成測試信號和方便結果顯示/繪圖

# --- 1. 正向離散傅立葉轉換 (DFT) ---

def dft_pure_math(x):
    N = len(x)
    X = []
    
    # 遍歷所有頻率分量 k (從 0 到 N-1)
    for k in range(N):
        sum_of_terms = 0 + 0j  # 初始化為複數 0
        
        # 遍歷所有時間樣本 n (從 0 到 N-1) 進行求和
        for n in range(N):
            # 計算旋轉因子 exp(-j * 2*pi*k*n / N)
            angle = -2j * math.pi * k * n / N 
            exponential_term = cmath.exp(angle)
            
            # 累加 x[n] 與旋轉因子的乘積
            sum_of_terms += x[n] * exponential_term
            
        X.append(sum_of_terms)
        
    return X

# --- 2. 逆向離散傅立葉轉換 (IDFT) ---

def idft_pure_math(X):
    N = len(X)
    x = []
    
    # 遍歷所有時間樣本 n (從 0 到 N-1)
    for n in range(N):
        sum_of_terms = 0 + 0j  # 初始化為複數 0
        
        # 遍歷所有頻率分量 k (從 0 到 N-1) 進行求和
        for k in range(N):
            # 計算旋轉因子 exp(j * 2*pi*k*n / N) - 注意：指數是正的
            angle = 2j * math.pi * k * n / N 
            exponential_term = cmath.exp(angle)
            
            # 累加 X[k] 與旋轉因子的乘積
            sum_of_terms += X[k] * exponential_term
        
        # 加上歸一化因子 1/N
        x_n = (1 / N) * sum_of_terms
        x.append(x_n)
        
    return x

