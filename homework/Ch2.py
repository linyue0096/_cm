import cmath

def root (a,b,c):
    ds=b**2 - 4*a*c
    r1=(-b+cmath.sqrt(ds))/(2*a)
    r2=(-b-cmath.sqrt(ds))/(2*a)
    return r1,r2

def df (a,b,c):
    r1 , r2 = root(a, b, c)
    df1 = a * (r1**2) + b*r1 +c
    df2 = a * (r2**2) + b*r2 +c
    if cmath.isclose(df1,0,rel_tol=1e-09,abs_tol=1e-9)and cmath.isclose(df2,0,rel_tol=1e-09,abs_tol=1e-9):
        return df1,df2,True
    else:
        return df1,df2,False
    
print (root(4,12,9))
print (df(4,12,9))

print (root(4,6,2))
print (df(4,6,2))

print (root(2,3,2))
print (df(2,3,2))
