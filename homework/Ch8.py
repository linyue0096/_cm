import math

p=0.5
n=10000
probability=p**n
print(f"連續投擲10000次全部得到正面的概率:{probability}")
log_probability=n*math.log(p)
print(f"對數概率:{log_probability}")