import cmath
import numpy as np

def log2(x):
    return cmath.log(x,2)

def entropy(a):
    r=0
    for i in range(len(a)):
        r += a[i]*log2(1/a[i])
    return r
