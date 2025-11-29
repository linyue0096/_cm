import tkinter as tk
import math
from tkinter import ttk 

class TransformableTriangleApp:
    def __init__(self, master):
        self.master = master
        master.title("藍色三角形變換器")

        # --- 設定畫布 ---
        self.canvas_width = 500
        self.canvas_height = 500
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(pady=10, padx=10)
        
        # --- 初始三角形設定 ---
        # 初始頂點座標 (以元組 (x, y) 形式儲存)
        p1 = (250, 100)
        p2 = (100, 350)
        p3 = (400, 350)
        
        # 原始座標用於重置
        self.original_points = [p1, p2, p3]
        # 當前座標用於變換
        self.current_points = list(self.original_points)
        
        # 繪製初始三角形，並取得它的 ID
        self.triangle_id = self._draw_triangle()
        
        # --- 設定控制按鈕 ---
        self._setup_controls()
        
        # 初始計算幾何中心 (用於旋轉和縮放)
        self._recalculate_center()

    def _setup_controls(self):
        """建立並放置控制按鈕"""
        frame = ttk.Frame(self.master)
        frame.pack(pady=10)

        # 旋轉按鈕
        ttk.Button(frame, text="🔄 旋轉 (15°)", command=self.rotate_triangle).pack(side=tk.LEFT, padx=5)
        
        # 縮放按鈕
        ttk.Button(frame, text="🔍 縮放 (x 1.2)", command=self.scale_triangle).pack(side=tk.LEFT, padx=5)
        
        # 平移按鈕
        ttk.Button(frame, text="➡️ 平移 (右/下 20)", command=self.translate_triangle).pack(side=tk.LEFT, padx=5)
        
        # 重設按鈕
        ttk.Button(frame, text="⟲ 重設", command=self.reset_triangle).pack(side=tk.LEFT, padx=15)

    def _get_coords_flat(self):
        """將 [(x1, y1), (x2, y2), ...] 轉換成 [x1, y1, x2, y2, ...]"""
        return [c for p in self.current_points for c in p]

    def _recalculate_center(self):
        """計算並更新當前三角形的幾何中心點 (用於變換基準)"""
        num_points = len(self.current_points)
        self.center_x = sum(p[0] for p in self.current_points) / num_points
        self.center_y = sum(p[1] for p in self.current_points) / num_points

    def _draw_triangle(self):
        """首次繪製三角形"""
        coords = self._get_coords_flat()
        return self.canvas.create_polygon(
            coords, 
            fill="blue", 
            outline="darkblue", 
            width=2
        )

    def _update_triangle(self):
        """用新的座標更新畫布上的三角形"""
        # 獲取新的扁平座標列表
        coords = self._get_coords_flat()
        
        # 關鍵修正點：使用 self.canvas.coords() 方法來直接設置新的座標
        self.canvas.coords(self.triangle_id, *coords) 
        # 注意：我們使用 *coords 將列表解包成單獨的參數
        
        self._recalculate_center() # 每次變換後更新中心點   
    # --- 1. 平移 (Translation) ---
    def translate_triangle(self, dx=20, dy=20):
        """將三角形向右和向下平移指定的距離"""
        new_points = []
        for x, y in self.current_points:
            new_points.append((x + dx, y + dy))
            
        self.current_points = new_points
        self._update_triangle()


    # --- 2. 縮放 (Scaling) ---
    def scale_triangle(self, factor=1.2):
        """以幾何中心點為基準，縮放三角形"""
        cx, cy = self.center_x, self.center_y
        new_points = []
        
        for x, y in self.current_points:
            # 1. 移至原點, 2. 縮放, 3. 移回中心
            new_x = cx + factor * (x - cx)
            new_y = cy + factor * (y - cy)
            new_points.append((new_x, new_y))
            
        self.current_points = new_points
        self._update_triangle()


    # --- 3. 旋轉 (Rotation) ---
    def rotate_triangle(self, angle_deg=15):
        """以幾何中心點為基準，順時針旋轉指定的角度"""
        
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        cx, cy = self.center_x, self.center_y
        new_points = []

        for x, y in self.current_points:
            # 相對於中心點的座標
            x_rel = x - cx
            y_rel = y - cy
            
            # 執行旋轉公式 (二維旋轉)
            # x' = x_rel * cos(a) - y_rel * sin(a)
            # y' = x_rel * sin(a) + y_rel * cos(a)
            rotated_x_rel = x_rel * cos_a - y_rel * sin_a
            rotated_y_rel = x_rel * sin_a + y_rel * cos_a
            
            # 移回中心點的位置
            new_x = rotated_x_rel + cx
            new_y = rotated_y_rel + cy
            new_points.append((new_x, new_y))

        self.current_points = new_points
        self._update_triangle()

    # --- 重設 ---
    def reset_triangle(self):
        """將三角形恢復到初始狀態"""
        # 複製原始座標列表
        self.current_points = list(self.original_points)
        self._update_triangle()

# --- 啟動應用程式 ---
def create_blue_triangle():
    root = tk.Tk()
    app = TransformableTriangleApp(root)
    root.mainloop()

if __name__ == "__main__":
    create_blue_triangle()