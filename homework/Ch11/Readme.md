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
# 演算法邏輯
由於電腦數值計算存在浮點數誤差，以採用了以下步驟來確保結果的數學正確性：
1. 求根 (Root Finding)：使用 numpy.roots 求解特徵多項式。
2. 數據清洗:
* 將根的實部與虛部四捨五入至小數點後 5 位。
* 去除極小的虛部雜訊（強制轉換為純實數）。
* 此步驟確保了「重根」能被正確識別，而不是被誤判為兩個極為接近的相異根。
3. 根的分類:使用Counter統計根的重數。
4. 字串生成:若為實根 $r$ (重數 $m$)：生成 $C e^{rx}, C x e^{rx}, \dots$若為複數根 $\alpha \pm i\beta$ (重數 $m$):生成 $e^{\alpha x}\cos(\beta x), e^{\alpha x}\sin(\beta x)$ 及其對應的 $x$ 乘積項。

## 求解特徵方程
``` python
def solve_ode_general(coefficients):
    # 利用 numpy 找出特徵方程式 P(r) = 0 的所有根
    roots = np.roots(coefficients)

```
* 邏輯:對應數學步驟的第一步。
* 數學意義：將微分方程 $a_n y^{(n)} + \dots + a_0 y = 0$ 轉為特徵方程 $a_n r^n + \dots + a_0 = 0$ 並求解 $r$。

## 數據清洗
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

## 統計重數與排序
``` python

root_counts = Counter(cleaned_roots)
    
    
sorted_unique_roots = sorted(
    root_counts.keys(), 
    key=lambda x: (abs(x.imag) > 0, x.real, x.imag)
)

```
* Counter:如果根是 [2.0, 2.0]，Counter 會回傳 {2.0: 2}，告訴我們 $r=2$ 是二重根 ($m=2$)。
* sorted:為了讓輸出的數學式美觀，我們自訂排序規則，讓實數解排在複數解前面。

## 生成通解字串
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

## 組合最終結果
``` python
    result = " + ".join(terms)
    result = result.replace("+ -", "- ")
    
    return f"y(x) = {result}"
```