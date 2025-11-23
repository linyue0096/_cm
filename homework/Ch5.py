class FiniteField:
    """有限體 GF(p)"""
    def __init__(self, p):
        if p <= 2:
            raise ValueError("p 必須是質數且大於 2")
        self.p = p
        self.add_elements = [GFElement(i, self) for i in range(p)]
        self.mul_elements = [GFElement(i, self) for i in range(1, p)]  # 1..p-1

    def element(self, value):
        return GFElement(value % self.p, self)

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
            "inverse": all(a / a == self.element(1) for a in self.mul_elements)
        }
        return results

    def test_distributive_law(self):
        return all(a * (b + c) == a * b + a * c 
                   for a in self.mul_elements for b in self.add_elements for c in self.add_elements)

class GFElement:
    """GF(p) 元素"""
    def __init__(self, value, field: FiniteField):
        self.value = value % field.p
        self.field = field

    def __repr__(self):
        return f"GF({self.field.p})[{self.value}]"

    # 加法
    def __add__(self, other):
        other_val = other.value if isinstance(other, GFElement) else other
        return GFElement((self.value + other_val) % self.field.p, self.field)
    __radd__ = __add__

    # 減法
    def __sub__(self, other):
        other_val = other.value if isinstance(other, GFElement) else other
        return GFElement((self.value - other_val) % self.field.p, self.field)

    def __rsub__(self, other):
        return GFElement((other - self.value) % self.field.p, self.field)

    # 乘法
    def __mul__(self, other):
        other_val = other.value if isinstance(other, GFElement) else other
        return GFElement((self.value * other_val) % self.field.p, self.field)
    __rmul__ = __mul__

    # 負元素
    def __neg__(self):
        return GFElement(-self.value % self.field.p, self.field)

    # 除法
    def __truediv__(self, other):
        other_val = other.value if isinstance(other, GFElement) else other
        inv = pow(other_val, -1, self.field.p)
        return GFElement((self.value * inv) % self.field.p, self.field)

    def __rtruediv__(self, other):
        inv = pow(self.value, -1, self.field.p)
        return GFElement((other * inv) % self.field.p, self.field)

    # 比較
    def __eq__(self, other):
        if isinstance(other, GFElement):
            return self.value == other.value and self.field == other.field
        return self.value == other % self.field.p

# ==========================
#       示範程式
# ==========================
if __name__ == "__main__":
    p = int(input("請輸入質數 p (>2) 來建立 GF(p)： "))
    F = FiniteField(p)

    print("\n--- 加法群公理檢測 ---")
    for prop, ok in F.test_add_group().items():
        print(f"{prop}: {ok}")

    print("\n--- 乘法群公理檢測 ---")
    for prop, ok in F.test_mul_group().items():
        print(f"{prop}: {ok}")

    print("\n--- 分配律檢測 ---")
    print("分配律成立:", F.test_distributive_law())

    # 使用示範
    a = F.element(int(input("\n輸入 a: ")))
    b = F.element(int(input("輸入 b: ")))
    c = F.element(int(input("輸入 c: ")))

    print("\n--- 運算示範 ---")
    print(f"a = {a}, b = {b}, c = {c}")
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"a / b = {a / b}")
    print(f"a + b * c = {a + b * c}")
    print(f"(a + b) * c = {(a + b) * c}")
    print(f"-a = {-a}")
