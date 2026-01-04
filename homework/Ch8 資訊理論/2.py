import math

def calculate_log_probability_method():
    n = 10000
    p = 0.5

    log10_val = n * math.log10(p)
    

    ln_val = n * math.log(p)
    
    return log10_val, ln_val

log10_result, ln_result = calculate_log_probability_method()

print(f"投擲次數: 10000 次")
print(f"單次機率: 0.5")
print("-" * 30)
print(f"Log10 結果 (以 10 為底): {log10_result:.4f}")
print(f"Ln 結果    (以 e 為底) : {ln_result:.4f}")

print("-" * 30)
print("結果解讀：")
print(f"這代表原始機率約為 10 的 {log10_result:.4f} 次方")