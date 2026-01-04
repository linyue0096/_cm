def is_prime(n):
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


class GFElement:
    """GF(p) 元素"""
    def __init__(self, value, field: 'FiniteField'):
        self.value = value % field.p
        self.field = field

    def __repr__(self):
        return f"GF({self.field.p})[{self.value}]"

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


# ==========================
#       示範程式
# ==========================
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