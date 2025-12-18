import math

# 設定浮點數比較容忍度，防止因浮點數誤差導致判斷錯誤
EPSILON = 1e-9

class Point:
    """定義點 (x, y)"""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"Point({self.x:.3f}, {self.y:.3f})"
    
    def distance_to(self, other_point):
        """計算兩點間距離"""
        return math.sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)

class Line:  # 定義直線，使用一般式 Ax + By + C = 0
    def __init__(self, A, B, C):
        self.A = float(A)
        self.B = float(B)
        self.C = float(C)

    @classmethod
    def from_points(cls, p1: Point, p2: Point):
        # (y2 - y1)x - (x2 - x1)y + (x2y1 - y2x1) = 0
        A = p2.y - p1.y
        B = p1.x - p2.x # 注意符號
        C = p2.x * p1.y - p1.x * p2.y
        return cls(A, B, C)
    
    def __repr__(self):
        return f"Line({self.A:.3f}x + {self.B:.3f}y + {self.C:.3f} = 0)"

class Circle: # 定義圓，使用 (x-h)^2 + (y-k)^2 = r^2
    def __init__(self, center: Point, radius):
        self.center = center
        self.radius = float(radius)

    def __repr__(self):
        return f"Circle(Center={self.center}, Radius={self.radius:.3f})"

# --- 幾何計算函式 ---

# 1. 計算兩直線交點 (Intersection of two Lines)
def intersect_two_lines(l1: Line, l2: Line):
    """
    計算兩直線 l1 和 l2 的交點。
    使用克拉瑪法則 解二元一次聯立方程式。
    """
    # 聯立方程組:
    # A1*x + B1*y = -C1
    # A2*x + B2*y = -C2
    
    D = l1.A * l2.B - l2.A * l1.B # 行列式 D
    
    if abs(D) < EPSILON:
        # D 接近 0，表示兩直線平行或重合
        if abs(l1.A * l2.C - l2.A * l1.C) < EPSILON and abs(l1.B * l2.C - l2.B * l1.C) < EPSILON:
             return "重合 (Coincident)", None # 重合
        else:
             return "平行 (Parallel)", None # 平行且不重合
    
    Dx = (-l1.C) * l2.B - (-l2.C) * l1.B
    Dy = l1.A * (-l2.C) - l2.A * (-l1.C)
    
    x = Dx / D
    y = Dy / D
    
    return "交於一點", Point(x, y)

# 2. 計算兩圓交點 (Intersection of two Circles)
def intersect_two_circles(c1: Circle, c2: Circle):
    """計算兩圓 c1 和 c2 的交點。"""
    
    d = c1.center.distance_to(c2.center)
    r1, r2 = c1.radius, c2.radius
    
    # 距離判斷
    if d > r1 + r2 + EPSILON:
        return "不相交 (External)", []
    if d < abs(r1 - r2) - EPSILON:
        # 內含或同心圓
        return "內含/同心 (Contained)", []
    if abs(d) < EPSILON and abs(r1 - r2) < EPSILON:
        return "重合 (Coincident)", []
    
    # 計算交點
    # a = (r1^2 - r2^2 + d^2) / (2d)
    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h = math.sqrt(abs(r1**2 - a**2)) # h 是交點弦到圓心的距離
    
    # 找出交點弦直線與兩圓心連線的交點 P2
    # P2 位於 P1 到 P2 距離為 a 的位置
    x0 = c1.center.x + a * (c2.center.x - c1.center.x) / d
    y0 = c1.center.y + a * (c2.center.y - c1.center.y) / d
    p2 = Point(x0, y0)
    
    # 找出交點
    # 交點距離 P2 為 h，方向與 P1-P2 連線垂直
    dx = (c2.center.x - c1.center.x) / d
    dy = (c2.center.y - c1.center.y) / d

    intersections = []
    
    # 第一個交點
    p_x1 = p2.x + h * dy # 注意 dy 和 dx 的位置
    p_y1 = p2.y - h * dx
    intersections.append(Point(p_x1, p_y1))

    # 第二個交點 (除非相切，否則存在)
    if abs(d - (r1 + r2)) > EPSILON and abs(d - abs(r1 - r2)) > EPSILON:
        p_x2 = p2.x - h * dy
        p_y2 = p2.y + h * dx
        intersections.append(Point(p_x2, p_y2))
        return "交於兩點", intersections

    return "相切 (Tangent)", intersections # 恰好相切

