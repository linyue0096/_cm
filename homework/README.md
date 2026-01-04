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
* 完成方法:原創
* 這是一個二次方程跟x**2+bx+c=0，a、b、c的變數不能為0。
**[(-b+cmath.sqrt(ds))/(2*a)]**
**[(-b-cmath.sqrt(ds))/(2*a)]**
- 步驟一：係數標準化
先將方程式的領導係數 $a$ 化為 1。若 $a=0$ 則不是三次方程式，需拋出錯誤。
```python
def root3(a,b,c,d):
    if a==0:
        raise ValueError("係數a不能為0")
    b /= a
    c /= a
    d /= a
```
將一般式轉化為首一多項式，方便後續代入公式。

- 步驟二：轉換為缺項三次方程式
透過變數變換 $x = y - \frac{b}{3}$，消去$x^2$ 項，將方程式簡化為$y^3 + py + q = 0$ 的形式
```python
p = c - (b**2)/3
    q = (2*b**3)/27 - (b*c)/3 + d
```
- 數學原理:$p = \frac{3ac - b^2}{3a^2}$ 
$q = \frac{2b^3 - 9abc + 27a^2d}{27a^3}$

- 步驟三：計算判別式與卡爾丹諾解
利用判別式 $\Delta$ 計算 $u$ 與 $v$ 的立方值，並引入單位根 $\omega$ 來求出所有解
```python
delta = (q/2)**2 + (p/3)**3
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
```
1. 判別式: $\Delta = (\frac{q}{2})^2 + (\frac{p}{3})^3$，決定了根的性質（實根或複數根）。
2. 卡爾丹諾公式: 解的形式為 $y = u + v$，其中 $u = \sqrt[3]{-\frac{q}{2} + \sqrt{\Delta}}$，$v = \sqrt[3]{-\frac{q}{2} - \sqrt{\Delta}}$。
3. 單位根: 由於複數開立方會有三個根，我们需要乘上 $1, \omega, \omega^2$ 來組合出三個解
- 步驟四：組合還原根並驗證
算出的 $y$ 值還原回 $x$ (即 $x = y - \frac{b}{3}$)
```python
roots= []
    for k in range(3):
        y = u * omega[k] + v * omega[(3-k) % 3] 
        x = y - b/3
        roots.append(x)
    return roots
```
-----------------------------------------------------
## [家庭作業 5 (請寫出有限體)]
* 完成方法:[使用GPT1](https://chatgpt.com/share/6922c855-b214-800d-987c-8fedb0458f4e)
          [使用GPT2](https://chatgpt.com/share/6922e95d-5174-800d-9018-8f6274c7e5a8)
          [使用Gemini]()
* 說明:甚麼是有限體?有限體是一個具有有限多個元素的代數結構，它滿足體的定義。(最簡單的有限體是GF(p)，其中p是一個質數)

- 步驟一:判斷n是否為質數 (因:體的大小p必須為質數)
```python 
def is_prime(n):  #判斷n是質數
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n: 
        if n % i == 0:
            return False
        i += 2
    return True
```

- 步驟二:基本的加減乘負運算
```python
class GFElement:
    """GF(p) 元素"""
    def __init__(self, value, field: 'FiniteField'):
        self.value = value % field.p
        self.field = field

    def __repr__(self):
        return f"GF({self.field.p})[{self.value}]"
```
1. 類別定義與初始化:定義了類別本身，在建立物件時初始化它的值，和它的有限域，確保其值始終保持在正確的範圍內

```python
    def __add__(self, other):
        other_val = other.value if isinstance(other, GFElement) else other
        return GFElement((self.value + other_val) % self.field.p, self.field)
    __radd__ = __add__
    def __sub__(self, other):
        other_val = other.value if isinstance(other, GFElement) else other
        return GFElement((self.value - other_val) % self.field.p, self.field)

    def __rsub__(self, other):
        return GFElement((other - self.value) % self.field.p, self.field)

    def __mul__(self, other):
        other_val = other.value if isinstance(other, GFElement) else other
        return GFElement((self.value * other_val) % self.field.p, self.field)
    __rmul__ = __mul__

    def __neg__(self):
        return GFElement(-self.value % self.field.p, self.field)

    def __truediv__(self, other):
        other_val = other.value if isinstance(other, GFElement) else (other % self.field.p)
        if other_val == 0:
            raise ZeroDivisionError("division by zero in finite field")
        inv = pow(other_val, -1, self.field.p)
        return GFElement((self.value * inv) % self.field.p, self.field)

    def __rtruediv__(self, other):
        if self.value == 0:
            raise ZeroDivisionError("division by zero in finite field")
        inv = pow(self.value, -1, self.field.p)
        return GFElement((other * inv) % self.field.p, self.field)

    def __eq__(self, other):
        if isinstance(other, GFElement):
            # 修正：比較 p 而非 field 物件
            return self.value == other.value and self.field.p == other.field.p
        return self.value == (other % self.field.p)
```
1. 封閉性維持：所有的加減乘算完後，都會立刻做 % p 運算，確保結果仍在有限體內。
2. 運算子重載 (Operator Overloading)：透過定義 __add__, __mul__ 等方法，讓我們可以直接用 +, *, / 符號來操作有限體元素。
3. 除法定義：有限體沒有一般的除法，而是乘上[乘法反元素]。程式中使用 pow(val, -1, p) 來計算模反元素。
- 步驟三:建構有限體並驗證公理
```python
class FiniteField:
    """有限體 GF(p)"""
    def __init__(self, p):
        if not is_prime(p):
            raise ValueError(f"{p} 不是質數，無法建構 GF(p)")
        self.p = p
        self.add_elements = [GFElement(i, self) for i in range(p)]
        self.mul_elements = [GFElement(i, self) for i in range(1, p)]

    def element(self, value):
        return GFElement(value, self)

    # ====== 群公理檢測 ======
    def test_add_group(self):
        results = {
            "closure": all(a + b in self.add_elements for a in self.add_elements for b in self.add_elements),
            "associativity": all((a + b) + c == a + (b + c) 
                                 for a in self.add_elements for b in self.add_elements for c in self.add_elements),
            "identity": all(a + self.element(0) == a for a in self.add_elements),
            "inverse": all(a + (-a) == self.element(0) for a in self.add_elements)
        }
        return results

    def test_mul_group(self):
        results = {
            "closure": all(a * b in self.mul_elements for a in self.mul_elements for b in self.mul_elements),
            "associativity": all((a * b) * c == a * (b * c)
                                 for a in self.mul_elements for b in self.mul_elements for c in self.mul_elements),
            "identity": all(a * self.element(1) == a for a in self.mul_elements),
            # 修正：真正檢查逆元存在
            "inverse": all(
                any(a * b == self.element(1) for b in self.mul_elements)
                for a in self.mul_elements
            )
        }
        return results

    def test_distributive_law(self):
        # 修正：a 必須遍歷所有元素（含 0）
        return all(
            a * (b + c) == a * b + a * c 
            for a in self.add_elements   # ← 關鍵修正！
            for b in self.add_elements 
            for c in self.add_elements
        )
```
1. 加法群：檢查是否符合阿貝爾群(Abelian Group)的性質。
2. 乘法群：檢查去除0之後的集合是否符合阿貝爾群性質。
3. 分配律：連結加法與乘法的橋樑。 若全部回傳True，則證明是有限體

```python
if __name__ == "__main__":
    # 安全讀取質數 p
    while True:
        try:
            user_input = input("請輸入質數 p 來建立 GF(p)： ").strip()
            if not user_input:
                print("錯誤：輸入不能為空，請輸入一個質數。")
                continue
            p = int(user_input)
            break
        except ValueError:
            print("錯誤：請輸入一個有效的整數！")
    
    try:
        F = FiniteField(p)

        print("\n--- 加法群公理檢測 ---")
        for prop, ok in F.test_add_group().items():
            print(f"{prop}: {ok}")

        print("\n--- 乘法群公理檢測 ---")
        for prop, ok in F.test_mul_group().items():
            print(f"{prop}: {ok}")
 
        print("\n--- 分配律檢測 ---")
        print("分配律成立:", F.test_distributive_law())

        # 讀取 a, b, c
        def safe_input(prompt):
            while True:
                try:
                    val = input(prompt).strip()
                    if val == '':
                        print("輸入不能為空，請重新輸入。")
                        continue
                    return int(val)
                except ValueError:
                    print("請輸入整數！")

        a_val = safe_input("\n輸入 a: ")
        b_val = safe_input("輸入 b: ")
        c_val = safe_input("輸入 c: ")

        a = F.element(a_val)
        b = F.element(b_val)
        c = F.element(c_val)

        print("\n--- 運算示範 ---")
        print(f"a = {a}, b = {b}, c = {c}")
        print(f"a + b = {a + b}")
        print(f"a - b = {a - b}")
        print(f"a * b = {a * b}")
        if b.value != 0:
            print(f"a / b = {a / b}")
        else:
            print("b = 0，無法進行除法")
        print(f"a + b * c = {a + b * c}")
        print(f"(a + b) * c = {(a + b) * c}")
        print(f"-a = {-a}")

    except ValueError as e:
        print("錯誤:", e)
    except ZeroDivisionError as e:
        print("錯誤:", e)
    except Exception as e:
        print("未預期錯誤:", e)
```
1. 程式會先要求輸入質數p。
2. 自動跑完所有公理驗證，確認數學性質成立。
3. 使用者可輸入任意整數，程式會將其轉換為有限體元素並展示運算結果
4. 驗證結果：顯示的運算結果完全符合模運算(Modular Arithmetic)的規則
## [家庭作業 8 (資訊理論)]
* 完成方法: 參考教授
* 說明: