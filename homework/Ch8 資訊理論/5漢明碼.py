import numpy as np

class Hamming74:
    def __init__(self):
        # --- 定義矩陣 ---
        
        # 1. 生成矩陣 (Generator Matrix) G [4x7]
        # 用途：將 4 bits 資料 -> 轉換為 7 bits 碼字
        # 格式：I_4 (左邊是單位矩陣) | P (右邊是檢查位產生規則)
        self.G = np.array([
            [1, 0, 0, 0, 1, 1, 0], # d1
            [0, 1, 0, 0, 1, 0, 1], # d2
            [0, 0, 1, 0, 0, 1, 1], # d3
            [0, 0, 0, 1, 1, 1, 1]  # d4
        ])
        
        # 2. 校驗矩陣 (Parity Check Matrix) H [3x7]
        # 用途：用來檢查 7 bits 碼字是否有錯
        # 格式：P^T (P的轉置) | I_3 (單位矩陣)
        self.H = np.array([
            [1, 1, 0, 1, 1, 0, 0], # p1 檢查規則
            [1, 0, 1, 1, 0, 1, 0], # p2 檢查規則
            [0, 1, 1, 1, 0, 0, 1]  # p3 檢查規則
        ])
        
        # 定義校驗子 (Syndrome) 對應的錯誤位置索引
        # 當 H * r^T = [s1, s2, s3] 時，這個二進位值代表哪裡錯了
        # 注意：這裡的 H 排列方式，計算出的 syndrome 轉換成十進位後，
        # 需要查表才能對應到 array index，或者我們調整 H 的欄位順序。
        # 為了程式簡單，我使用查表法 (Syndrome -> Error Index)。
        self.syndrome_map = {
            (0, 0, 0): None, # 沒錯
            (1, 1, 0): 0,    # Index 0 錯 (d1)
            (1, 0, 1): 1,    # Index 1 錯 (d2)
            (0, 1, 1): 2,    # Index 2 錯 (d3)
            (1, 1, 1): 3,    # Index 3 錯 (d4)
            (1, 0, 0): 4,    # Index 4 錯 (p1)
            (0, 1, 0): 5,    # Index 5 錯 (p2)
            (0, 0, 1): 6     # Index 6 錯 (p3)
        }

    def encode(self, data_bits):
        """
        編碼：輸入 4 bits，輸出 7 bits
        公式：c = d * G (模 2 運算)
        """
        d = np.array(data_bits)
        if len(d) != 4:
            raise ValueError("資料必須是 4 個位元")
            
        # 矩陣乘法後取餘數 (Modulo 2)
        codeword = np.dot(d, self.G) % 2
        return codeword

    def decode(self, received_bits):
        """
        解碼：輸入 7 bits，輸出修正後的 4 bits
        公式：s = H * r^T (模 2 運算)
        """
        r = np.array(received_bits)
        
        # 1. 計算校驗子 (Syndrome)
        syndrome = np.dot(self.H, r) % 2
        s_tuple = tuple(syndrome) # 轉成 tuple 方便查表
        
        print(f"  > 接收到的訊號: {r}")
        print(f"  > 計算校驗子 (Syndrome): {s_tuple}")
        
        # 2. 錯誤修正
        error_index = self.syndrome_map.get(s_tuple)
        
        corrected_r = r.copy()
        if error_index is not None:
            print(f"  > [偵測到錯誤] 位置在 Index: {error_index}")
            # 翻轉位元 (0變1, 1變0)
            corrected_r[error_index] = 1 - corrected_r[error_index]
            print(f"  > 修正後的訊號: {corrected_r}")
        else:
            print(f"  > [無錯誤] 傳輸完美。")
            
        # 3. 提取資料位元 (前 4 位是資料)
        # 根據我們 G 矩陣的設計，前 4 位就是原始資料 (Systematic Code)
        decoded_data = corrected_r[:4]
        
        return decoded_data

# --- 主程式測試 ---
hamming = Hamming74()

# 1. 原始資料
original_data = [1, 0, 1, 1] 
print(f"1. 原始資料 (4 bits): {original_data}")

# 2. 編碼
encoded_signal = hamming.encode(original_data)
print(f"2. 編碼結果 (7 bits): {encoded_signal}")
print("-" * 50)

# 3. 模擬傳輸 (正常情況)
print("--- 測試情境 A: 傳輸無錯誤 ---")
decoded_A = hamming.decode(encoded_signal)
print(f"  > 解碼結果: {decoded_A}")
print("-" * 50)

# 4. 模擬傳輸 (發生 1 bit 錯誤)
print("--- 測試情境 B: 傳輸發生 1 bit 錯誤 ---")
noisy_signal = encoded_signal.copy()
error_pos = 2 # 假設 Index 2 (d3) 壞掉了
noisy_signal[error_pos] = 1 - noisy_signal[error_pos] # 故意翻轉

decoded_B = hamming.decode(noisy_signal)
print(f"  > 解碼結果: {decoded_B}")

# 驗證
is_correct = np.array_equal(decoded_B, original_data)
print(f"\n最終驗證: {'成功還原!' if is_correct else '還原失敗'}")