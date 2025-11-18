import math

def root3(a,b,c,d):
    b /= a
    c /= a
    d /= a

    p = c - (b**2)/3
    q = (2*b**3)/27 - (b*c)/3 + d

    delta = (q/2)**2 + (p/3)**3

    u = math.sqrt(delta)
    u_cub = (-q/2 + u) ** (1/3)
    v_cub = (-q/2 - u) ** (1/3)

    omega = [1, 
             -0.5 + math.sqrt(3)/2*1j,
             -0.5 - math.sqrt(3)/2*1j]
    
    roots= []
    
    for k in range(3):
        y = u_cub * omega[k] + v_cub * omega[(3-k) % 3]
        x = y - b/3
        roots.append(x)

    return roots

print(root3(1, -6, 11, -6))