# 3. 計算直線與圓交點 (Intersection of Line and Circle)
def intersect_line_circle(l: Line, c: Circle):
    """計算直線 l 和圓 c 的交點。"""
    
    cx, cy = c.center.x, c.center.y
    r = c.radius
    A, B, C = l.A, l.B, l.C
    
    # 將圓心移到原點 (0, 0) 以簡化計算
    # 直線方程變成 A*x + B*y + (C + A*cx + B*cy) = 0
    C_prime = C + A * cx + B * cy
    
    # 計算圓心到直線的距離 d
    d = abs(C_prime) / math.sqrt(A**2 + B**2)
    
    if d > r + EPSILON:
        return "不相交", [] # 距離大於半徑
    
    # 找出垂足 P0 的座標 (最近點)
    # x0 = -A * C' / (A^2 + B^2)
    # y0 = -B * C' / (A^2 + B^2)
    A2_B2 = A**2 + B**2
    x0_rel = -A * C_prime / A2_B2
    y0_rel = -B * C_prime / A2_B2
    
    # 將垂足移回原來的座標系
    x0 = x0_rel + cx
    y0 = y0_rel + cy
    
    intersections = []
    
    if abs(d - r) < EPSILON:
        # 相切 (距離等於半徑)
        intersections.append(Point(x0, y0))
        return "相切", intersections
        
    # 相交於兩點
    if d < r - EPSILON:
        # L 是半弦長 (半弦長L^2 + d^2 = r^2)
        L = math.sqrt(r**2 - d**2)
        
        # 找出直線方向單位向量的兩個分量
        # 垂直於 (A, B)，因此方向向量為 (B, -A) 或 (-B, A)
        L_div = math.sqrt(A2_B2) # 單位化所需的除數
        
        # 第一個交點
        p1_x = x0 + L * B / L_div
        p1_y = y0 - L * A / L_div
        intersections.append(Point(p1_x, p1_y))

        # 第二個交點
        p2_x = x0 - L * B / L_div
        p2_y = y0 + L * A / L_div
        intersections.append(Point(p2_x, p2_y))
        
        return "交於兩點", intersections
        
    return "不相交", [] # 理論上應該被 d > r 涵蓋

# 4. 從線外一點向直線做垂直線
def perpendicular_line_from_point(l: Line, p_out: Point):
    """
    給定直線 l 和線外一點 p_out，計算過 p_out 且垂直於 l 的新直線。
    
    如果 l 的方程式是 A*x + B*y + C = 0，則垂直線的法向量為 (B, -A)。
    因此，垂直線的方程式是 B*x - A*y + D = 0。
    D 可以透過將 p_out(x0, y0) 代入求得： D = A*y0 - B*x0
    """
    
    A_perp = l.B
    B_perp = -l.A
    C_perp = l.A * p_out.y - l.B * p_out.x
    
    return Line(A_perp, B_perp, C_perp)

# 5. 驗證畢氏定理
def verify_pythagorean_theorem(l: Line, p_out: Point):
    """
    給定直線 L 和線外一點 P_out。
    計算垂足 H，形成直角三角形 P_out-H-P_on。
    驗證 P_outH^2 + HP_on^2 = P_outP_on^2
    """
    print("\n--- 畢氏定理驗證 ---")
    print(f"原直線 L: {l}")
    print(f"線外一點 P_out: {p_out}")

    # 步驟 1: 找出垂直線 L_perp
    l_perp = perpendicular_line_from_point(l, p_out)
    print(f"垂直線 L_perp: {l_perp}")
    
    # 步驟 2: 找出垂足 H (L 與 L_perp 的交點)
    status, h_point = intersect_two_lines(l, l_perp)
    
    if status != "交於一點":
        print(f"錯誤: 垂直線與原直線沒有交點 (狀態: {status})")
        return False

    h = h_point
    print(f"垂足 H (直角頂點): {h}")
    
    # 步驟 3: 在 L 上取一點 P_on (隨便取，只要在直線上即可)
    # 為了簡化，我們取 y=0 時的點 (如果 B!=0) 或 x=0 時的點 (如果 A!=0)
    if abs(l.A) > EPSILON:
        # 取 y=0
        p_on = Point(-l.C / l.A, 0)
    elif abs(l.B) > EPSILON:
        # 取 x=0
        p_on = Point(0, -l.C / l.B)
    else:
        print("錯誤: 直線 A=0, B=0，不是有效直線。")
        return False
        
    print(f"直線上任取一點 P_on: {p_on}")

    # 步驟 4: 計算三邊長平方
    
    # 直角邊 1: P_out 到 H 的距離平方 (d1^2)
    d1_sq = p_out.distance_to(h)**2
    print(f"直角邊 P_outH^2 (距離 d1^2): {d1_sq:.3f}")
    
    # 直角邊 2: H 到 P_on 的距離平方 (d2^2)
    d2_sq = h.distance_to(p_on)**2
    print(f"直角邊 HP_on^2 (距離 d2^2): {d2_sq:.3f}")
    
    # 斜邊: P_out 到 P_on 的距離平方 (d3^2)
    d3_sq = p_out.distance_to(p_on)**2
    print(f"斜邊 P_outP_on^2 (距離 d3^2): {d3_sq:.3f}")

    # 步驟 5: 驗證
    sum_of_squares = d1_sq + d2_sq
    
    # 使用 EPSILON 容忍度進行浮點數比較
    if abs(sum_of_squares - d3_sq) < EPSILON:
        print(f"\n驗證成功: {sum_of_squares:.3f} (d1^2+d2^2) ≈ {d3_sq:.3f} (d3^2)")
        return True
    else:
        print(f"\n驗證失敗: {sum_of_squares:.3f} (d1^2+d2^2) ≠ {d3_sq:.3f} (d3^2)")
        return False


