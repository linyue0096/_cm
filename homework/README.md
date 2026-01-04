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
## [家庭作業 4 (請寫一個函數 root(c) 求出 n 次多項式的根)]
* 完成方法:原創(readme使用Gemini幫忙寫)
* 這是利用 Python 的 numpy 函式庫實作同伴矩陣方法。此程式能求出任意 $n$ 次多項式 $P(x) = c_n x^n + \dots + c_1 x + c_0 = 0$ 的所有根（包含實根與複數根）。這是目前許多科學計算軟體計算多項式根的標準演算法
先將方程式的領導係數 $a$ 化為 1。若 $a=0$ 則不是三次方程式，需拋出錯誤。

- 步驟一：係數預處理與降階
多項式的係數列表中，最高次項的係數不能為 0，否則它就不是該次數的多項式。我們需要清理輸入數據
```python
c = np.array(c, dtype=float)
    while len(c) > 0 and abs(c[-1]) < TOL:
        c = c[:-1]
```
* 輸入格式: 程式預設輸入列表為 [常數項, 一次項, ..., 最高次項] (升冪排列)。
* 防呆機制: 若輸入列表全為 0 或為空，則直接回傳對應的訊息，避免程式崩潰。
* 特殊情況: 若清理後 $n=1$，直接回傳線性解 $-c_0/c_1$。

- 步驟二: 正規化與構建同伴矩陣
將多項式轉化為首一多項式，並建立其對應的同伴矩陣
```python
leading_coeff = c[-1]
    c_norm = c / leading_coeff
    
    a = c_norm[:-1]
    companion = np.zeros((n, n), dtype=complex)
    companion[1:, :-1] = np.eye(n-1)
    companion[0, :] = -a[::-1] 
```
1. 正規化: 將所有係數除以最高次係數 leading_coeff。
2. 矩陣構造: 利用 np.eye 快速建立次對角線，並將係數填入矩陣的第一列（或最後一列/行，視定義而定，此程式碼採用頂列形式）

