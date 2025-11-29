import math
from typing import List, Tuple, Union, Optional

class Geometry:
    """處理二維幾何計算的工具類別"""

    @staticmethod
    def line_intersection(l1: Tuple[float, float, float], 
                          l2: Tuple[float, float, float]) -> Optional[Tuple[float, float]]:
        """
        計算兩直線的交點。
        直線 L: (A, B, C) 代表 Ax + By + C = 0
        """
        A1, B1, C1 = l1
        A2, B2, C2 = l2

        # 矩陣行列式
        D = A1 * B2 - A2 * B1
        Dx = B1 * C2 - B2 * C1
        Dy = A2 * C1 - A1 * C2

        if abs(D) < 1e-9: # 行列式接近 0，表示平行或重合
            # 檢查是否重合 (如果 A1/A2 = B1/B2 = C1/C2)
            if abs(Dx) < 1e-9 and abs(Dy) < 1e-9:
                # 數學上視為無數交點，程式中返回 None
                # print("兩直線重合，無數交點")
                return None 
            else:
                # print("兩直線平行，無交點")
                return None
        else:
            x = Dx / D
            y = Dy / D
            return (x, y)

    @staticmethod
    def circle_line_intersection(circle: Tuple[float, float, float], 
                                 line: Tuple[float, float, float]) -> List[Tuple[float, float]]:
        """
        計算直線與圓的交點。
        圓 C: (h, k, r) 代表 (x-h)^2 + (y-k)^2 = r^2
        直線 L: (A, B, C) 代表 Ax + By + C = 0
        """
        h, k, r = circle
        A, B, C = line
        
        # 1. 將圓心移至原點，並調整直線 C: A*x + B*y + (C + A*h + B*k) = 0
        C_prime = C + A * h + B * k

        intersections = []
        
        if abs(B) < 1e-9: # 垂直線 A*x + C_prime = 0
            # x = -C_prime / A
            x = -C_prime / A
            delta_y_sq = r**2 - x**2
            
            if delta_y_sq < -1e-9:
                return []
            elif delta_y_sq < 1e-9: # 相切
                intersections.append((x + h, k))
            else:
                delta_y = math.sqrt(delta_y_sq)
                intersections.append((x + h, k + delta_y))
                intersections.append((x + h, k - delta_y))
                
        elif abs(A) < 1e-9: # 水平線 B*y + C_prime = 0
            # y = -C_prime / B
            y = -C_prime / B
            delta_x_sq = r**2 - y**2
            
            if delta_x_sq < -1e-9:
                return []
            elif delta_x_sq < 1e-9: # 相切
                intersections.append((h, y + k))
            else:
                delta_x = math.sqrt(delta_x_sq)
                intersections.append((h + delta_x, y + k))
                intersections.append((h - delta_x, y + k))

        else: # 一般斜線 y = m*x + b_prime
            # L: y = (-A/B)x + (-C_prime/B)
            # 圓: x^2 + y^2 = r^2
            # a*x^2 + b*x + c = 0
            
            # 讓 y = m*x + b'
            m = -A / B
            b_prime = -C_prime / B
            
            a = m**2 + 1
            b = 2 * m * b_prime
            c = b_prime**2 - r**2
            
            # 判別式
            delta = b**2 - 4 * a * c
            
            if delta < -1e-9: # 無交點
                return []
            elif delta < 1e-9: # 相切 (一個交點)
                x = -b / (2 * a)
                y = m * x + b_prime
                intersections.append((x + h, y + k))
            else: # 兩個交點
                sqrt_delta = math.sqrt(delta)
                x1 = (-b + sqrt_delta) / (2 * a)
                y1 = m * x1 + b_prime
                
                x2 = (-b - sqrt_delta) / (2 * a)
                y2 = m * x2 + b_prime
                
                intersections.append((x1 + h, y1 + k))
                intersections.append((x2 + h, y2 + k))

        return intersections

    @staticmethod
    def circle_intersection(c1: Tuple[float, float, float], 
                            c2: Tuple[float, float, float]) -> List[Tuple[float, float]]:
        """
        計算兩圓的交點。
        圓 C: (h, k, r) 代表 (x-h)^2 + (y-k)^2 = r^2
        """
        h1, k1, r1 = c1
        h2, k2, r2 = c2

        # 1. 取得兩圓公共弦 (Common Chord) 的直線方程式 A x + B y + C = 0
        # (x^2 - 2h1*x + h1^2 + y^2 - 2k1*y + k1^2) - r1^2 = 0
        # (x^2 - 2h2*x + h2^2 + y^2 - 2k2*y + k2^2) - r2^2 = 0
        
        # 相減後得到:
        # (-2h1 + 2h2)x + (-2k1 + 2k2)y + (h1^2 - h2^2 + k1^2 - k2^2 + r2^2 - r1^2) = 0
        
        A = 2 * (h2 - h1)
        B = 2 * (k2 - k1)
        C = h1**2 - h2**2 + k1**2 - k2**2 + r2**2 - r1**2
        
        # 如果 A=0 且 B=0，表示圓心相同。
        if abs(A) < 1e-9 and abs(B) < 1e-9:
            if abs(r1 - r2) < 1e-9:
                # print("兩圓重合，無數交點")
                return [] # 程式中返回空列表
            else:
                # print("同心圓，無交點")
                return []

        # 2. 將問題轉化為 直線與圓 C1 的交點問題
        line = (A, B, C)
        intersections = Geometry.circle_line_intersection(c1, line)
        
        return intersections