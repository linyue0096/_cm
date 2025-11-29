import cmath

def root (a,b,c):
    if a==0:
        raise ValueError("係數a不能為0，這不屬於二次方程式")
    ds=b**2 - 4*a*c
    r1=(-b+cmath.sqrt(ds))/(2*a)
    r2=(-b-cmath.sqrt(ds))/(2*a)
    return r1,r2


def df (a,b,c):
    try:
        r1,r2=root(a,b,c)
    except ValueError as e:
        return str(e),None,False
    
    r1 , r2 = root(a, b, c)
    df1 = a * (r1**2) + b*r1 +c
    df2 = a * (r2**2) + b*r2 +c

    if cmath.isclose(df1,0,rel_tol=1e-09,abs_tol=1e-9)and cmath.isclose(df2,0,rel_tol=1e-09,abs_tol=1e-9):
        return df1,df2,True
    else:
        return df1,df2,False
    
print("測試1:重根")
print (root(4,12,9))
print (df(4,12,9))

print("\n測試2:兩個實根")
print (root(4,6,2))
print (df(4,6,2))

print("\n測試3:負數根")
print (root(2,3,2))
print (df(2,3,2))

print("\n測試4:a=0")
try:
    print (root(0,3,2))
except ValueError as e:
    print("錯誤",e)

print(df(0,3,2))
