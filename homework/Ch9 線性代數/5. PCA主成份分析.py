import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] # 設定字體為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False # 解決負號 '-' 顯示成方塊的問題

def run_pca_analysis():
    print("=== 1. 數據生成與預處理 ===")
    # 固定種子，確保每次結果一致
    np.random.seed(42)
    
    # 產生 200 筆 2D 數據 (故意製造強烈的相關性)
    # 這裡我們用矩陣乘法把標準常態分佈拉伸、旋轉
    n_samples = 200
    C = np.array([[0.7, 0.7], [-0.3, 0.8]]) # 變換矩陣
    X = np.dot(np.random.randn(n_samples, 2), C.T)
    
    # 中心化 (Centering)
    X_mean = np.mean(X, axis=0)
    X_centered = X - X_mean
    
    print(f"數據形狀: {X.shape}")
    print(f"數據平均值 (應接近 0): {np.round(np.mean(X_centered, axis=0), 4)}")
    print("-" * 30)

    print("=== 2. 手刻 PCA 計算 ===")
    # 步驟 A: 計算協方差矩陣
    cov_matrix = np.cov(X_centered.T)
    
    # 步驟 B: 特徵值分解
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    
    # 步驟 C: 排序 (從大到小)
    # argsort 預設是小到大，所以用 [::-1] 反轉
    sorted_idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_idx]
    eigenvectors = eigenvectors[:, sorted_idx]
    
    # 步驟 D: 投影 (Projection)
    # 將數據轉換到新的主成分座標系
    X_pca = np.dot(X_centered, eigenvectors)
    
    print("計算完成！")
    print(f"主成分方向 (特徵向量):\n{eigenvectors}")
    print(f"解釋變異量 (特徵值): {eigenvalues}")
    print("-" * 30)

    print("=== 3. 自動驗算 (Verification) ===")
    
    # 驗算邏輯 1: 
    # PCA 的目的就是要讓新特徵之間「零相關」。
    # 所以 X_pca 的協方差矩陣，應該要是「對角矩陣」(非對角線元素為 0)。
    new_cov = np.cov(X_pca.T)
    
    # 提取非對角線元素 (Off-diagonal elements)
    off_diagonal = new_cov - np.diag(np.diagonal(new_cov))
    
    # 檢查是否極接近 0
    if np.allclose(off_diagonal, 0, atol=1e-10):
        print("✅ 驗算成功 1：新特徵之間已完全解耦 (協方差為對角矩陣)。")
    else:
        print("❌ 驗算失敗 1：新特徵之間仍有相關性。")
        print(off_diagonal)

    # 驗算邏輯 2:
    # 總變異量應該守恆 (原本的變異量總和 = 投影後的變異量總和)
    original_variance = np.trace(cov_matrix) # 跡 (Trace)
    new_variance = np.sum(eigenvalues)
    
    if np.isclose(original_variance, new_variance):
        print(f"✅ 驗算成功 2：能量守恆 (總變異量: {original_variance:.4f})。")
    else:
        print("❌ 驗算失敗 2：變異量不守恆。")
        
    print("-" * 30)

    # === 4. 畫圖視覺化 ===
    try:
        plot_results(X, X_mean, X_pca, eigenvectors, eigenvalues)
    except Exception as e:
        print(f"畫圖時發生錯誤: {e}")
        print("可能是 matplotlib 環境問題，但上方的數學驗算已確認 PCA 正確。")

def plot_results(X, X_mean, X_pca, eigenvectors, eigenvalues):
    plt.figure(figsize=(12, 5))

    # --- 左圖：原始數據 + 主成分軸 ---
    plt.subplot(1, 2, 1)
    plt.scatter(X[:, 0], X[:, 1], alpha=0.4, label='Data')
    
    # 畫出兩個主成分箭頭
    for length, vector, color, name in zip(eigenvalues, eigenvectors.T, ['r', 'b'], ['PC1', 'PC2']):
        # 箭頭長度用特徵值(標準差)放大，方便觀看
        v = vector * 3 * np.sqrt(length)
        plt.arrow(X_mean[0], X_mean[1], v[0], v[1], 
                  head_width=0.05, head_length=0.1, fc=color, ec=color, linewidth=2, label=name)
    
    plt.axis('equal')
    plt.grid(True)
    plt.title('原始數據與主成分軸 (Original Data)')
    plt.legend()

    # --- 右圖：投影後的數據 ---
    plt.subplot(1, 2, 2)
    plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.4, c='orange')
    plt.xlabel('PC1 (變異最大)')
    plt.ylabel('PC2 (變異次之)')
    plt.title('PCA 投影結果 (Projected Data)')
    plt.axis('equal')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# ==========================================
# 這一行最重要！確保程式會被執行
# ==========================================
if __name__ == "__main__":
    run_pca_analysis()