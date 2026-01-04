import decimal
import math

def calculate_extreme_probability():
    # 1. 設定計算精確度
    # 0.5^10000 大約是 10^-3010，所以我們至少需要 3020 位的精確度才能看到非零的數字
    decimal.getcontext().prec = 3050 

    # 2. 定義變數 (使用字串 '0.5' 初始化以確保精確度)
    p = decimal.Decimal('0.5')
    n = 10000

    # 3. 計算機率
    probability = p ** n

    return probability

# 執行計算
result = calculate_extreme_probability()

# 4. 輸出結果
print("計算結果 (科學記號):")
# 格式化輸出，保留前 5 位有效數字
print(f"{result:.5e}")

print("-" * 30)

# 額外補充：使用對數驗證數量級
# log10(0.5^10000) = 10000 * log10(0.5)
log_val = 10000 * math.log10(0.5)
print(f"對數驗證 (10的幾次方): 10^{log_val:.2f}")