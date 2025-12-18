import math
N = 10000
p = 0.5
log_p = math.log(p)
log_probability = N * log_p

print(f"--- 連續投擲 {N} 次公平銅板 (p={p}) ---")
print(f"連續 {N} 次全部正面的機率 (P) 的對數值 log(P) 為：")
print(f"log(P) = N * log(p) = {N} * ({log_p})")
print(f"log(P) = {log_probability}")

actual_probability = math.exp(log_probability)

print("-" * 30)
print("【機率 P 的數值分析 (額外資訊)】")
print(f"P 的近似值 (使用 e^log(P)) 為：{actual_probability:e}")