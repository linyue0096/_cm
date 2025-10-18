import math

EPSILON = 1e-9
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x:.3f}, {self.y:.3f})"

class Triangle:
    def __init__(self, A: Point, B: Point, C: Point):
        self.A = A
        self.B = B
        self.C = C
    def __repr__(self):
        return f"Triangle: {self.A}, {self.B}, {self.C}"

def line_line_intersection(A1, B1, C1, A2, B2, C2):
    D = A1 * B2 - A2 * B1
    if abs(D) < EPSILON:
        if abs(A1 * C2 - A2 * C1) < EPSILON and abs(B1 * C2 - B2 * C1) < EPSILON:
            return "Coincident", None
        else:
            return "Parallel", None
    else:
        x = (B1 * C2 - B2 * C1) / D
        y = (A2 * C1 - A1 * C2) / D
        return "Intersect", Point(x, y)

def line_circle_intersection(h, k, r, A, B, C):
    if abs(B) < EPSILON:
        if abs(A) < EPSILON:
            return "Error", None
        x_line = -C / A
        d = abs(x_line - h)
        if d > r + EPSILON:
            return "Separate", []
        y_half = math.sqrt(r**2 - d**2)
        if d >= r - EPSILON:
            return "Tangent", [Point(x_line, k)]
        else:
            return "Intersect", [Point(x_line, k + y_half), Point(x_line, k - y_half)]
    
    dist_sq = A**2 + B**2
    d = abs(A * h + B * k + C) / math.sqrt(dist_sq)

    if d > r + EPSILON:
        return "Separate", []
    elif d >= r - EPSILON:
        t = -(A * h + B * k + C) / dist_sq
        x0 = h + A * t
        y0 = k + B * t
        return "Tangent", [Point(x0, y0)]
    else:
        t = -(A * h + B * k + C) / dist_sq
        x0 = h + A * t
        y0 = k + B * t
        L_half = math.sqrt(r**2 - d**2)
        mag = math.sqrt(dist_sq)
        u_x = -B / mag
        u_y = A / mag
        p1 = Point(x0 + L_half * u_x, y0 + L_half * u_y)
        p2 = Point(x0 - L_half * u_x, y0 - L_half * u_y)
        return "Intersect", [p1, p2]

def circle_circle_intersection(h1, k1, r1, h2, k2, r2):
    d = math.hypot(h1 - h2, k1 - k2)

    if d < EPSILON and abs(r1 - r2) < EPSILON:
        return "Coincident", None
    elif d < EPSILON:
        return "Separate", []

    if d > r1 + r2 + EPSILON or d < abs(r1 - r2) - EPSILON:
        return "Separate", []

    A = 2 * (h2 - h1)
    B = 2 * (k2 - k1)
    C = h1**2 + k1**2 - r1**2 - h2**2 - k2**2 + r2**2

    status, points = line_circle_intersection(h1, k1, r1, A, B, C)

    if d >= r1 + r2 - EPSILON or abs(d - abs(r1 - r2)) < EPSILON:
        return "Tangent", points
    return status, points

def perpendicular_line_and_projection(A, B, C, xp, yp):
    if abs(A) < EPSILON and abs(B) < EPSILON:
        return "Error", "Invalid Line (A=B=0)", None

    A_perp = B
    B_perp = -A
    C_perp = A * yp - B * xp

    D = -(A**2 + B**2)
    D_x = A * C - B**2 * xp + A * B * yp
    D_y = A * B * xp - A**2 * yp + B * C

    x0 = D_x / D
    y0 = D_y / D

    return "Success", (A_perp, B_perp, C_perp), Point(x0, y0)

def distance(p1: Point, p2: Point) -> float:
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def verify_pythagorean(a: Point, b: Point, c: Point) -> bool:
    ab = distance(a, b)
    bc = distance(b, c)
    ac = distance(a, c)
    return math.isclose(ab**2 + bc**2, ac**2, rel_tol=1e-6)

def translate(p: Point, dx: float, dy: float) -> Point:
    return Point(p.x + dx, p.y + dy)

def scale(p: Point, center: Point, factor: float) -> Point:
    return Point(center.x + (p.x - center.x) * factor,
                 center.y + (p.y - center.y) * factor)

def rotate(p: Point, center: Point, angle_deg: float) -> Point:
    angle_rad = math.radians(angle_deg)
    x_shifted = p.x - center.x
    y_shifted = p.y - center.y
    x_new = x_shifted * math.cos(angle_rad) - y_shifted * math.sin(angle_rad)
    y_new = x_shifted * math.sin(angle_rad) + y_shifted * math.cos(angle_rad)
    return Point(center.x + x_new, center.y + y_new)

