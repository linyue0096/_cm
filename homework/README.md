# 每題說明

## [家庭作業 1 (驗證微積分基本定理)]
* 完成方法: 參考教授
* 說明:這是利用Python程式去驗證微積分的基本定理。
* 微積分基本定理是[微分]和[積分]兩大核心定理。

- 步驟一：設置精度
先設置h=0.00001，h的大小會影響浮點數，太大會不精準，太小會因為浮點數錯誤，導致結果不穩定，所以在電腦裡要轉化成一個可控制的有限近似。

- 步驟二：定義數值微分與積分函數
```python
 def df(f, x):
   return (f(x+h)-f(x))/h
```
這是微分的近似定義： 差商公式，透過這個函數，我能觀察一個函數在某一點的變化速率。
```python
def integral(f, a, b):
    x = a
    area = 0
    while x < b:
       area += f(x) * h
       x += h
       return area
```
這部分是積分的近似定義，原理是將區間[a,b] 切成許多小矩形，累加每個矩形的面積。

- 步驟三：驗證微積分基本定理
```python
def theorem1(f, x):
   r = df(lambda x:integral(f, 0, x), x)
   print('r=', r, 'f(x)=', f(x))
   print('abs(r-f(x))<0.01 = ', abs(r-f(x))<0.01)
   assert abs(r-f(x))<0.01
```
** 這是整個程式碼的核心 **
1. 用df()去對它做微分，理論上應該得到原函數f(x)。
2. 執行後，兩者的差並設下誤差條件（小於 0.01）。
- 步驟四：以範例函數測試
```python
def f(x):
   return x**3
print('df(f, 2)=', df(f, 2))
print('integral(f, 0, 2)=', integral(f, 0, 2))
theorem1(f, 2)
```
1. 我用ｆ(x)=x**3測試。
2. 導數：f'(x)=3x**2，所以f'(2)=12
3. 積分：∫₀**2 x**3dx
4. 而驗證部分則應該得到F'(2)≈f(2)=8
```Python
r=7.999991000014855 f(x)= 8
abs(r-f(x))<0.01=True
```
python的計算與結果是對的

--------------------------------------------------
## [家庭作業 2 (寫出圖表第二個圖表的根)]
* 完成方法:[GPT](https://chatgpt.com/share/68d5fca4-e638-800d-89cf-03067dc4a190)
* 這是一個二次方程跟x**2+bx+c=0，a、b、c的變數不能為0。
**[(-b+cmath.sqrt(ds))/(2*a)]**
**[(-b-cmath.sqrt(ds))/(2*a)]**
```python
print (root(4,12,9))
print (df(4,12,9))
#方程式 4x² + 12x + 9 = 0：
#根 = ((-1.5+0j), (-1.5+0j))
#驗證 = (0j, 0j, True)

print (root(4,6,2))
print (df(4,6,2))
#方程式 4x² + 6x + 2 = 0：
#根 = ((-0.5+0j), (-1+0j))
#驗證 = (0j, 0j, True)

print (root(2,3,2))
print (df(2,3,2))
#方程式 2x² + 3x + 2 = 0（複數根）：
#根 = ((-0.75+0.6614j), (-0.75-0.6614j))
#驗證 = (0j, 0j, True)
```
1. root(a, b, c):
2. 計算方程式的兩個根r1和r2回傳。
3. df(a, b, c):
4. 將根代回原方程式f(x) = ax**2 + bx + c驗證結果非常接近0。

-----------------------------------------------------
## [家庭作業 3 (請寫三次三次插圖式的根)]
## [家庭作業 5 (請寫出有限體)]
* 完成方法:[使用GPT]()
```python
  def __init__(self, n):
        if n <= 0:
            raise ValueError("n 必須是正整數")
        self.n = n
        self.elements = list(range(n))
```
1. 建立有限加法群的物件,n代表群的大小
2. elements存放所有元素的集合, 

```python
   def cayley_table(self):
        print(f"\n加法 Cayley 表  Z_{self.n}：")
        print("     " + " ".join([f"{b:3}" for b in self.elements]))
        print("     " + "---"*self.n)
        for a in self.elements:
            row = [self.add(a, b) for b in self.elements]
            print(f"{a:3} | " + " ".join([f"{x:3}" for x in row]))
```
1. 群的運算表
2. a=列, b=欄, Cayley表驗證群是否封閉

```python
   def check_group_axioms(self):
        e = self.identity()
```
* 檢查群公理


```python
   for a in self.elements:
            for b in self.elements:
                if self.add(a, b) not in self.elements:
                    return False, "未滿足封閉性"

   for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    if self.add(self.add(a, b), c) != self.add(a, self.add(b, c)):
                        return False, "未滿足結合律"

   for a in self.elements:
            if self.add(a, e) != a or self.add(e, a) != a:
                return False, "未找到單位元"

   for a in self.elements:
            if self.add(a, self.inverse(a)) != e:
                return False, "沒有反元素"
   return True, "已滿足所有群公理"
```
1. 檢查封閉性 : **[a*b mob p]** (結果永遠不會為0,除非a or b為0,但0不會存在於集合裡)
2. 檢查結合律 : **(ab)c=a(bc)**
3. 檢查單位元 : **a*1=a**
4. 檢查反元素 : a**(p - 1)
5. 最後返回結果


## [家庭作業 9 (資訊理論)]
* 完成方法: 參考教授
* 說明: