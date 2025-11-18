class FiniteAdditiveGroup:
    def __init__(self, n):
        if n <= 0:
            raise ValueError("n 必須是正整數")
        self.n = n
        self.elements = list(range(n))

    # 加法 (mod n)
    def add(self, a, b):
        return (a + b) % self.n

    # 加法單位元
    def identity(self):
        return 0

    # 加法反元素
    def inverse(self, a):
        return (-a) % self.n

    # 建立加法 Cayley 表
    def cayley_table(self):
        print(f"\n加法 Cayley 表  Z_{self.n}：")
        print("     " + " ".join([f"{b:3}" for b in self.elements]))
        print("     " + "---"*self.n)
        for a in self.elements:
            row = [self.add(a, b) for b in self.elements]
            print(f"{a:3} | " + " ".join([f"{x:3}" for x in row]))

    # 檢查群公理
    def check_group_axioms(self):
        e = self.identity()

        # 1. 封閉性
        for a in self.elements:
            for b in self.elements:
                if self.add(a, b) not in self.elements:
                    return False, "未滿足封閉性"

        # 2. 結合性 (a+b)+c == a+(b+c)
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    if self.add(self.add(a, b), c) != self.add(a, self.add(b, c)):
                        return False, "未滿足結合律"

        # 3. 單位元
        for a in self.elements:
            if self.add(a, e) != a or self.add(e, a) != a:
                return False, "未找到單位元"

        # 4. 反元素
        for a in self.elements:
            if self.add(a, self.inverse(a)) != e:
                return False, "沒有反元素"

        return True, "已滿足所有群公理"

class FiniteMultiplicativeGroup:
    def __init__(self, p):
        # p 必須是質數，以保證 Z_p 是一個有限體
        self.p = p
        self.elements = list(range(1, p))  # 1 ~ p-1，不包含 0

    # 群運算：乘法 mod p
    def mul(self, a, b):
        return (a * b) % self.p

    # 單位元（恆等元素，identity element）
    def identity(self):
        return 1

    # 反元素（a 的乘法反元素）
    def inverse(self, a):
        # 使用費馬小定理：a^(p-2) mod p = a⁻¹
        return pow(a, self.p - 2, self.p)

    # 印出乘法 Cayley 表
    def cayley_table(self):
        print(f"\n乘法 Cayley 表  (Z_{self.p}^×)：")
        print("     " + " ".join([f"{b:3}" for b in self.elements]))
        print("     " + "---"*len(self.elements))
        for a in self.elements:
            row = [self.mul(a, b) for b in self.elements]
            print(f"{a:3} | " + " ".join([f"{x:3}" for x in row]))

    # 檢查群四大公理
    def check_group_axioms(self):
        e = self.identity()

        # 1. 封閉性：a*b mod p 必須仍在元素集合
        for a in self.elements:
            for b in self.elements:
                if self.mul(a, b) not in self.elements:
                    return False, "  未滿足封閉性"

        # 2. 結合律：(ab)c = a(bc)
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    if self.mul(self.mul(a, b), c) != self.mul(a, self.mul(b, c)):
                        return False, "未滿足結合律"

        # 3. 單位元存在：a * 1 = a = 1 * a
        for a in self.elements:
            if self.mul(a, e) != a or self.mul(e, a) != a:
                return False, "單位元不存在"

        # 4. 每個元素有反元素：a * a⁻¹ = 1
        for a in self.elements:
            if self.mul(a, self.inverse(a)) != e:
                return False, f"缺少元素 {a} 的反元素"

        return True, "已滿足所有群公理！"