- 步驟三：計算特徵值
根據線性代數定理，同伴矩陣 $C$ 的特徵值 (Eigenvalues) 恰好就是原多項式 $P(x)$ 的根。
```python
roots = np.linalg.eigvals(companion)
    roots = np.real_if_close(roots, tol=1e-8)
    return roots
```
1.核心原理: 我們將非線性的「多項式求根問題」轉換為線性的「矩陣特徵值問題」。
2. 數值運算: 使用 np.linalg.eigvals 進行 QR 分解或類似算法來迭代求出特徵值。
3.後處理: 使用 np.real_if_close 將虛部極小的複數根轉換為實數，讓結果更乾淨。
- 步驟四：測試結果
將高次方程式轉化為矩陣運算的高效解法，無需針對特定次數背誦公式 (如三次、四次公式)，適用於任意 $n$ 次多項式
```python
print(root([1, -7, 14, -8]))
print(root([-1, -1, 0, 0, 0, 1]))
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
-----------------------------------------------------
## [家庭作業 6 (幾何學：（點，線，圓）世界的建構)]
* 完成方式:[Gemini](https://gemini.google.com/share/61bc6b22edf3)
* 說明:定義基本的幾何圖形（點、線、圓、三角形）與計算它們的交點外，還實作了圖形的幾何變換。
先將方程式的領導係數 $a$ 化為 1。若 $a=0$ 則不是三次方程式，需拋出錯誤。

- 步驟一：幾何物件定義與數學模型
1. 點: 平面座標系上的位置 $P(x, y)$。
2. 直線: 使用一般式 $Ax + By + C = 0$ 表示。
優點: 可以表示垂直線 ($x=k$, 即 $B=0$)，這是斜截式 ($y=mx+b$) 做不到的。
3. 圓: 由圓心 $O(h, k)$ 與半徑 $r$ 定義，方程式為 $(x-h)^2 + (y-k)^2 = r^2$。
4. 三角形: 由三個頂點 $P_1, P_2, P_3$ 組成的封閉圖形。

- 步驟二: 交點計算原理
1. 兩直線交點:求解二元一次聯立方程式
* 克拉瑪法則 (Cramer's Rule)：
$$D = A_1 B_2 - A_2 B_1$$$$x = \frac{B_1 C_2 - B_2 C_1}{D}, \quad y = \frac{C_1 A_2 - C_2 A_1}{D}$$
若 $D=0$，則直線平行或重合
2. 直線與圓交點:計算圓心到直線的垂直距離 $d = \frac{|Ax_0 + By_0 + C|}{\sqrt{A^2+B^2}}$。
* 若 $d > r$: 不相交。
* 若 $d = r$: 相切 (一點)。
* 若 $d < r$: 交於兩點 (割線)。
3. 兩圓交點:計算兩圓心距離 $d$。利用餘弦定理或幾何關係求出交點連線（根軸）的位置，再轉化為[直線與圓交點]
--------------------------------------------------
## [家庭作業 7 機率統計 - 檢定背後的數學原理]
* 完成方式:[Gemini](https://gemini.google.com/share/70c6a8082e11)
* 利用AI問答，理解z檢定與t檢定背後的數學原理(包含公式是如何推導出來的)
* z-test
單樣本 -- 在母體標準差和平均值已知的情況
* t-test
單樣本 -- 母體標準差未知，母體平均值已知
雙樣本獨立 -- 兩組不同且獨立的樣本
雙樣本配對 -- 同樣個體不同時間的樣本
* 數學原理:
$$t = \frac{\bar{X}_1 - \bar{X}_2}{S_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}$$
* 分子 $(\bar{X}_1 - \bar{X}_2)$: 兩組間的實際差異。
* 分母 $S_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}$: 估計的標準誤 (Standard Error)，代表隨機抽樣下的預期波動。
------------------------------------------------------------
## [家庭作業 8 (資訊理論)]
* 完成方式:[Gemini](https://gemini.google.com/share/1448ea73b408)
* 夏農-哈特利定理和夏農信道編碼定理:[Readme](https://github.com/linyue0096/_cm/blob/5663b842f87aa053a9c1f3d637dc08a7a94dfbed/homework/Ch8%20%E8%B3%87%E8%A8%8A%E7%90%86%E8%AB%96/readme.md)
1. 寫一個程式，計算一公平銅板，連續投擲 10000 次，全部得到正面的機率。 (p^10000)
2. 寫另一個程式，用 log(p^n) = n log(p) 計算 log(p^n)，然後代入 p=0.5，算出 log(0.5^10000)
3. 寫程式計算『熵，交叉熵，KL 散度，互熵（互資訊）』
4. 寫程式驗證 cross_entropy(p,p) > cross_entropy(p,q), 當 q != p 時。
5. 寫出 『7-4 漢明碼』的編碼與解碼程式
- 驗證吉布斯不等式
透過數值模擬驗證「交叉熵恆大於等於熵」，即 $H(P, Q) \ge H(P)$
```python
def verify_inequality():
    # 設定真實分佈 P，並計算基準值 H(P)
    self_entropy = cross_entropy(P, P)
    
    # 隨機生成多個 Q 分佈進行測試
    for i in range(5):
        # ... (生成隨機 Q) ...
        ce_val = cross_entropy(P, Q)
        is_greater = ce_val > self_entropy # 驗證 H(P,Q) > H(P)
```
在機器學習證明了為什麼我們要最小化 Cross-Entropy Loss。因為當 Loss 降到最低（等於 $H(P)$）時，代表我們的預測模型 $Q$ 已經完美逼近真實分佈 $P$（即 $D_{KL} \to 0$）

- 通道編碼 - 漢明碼 (Hamming Code)
資訊理論不僅討論資訊的度量，也討論如何在雜訊通道中可靠傳輸。
```python
class Hamming74:
    def __init__(self):
        # 生成矩陣 G [4x7] : 負責編碼
        self.G = np.array([...]) 
        # 校驗矩陣 H [3x7] : 負責偵錯
        self.H = np.array([...])

    def encode(self, d):
        # c = d * G (mod 2)
        return np.dot(d, self.G) % 2

    def decode(self, r):
        # 計算校驗子 (Syndrome): s = H * r^T
        syndrome = np.dot(self.H, r) % 2