# --- 範例測試 ---
if __name__ == "__main__":
    
    # 範例點
    P_a = Point(0, 0)
    P_b = Point(2, 4)
    P_c = Point(5, 0)

    # 範例直線
    L_1 = Line(1, 1, -4)  # x + y - 4 = 0
    L_2 = Line(2, -1, 1)  # 2x - y + 1 = 0
    L_3_parallel = Line(1, 1, 10) # x + y + 10 = 0
    L_4_from_points = Line.from_points(Point(1, 1), Point(3, 5)) # 4x - 2y - 2 = 0

    # 範例圓
    C_1 = Circle(Point(0, 0), 5)    # 圓心 (0, 0), 半徑 5
    C_2 = Circle(Point(7, 0), 4)    # 圓心 (7, 0), 半徑 4
    C_3_intersect = Circle(Point(4, 0), 3) # 圓心 (4, 0), 半徑 3 (與 C1 相切)
    
    
    ## 1. 兩直線交點測試
    print("================== 1. 兩直線交點 ==================")
    status_1, intersection_1 = intersect_two_lines(L_1, L_2)
    print(f"L1: {L_1} 與 L2: {L_2}")
    print(f" -> 狀態: {status_1}, 交點: {intersection_1}")
    # 預期交點 (1, 3)

    status_2, intersection_2 = intersect_two_lines(L_1, L_3_parallel)
    print(f"L1: {L_1} 與 L3: {L_3_parallel}")
    print(f" -> 狀態: {status_2}, 交點: {intersection_2}")
    # 預期平行

    ## 2. 兩圓交點測試
    print("\n================== 2. 兩圓交點 ==================")
    status_3, intersections_3 = intersect_two_circles(C_1, C_2)
    print(f"C1: {C_1} 與 C2: {C_2}")
    print(f" -> 狀態: {status_3}, 交點: {intersections_3}")
    # 預期不相交 (距離 7 > 5+4=9) -> 修正: 距離 7 < 5+4=9，應為兩點相交

    status_4, intersections_4 = intersect_two_circles(C_1, C_3_intersect)
    print(f"C1: {C_1} 與 C3: {C_3_intersect}")
    print(f" -> 狀態: {status_4}, 交點: {intersections_4}")
    # 預期相切 (距離 4 = 5-3=2 (內切) 或 5+3=8 (外切)) -> 距離 4，r1-r2=2, r1+r2=8。兩點相交

    ## 3. 直線與圓交點測試
    print("\n================== 3. 直線與圓交點 ==================")
    # 直線 L_5: y=3 (0x + 1y - 3 = 0)
    L_5 = Line(0, 1, -3)
    print(f"L5: {L_5} 與 C1: {C_1}")
    status_5, intersections_5 = intersect_line_circle(L_5, C_1)
    print(f" -> 狀態: {status_5}, 交點: {intersections_5}")
    # 預期交於兩點 (y=3, x^2=16, x=+-4)

    # 直線 L_6: x=5 (1x + 0y - 5 = 0)
    L_6 = Line(1, 0, -5)
    print(f"L6: {L_6} 與 C1: {C_1}")
    status_6, intersections_6 = intersect_line_circle(L_6, C_1)
    print(f" -> 狀態: {status_6}, 交點: {intersections_6}")
    # 預期相切 (x=5)

    ## 4. 垂直線測試
    print("\n================== 4. 垂直線 ==================")
    L_7 = Line(3, 4, -12) # 3x + 4y - 12 = 0
    P_out_7 = Point(10, 5)
    L_perp_7 = perpendicular_line_from_point(L_7, P_out_7)
    print(f"原直線 L7: {L_7}")
    print(f"線外一點 P_out_7: {P_out_7}")
    print(f"垂直線 L_perp_7: {L_perp_7}")
    # 預期垂直線: 4x - 3y - D = 0。 代入 (10, 5) -> 40 - 15 = 25。 L_perp: 4x - 3y - 25 = 0

    ## 5. 畢氏定理驗證
    L_pyth = Line(1, -1, 0) # x - y = 0
    P_out_pyth = Point(5, 1)
    verify_pythagorean_theorem(L_pyth, P_out_pyth) 
    # 預期結果: 垂足 H (3, 3)。P_outH = sqrt(8)。P_on (0, 0)。HP_on = sqrt(18)。P_outP_on = sqrt(26)。
    # 8 + 18 = 26 (驗證成功)