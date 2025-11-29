import cmath

def root3(a,b,c,d):
    if a==0:
        raise ValueError("係數a不能為0")
    
    b /= a
    c /= a
    d /= a

    p=c-(b**2)/3
    q=(2*b**3)/27-(b*c)/3+d

    delta=(q/2)**2+(p/3)**3

    sqrt_delta = cmath.sqrt(delta)

    u_cub = (-q/2 + sqrt_delta)
    v_cub = (-q/2 - sqrt_delta)

    u = u_cub ** (1/3)
    v = v_cub ** (1/3)

    omega = [
        1, 
        -0.5 + cmath.sqrt(3)/2*1j,
        -0.5 - cmath.sqrt(3)/2*1j
    ]
    
    roots= []
    
    for k in range(3):
        y = u_cub * omega[k] + v_cub * omega[(3-k) % 3]
        x = y - b/3
        roots.append(x)

    return roots

print("測試1:x^3-6x^2+11x-6=0(根為 1, 2, 3)")
result1 = root3(1, -6, 11, -6)
print([x.real if abs(x.imag) < 1e-10 else x for x in result1])

print("\n測試2:x^3-1=0(一個實根1，兩個複根)")
result2 = root3(1, 0, 0, -1)
print([x.real if abs(x.imag) < 1e-10 else x for x in result2])

print("\n測試3:x^3-3x^2+3x-1=0(重根,(x-1)^3 = 0)")
result3 = root3(1, -3, 3, -1)
print([x.real if abs(x.imag)<1e-10 else x for x in result3])

print("\n測試4:x^3 - x = 0 (根為 0, 1, -1)")
result4 = root3(1, 0, -1, 0)
print([x.real if abs(x.imag) < 1e-10 else x for x in result4])