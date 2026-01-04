import numpy as np

def calculate_information_metrics():
    # --- 準備數據 ---
    # P: 真實分佈 (例如：這張照片真的是貓的機率)
    P = np.array([0.7, 0.2, 0.1]) 
    
    # Q: 預測分佈 (例如：模型預測這張照片是貓的機率)
    Q = np.array([0.6, 0.3, 0.1])
    
    # 為了避免 log(0) 發生錯誤，我們加上一個極小值 epsilon
    epsilon = 1e-10

    # --- 1. 熵 (Entropy) ---
    # 公式: H(P) = - Σ p(x) * log(p(x))
    entropy = -np.sum(P * np.log2(P + epsilon))

    # --- 2. 交叉熵 (Cross-Entropy) ---
    # 公式: H(P, Q) = - Σ p(x) * log(q(x))
    # 在機器學習中，這就是 Loss Function (損失函數)
    cross_entropy = -np.sum(P * np.log2(Q + epsilon))

    # --- 3. KL 散度 (KL Divergence) ---
    # 公式: D_KL(P||Q) = Σ p(x) * log(p(x) / q(x))
    # 也可以寫成: 交叉熵 - 熵
    kl_divergence = np.sum(P * np.log2((P / (Q + epsilon)) + epsilon))

    # --- 4. 互資訊 (Mutual Information) ---
    # 這裡需要一個聯合機率分佈矩陣 P(X,Y)
    # 假設 X 和 Y 的聯合機率如下 (Rows=X, Cols=Y)
    P_xy = np.array([[0.1, 0.1], 
                     [0.0, 0.8]]) 
    
    # 計算邊緣機率 P(x) 和 P(y)
    P_x = np.sum(P_xy, axis=1) # Row sum -> [0.2, 0.8]
    P_y = np.sum(P_xy, axis=0) # Col sum -> [0.1, 0.9]
    
    # 公式: I(X;Y) = ΣΣ p(x,y) * log( p(x,y) / (p(x)p(y)) )
    mi = 0
    for i in range(len(P_x)):
        for j in range(len(P_y)):
            if P_xy[i, j] > 0: # 只計算非零項
                mi += P_xy[i, j] * np.log2(P_xy[i, j] / (P_x[i] * P_y[j]))

    return entropy, cross_entropy, kl_divergence, mi

# 執行並輸出
res_entropy, res_ce, res_kl, res_mi = calculate_information_metrics()

print(f"1. 熵 (Entropy)         : {res_entropy:.4f} bits")
print(f"2. 交叉熵 (Cross-Entropy): {res_ce:.4f} bits")
print(f"3. KL 散度 (KL Divergence): {res_kl:.4f} bits")
print(f"4. 互資訊 (Mutual Info)  : {res_mi:.4f} bits")
print("-" * 30)
print(f"驗證: 交叉熵({res_ce:.4f}) ≈ 熵({res_entropy:.4f}) + KL散度({res_kl:.4f})")
print(f"加總結果: {res_entropy + res_kl:.4f}")