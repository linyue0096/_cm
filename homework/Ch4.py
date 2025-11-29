import numpy as np

def root(c):
    TOL = 1e-10
    
    c = np.array(c, dtype=float)
    if c.size == 0:
        return "輸入列表為空,不是多項式"
    
   
    while len(c) > 0 and abs(c[-1]) < TOL:
        c = c[:-1]
    
    if len(c) == 0:
        return "所有係數接近0，所有x都為根"
    
    n = len(c) - 1  
    
    if n == 0:
        return "no roots"
    
    if n == 1:
        c0, c1 = c[0], c[1]
        if abs(c1) < TOL:
            return "最高次係數接近0，無法求解"
        return [-c0 / c1]
    
    leading_coeff = c[-1]
    if abs(leading_coeff) < TOL:
        return "最高次係數接近0，請檢查輸入"
    
    c_norm = c / leading_coeff 
    
    a = c_norm[:-1]  
   
    companion = np.zeros((n, n), dtype=complex)
    companion[1:, :-1] = np.eye(n-1) 
    companion[0, :] = -a[::-1]       
    
    roots = np.linalg.eigvals(companion)
  
    roots = np.real_if_close(roots, tol=1e-8)
    return roots

print(root([1, -7, 14, -8]))
print(root([-1, -1, 0, 0, 0, 1]))