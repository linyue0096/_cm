import numpy as np

def cross_entropy(P, Q):
    # 避免 log(0) 錯誤
    epsilon = 1e-15
    return -np.sum(P * np.log2(Q + epsilon))

def verify_inequality():
    # 1. 設定真實分佈 P
    P = np.array([0.6, 0.1, 0.3])
    
    # 計算 P 自己的熵 (H(P) 或 H(P,P))
    # 這是理論上的最小值
    self_entropy = cross_entropy(P, P)
    
    print(f"真實分佈 P: {P}")
    print(f"基準值 H(P, P) [熵]: {self_entropy:.6f} bits")
    print("-" * 40)
    print(f"{'測試':<5} | {'預測分佈 Q':<25} | {'H(P, Q)':<10} | {'結果 (是否 H(P,Q) > H(P,P)?)'}")
    print("-" * 75)

    # 2. 測試 5 個隨機生成的 Q (Q != P)
    np.random.seed(42) # 固定隨機，方便重現
    
    for i in range(5):
        # 隨機生成 3 個數並歸一化 (讓總和為 1)
        random_vec = np.random.rand(3)
        Q = random_vec / np.sum(random_vec)
        
        # 計算交叉熵
        ce_val = cross_entropy(P, Q)
        
        # 驗證是否大於熵
        is_greater = ce_val > self_entropy
        
        # 格式化輸出
        q_str = str(np.round(Q, 2))
        print(f"#{i+1:<4} | {q_str:<25} | {ce_val:.6f}   | {is_greater}")

    print("-" * 75)
    
    # 3. 結論驗證
    if self_entropy <= min([cross_entropy(P, np.random.dirichlet(np.ones(3))) for _ in range(100)]):
        print("\n結論：驗證成功！")
        print("H(P, Q) (交叉熵) 永遠大於等於 H(P, P) (熵)。")
        print("也就是說：用錯誤的 Q 去預測 P，付出的代價(Bits)一定比用 P 自己預測要高。")
    else:
        print("數學崩壞了，這不可能發生。")

# 執行驗證
verify_inequality()