```
* 編碼效率:使用3個parity bits保護4個data bits，碼率 $R = 4/7$。
* 校驗子 (Syndrome): $\mathbf{s} = \mathbf{H}\mathbf{r}^T = \mathbf{H}(\mathbf{c}+\mathbf{e})^T = \mathbf{H}\mathbf{e}^T$。
* 因為 $\mathbf{H}$ 的每一行都是獨特的，所以算出的 $\mathbf{s}$ 可以唯一對應到錯誤向量 $\mathbf{e}$ 中的錯誤位置，實現 1 bit 的自動修正
-------------------------------------------------------
## [家庭作業 9 線性代數]
* 完成方式(利用Gemini幫我寫數學原理):[Gemini](https://gemini.google.com/share/578c7a046eca)
* 觀念題:[README](https://github.com/linyue0096/_cm/blob/5663b842f87aa053a9c1f3d637dc08a7a94dfbed/homework/Ch9%20%E7%B7%9A%E6%80%A7%E4%BB%A3%E6%95%B8/ReadMe.md)
* 從零開始實作了線性代數中的核心演算法。內容涵蓋矩陣運算（行列式、反矩陣）、高效的矩陣分解（LU、SVD），以及資料科學中最重要的降維技術（PCA）

- 步驟一：行列式與反矩陣
* 遞迴行列式:利用拉普拉斯展開，將 $n \times n$ 矩陣拆解為多個 $(n-1) \times (n-1)$ 子矩陣的行列式和。
$$\det(A) = \sum_{j=1}^{n} (-1)^{1+j} a_{1j} \det(M_{1j})$$
* 伴隨矩陣法求反矩陣 (Inverse via Adjugate):若 $\det(A) \neq 0$，則：$$A^{-1} = \frac{1}{\det(A)} \text{adj}(A)$$
```python
def inverse(matrix):
    det = determinant(matrix)
    if det == 0: raise ValueError("Singular Matrix")
    adjugate = transpose(cofactors)
    return [[elem / det for elem in row] for row in adjugate]
```
- 步驟二: 矩陣分解 LU 分解
1. Doolittle 演算法:逐步消除矩陣下方的元素，將其儲存在 $L$ 中，剩餘部分形成 $U$。
2. 快速計算行列式:一旦分解完成，行列式即為 $U$ 矩陣對角線元素的乘積：$$\det(A) = \det(L) \cdot \det(U) = 1 \cdot \prod_{i=1}^{n} u_{ii}$$
```python
def determinant_via_lu(matrix):
    L, U = lu_decomposition(matrix)
    # 行列式 = U 的對角線乘積
    det = 1.0
    for i in range(len(U)):
        det *= U[i][i]
    return det
```
- 步驟三：奇異值分解
線性代數的任意矩陣 $A$ 都可以分解為 $A = U \Sigma V^T$。這表示矩陣的幾何本質：旋轉 $\to$ 拉伸 $\to$ 旋轉
* 數學原理
我們利用特徵值分解來手動實作 SVD：
1. 計算 $A^T A$: 這是一個對稱半正定矩陣。
2. 求解特徵值: 對 $A^T A$ 進行特徵值分解，得到的特徵向量即為 $V$。
3. 計算奇異值: $\sigma_i = \sqrt{\lambda_i}$，構成對角矩陣 $\Sigma$。
4. 推導 $U$: 利用公式 $u_i = \frac{A v_i}{\sigma_i}$ 計算左奇異向量
```python
def svd_from_eigen(A):
    ATA = A.T @ A
    eigenvalues, V = np.linalg.eig(ATA)
    singular_values = np.sqrt(eigenvalues)
    U = (A @ V) / singular_values
    return U, singular_values, V.T
```

- 步驟四：主成分分析
資料科學中最重要的降維技術。透過 SVD 或特徵值分解找出資料變異量最大的方向
* 數學原理
1. 中心化 (Centering):將數據平移，使平均值為 0。
2. 協方差矩陣 (Covariance Matrix):$$C = \frac{1}{n-1} X^T X$$
3. 特徵分解: 計算 $C$ 的特徵向量。最大的特徵值對應的方向即為第一主成分 (PC1)。
4. 投影 (Projection): 將原始數據 $X$ 投影到特徵向量上，完成降維。
```python
new_cov = np.cov(X_pca.T)
off_diagonal = new_cov - np.diag(np.diagonal(new_cov))
    
if np.allclose(off_diagonal, 0):
    print("✅ 驗算成功：新特徵之間已完全解耦")
```
--------------------------------------------------
## [家庭作業 10 請寫出傅立葉正轉換和逆轉換的函數（不要用套件）]
* 完成方式(利用Gemini幫我寫數學原理):[Gemini](https://gemini.google.com/share/8958e324d9b1)
* 從零開始實作了線性代數中的核心演算法。內容涵蓋矩陣運算（行列式、反矩陣）、高效的矩陣分解（LU、SVD），以及資料科學中最重要的降維技術（PCA）

- 步驟一：離散傅立葉轉換 (DFT)
* 將離散的時域訊號 $x[n]$ 轉換為頻域訊號 $X[k]$。
```python
def dft(x: List[float]) -> List[Complex]:
    # ...
    coefficient = -2j * math.pi / N
    for k in range(N):
        # 核心數學式: X[k] = Σ x[n] * e^(-j * 2π * k * n / N)
        value = sum(x[n] * cmath.exp(coefficient * k * n) for n in range(N))
        X.append(value)
    return X
```
* 數學原理:
$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2\pi}{N} k n}$$
* 利用歐拉公式 
$e^{-j\theta} = \cos\theta - j\sin\theta$，我們將時域訊號投影到一組正交的複數弦波基底上。
* 複雜度: 雙重迴圈結構 (隱藏在 sum 與外層 loop)，時間複雜度為 $O(N^2)$。
- 步驟二: 逆離散傅立葉轉換 (IDFT)
將頻域訊號 $X[k]$ 還原回時域訊號 $x[n]$。
```python
def idft(X: List[Complex]) -> List[float]:
    # ...
    coefficient = 2j * math.pi / N  # 注意：指數為正
    for n in range(N):
        # 核心數學式: x[n] = (1/N) * Σ X[k] * e^(j * 2π * k * n / N)
        value = sum(X[k] * cmath.exp(coefficient * k * n) for k in range(N))
        x.append(value.real / N) # 取實部並正規化
    return x
```
* 數學原理:
$$x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] \cdot e^{j \frac{2\pi}{N} k n}$$
* 正交歸一性: 逆轉換需要除以訊號長度 $N$ 進行正規化。
* 實數還原: 理論上原始訊號若為實數，IDFT 計算結果的虛部應相互抵銷為 0。程式中直接取 .real 濾除極微小的浮點數誤差。
- 步驟三：訊號生成與頻譜分析
生成一個由不同頻率組成的合成波
```python
def generate_signal(N: int) -> List[float]:
    # f(n) = 1.0*sin(2πn/N) + 0.5*cos(4πn/N)
    # 對應頻率 k=1 (sin) 和 k=2 (cos)
    return [...]
```
包含頻率 $k=1$ 的正弦波與 $k=2$ 的餘弦波
- 步驟四:驗證結果
資料科學中最重要的降維技術。透過 SVD 或特徵值分解找出資料變異量最大的方向
```python
magnitudes = [abs(val) for val in X]
```
* 程式成功透過 math.isclose 驗證了 $x[n] \approx \text{IDFT}(\text{DFT}(x[n]))$，證明手寫演算法正確無誤。
------------------------------------------------------
## [家庭作業 11 (資訊理論)]
* 完成方法(Gemini幫我寫，並讓AI幫我說明):[Gemini](https://gemini.google.com/share/111fde1c9c43)
* 微分方程的形式
$$a_n y^{(n)} + a_{n-1} y^{(n-1)} + \dots + a_1 y' + a_0 y = 0$$

``` python
from ode_solver import solve_ode_general 
coeffs = [1, -3, 2]
solution = solve_ode_general(coeffs)

print(f"係數: {coeffs}")
print(f"通解: {solution}")
# 輸出: y(x) = C_1e^(2.0x) + C_2e^(1.0x)
```
### 演算法邏輯
由於電腦數值計算存在浮點數誤差，以採用了以下步驟來確保結果的數學正確性：
1. 求根 (Root Finding)：使用 numpy.roots 求解特徵多項式。
2. 數據清洗:
* 將根的實部與虛部四捨五入至小數點後 5 位。
* 去除極小的虛部雜訊（強制轉換為純實數）。
* 此步驟確保了「重根」能被正確識別，而不是被誤判為兩個極為接近的相異根。
3. 根的分類:使用Counter統計根的重數。
4. 字串生成:若為實根 $r$ (重數 $m$)：生成 $C e^{rx}, C x e^{rx}, \dots$若為複數根 $\alpha \pm i\beta$ (重數 $m$):生成 $e^{\alpha x}\cos(\beta x), e^{\alpha x}\sin(\beta x)$ 及其對應的 $x$ 乘積項。

### 求解特徵方程
``` python
def solve_ode_general(coefficients):
    # 利用 numpy 找出特徵方程式 P(r) = 0 的所有根
    roots = np.roots(coefficients)

```
* 邏輯:對應數學步驟的第一步。
* 數學意義：將微分方程 $a_n y^{(n)} + \dots + a_0 y = 0$ 轉為特徵方程 $a_n r^n + \dots + a_0 = 0$ 並求解 $r$。

### 數據清洗
``` python
cleaned_roots = []
    tolerance = 5  # 設定精確度: 小數點後 5 位
    
    for r in roots:
        # 1. 四捨五入: 強制將 1.9999999 轉回 2.0
        real_part = round(r.real, tolerance)
        imag_part = round(r.imag, tolerance)
        
        # 2. 濾除雜訊: 如果虛部極小 (例如 1e-15)，強制設為 0
        if abs(imag_part) == 0.0:
            cleaned_roots.append(complex(real_part, 0))
        else:
            cleaned_roots.append(complex(real_part, imag_part))

```
* 為什麼要這樣做？ 電腦在計算浮點數時不精確
* 如果不清洗，程式會誤判為「兩個不同的實根」，導致錯誤的通解。所以透過 round 統一數值，確保重根能被正確識別。

### 統計重數與排序
``` python

root_counts = Counter(cleaned_roots)
    
    
sorted_unique_roots = sorted(
    root_counts.keys(), 
    key=lambda x: (abs(x.imag) > 0, x.real, x.imag)
)

```
* Counter:如果根是 [2.0, 2.0]，Counter 會回傳 {2.0: 2}，告訴我們 $r=2$ 是二重根 ($m=2$)。
* sorted:為了讓輸出的數學式美觀，我們自訂排序規則，讓實數解排在複數解前面。

### 生成通解字串
1. 變數
``` python
terms = []
    c_index = 1 
    processed_conjugates = set()
```

2. 實數根處理
``` python
if r.imag == 0:
    alpha = r.real
    for k in range(m):
        term = f"C_{c_index}{x_str}{exp_str}"
        terms.append(term)
        c_index += 1
```

2. 複數根處理
``` python
else:
     if r in processed_conjugates: continue
    processed_conjugates.add(r)
    processed_conjugates.add(r.conjugate())
    for k in range(m):
        term1 = f"C_{c_index}{x_str}{exp_str}{cos_str}"
        c_index += 1
        term2 = f"C_{c_index}{x_str}{exp_str}{sin_str}"
                c_index += 1
                
        terms.append(term1)
        terms.append(term2)
```
* 當根為複數 ($\alpha \pm i\beta$) 時，通解形式為 $e^{\alpha x}(C_1 \cos \beta x + C_2 \sin \beta x)$。
* 邏輯:複數根總是成對出現。我們使用 processed_conjugates 來確保不會對同一對根輸出兩次解

### 組合最終結果
``` python
    result = " + ".join(terms)
    result = result.replace("+ -", "- ")
    
    return f"y(x) = {result}"
```