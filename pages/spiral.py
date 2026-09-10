"""Logarithmic nautilus + the golden-ratio construction from the company logo."""

import math

PHI = (1 + math.sqrt(5)) / 2


def generate_spiral_path(
    center_x: float,
    center_y: float,
    start_radius: float,
    turns: float,
    growth_rate: float,
    points_per_turn: int = 100,
) -> str:
    total_points = int(turns * points_per_turn)
    parts = []
    for i in range(total_points + 1):
        theta = (i / points_per_turn) * 2 * math.pi
        r = start_radius * math.exp(growth_rate * theta)
        x = center_x + r * math.cos(theta)
        y = center_y + r * math.sin(theta)
        cmd = "M" if i == 0 else "L"
        parts.append(f"{cmd} {x:.2f} {y:.2f}")
    return " ".join(parts)


def generate_chamber_path(
    center_x: float,
    center_y: float,
    start_radius: float,
    growth_rate: float,
    angle_offset: float,
) -> str:
    inner_r = start_radius * math.exp(growth_rate * angle_offset)
    outer_r = start_radius * math.exp(growth_rate * (angle_offset + 2 * math.pi))
    inner_x = center_x + inner_r * math.cos(angle_offset)
    inner_y = center_y + inner_r * math.sin(angle_offset)
    outer_x = center_x + outer_r * math.cos(angle_offset)
    outer_y = center_y + outer_r * math.sin(angle_offset)
    mid_r = (inner_r + outer_r) / 2
    mid_angle = angle_offset + 0.15
    ctrl_x = center_x + mid_r * math.cos(mid_angle)
    ctrl_y = center_y + mid_r * math.sin(mid_angle)
    return (
        f"M {inner_x:.2f} {inner_y:.2f} "
        f"Q {ctrl_x:.2f} {ctrl_y:.2f} {outer_x:.2f} {outer_y:.2f}"
    )


def _quarter_arc(x: float, y: float, side: float, orientation: int) -> str:
    """Clockwise quarter-circle inside a Fibonacci square (logo construction)."""
    r = side
    k = orientation % 4
    if k == 0:  # square on the left — arc BL → TR around BR
        start, end, cx, cy = (x, y + side), (x + side, y), x + side, y + side
    elif k == 1:  # square on the top — arc TL → BR around BL
        start, end, cx, cy = (x, y), (x + side, y + side), x, y + side
    elif k == 2:  # square on the right — arc TR → BL around TL
        start, end, cx, cy = (x + side, y), (x, y + side), x, y
    else:  # square on the bottom — arc BR → TL around TR
        start, end, cx, cy = (x + side, y + side), (x, y), x + side, y
    return (
        f"M {start[0]:.2f} {start[1]:.2f} "
        f"A {r:.2f} {r:.2f} 0 0 1 {end[0]:.2f} {end[1]:.2f}"
    )


def golden_construction(view: float = 600, margin: float = 78, depth: int = 8) -> dict:
    """Fibonacci tiling that matches the Black Shell logo geometry.

    Largest square on the left (θ), remaining golden rectangle on the right
    (φ = √5/2), nested squares winding clockwise into a plus at the core.
    """
    # Golden rectangle fitted inside the viewBox.
    width = view - 2 * margin
    height = width / PHI
    x = (view - width) / 2
    y = (view - height) / 2

    squares: list[dict] = []
    arcs: list[str] = []
    orientation = 0
    rx, ry, rw, rh = x, y, width, height

    for i in range(depth):
        if min(rw, rh) < 8:
            break
        if orientation % 2 == 0:
            side = rh
            if orientation % 4 == 0:  # left
                sx, sy = rx, ry
                nx, ny, nw, nh = rx + side, ry, rw - side, rh
            else:  # right
                sx, sy = rx + rw - side, ry
                nx, ny, nw, nh = rx, ry, rw - side, rh
        else:
            side = rw
            if orientation % 4 == 1:  # top
                sx, sy = rx, ry
                nx, ny, nw, nh = rx, ry + side, rw, rh - side
            else:  # bottom
                sx, sy = rx, ry + rh - side
                nx, ny, nw, nh = rx, ry, rw, rh - side
        squares.append({"x": round(sx, 2), "y": round(sy, 2), "s": round(side, 2)})
        arcs.append(_quarter_arc(sx, sy, side, orientation))
        rx, ry, rw, rh = nx, ny, nw, nh
        orientation += 1

    large = squares[0]
    second = squares[1] if len(squares) > 1 else large
    inner = squares[-1]

    # θ sits in the large left square; φ formula in the top-right square;
    # 9 hangs on the outer arc where the logo places it.
    glyphs = [
        {
            "char": "θ",
            "x": round(large["x"] + large["s"] * 0.42, 2),
            "y": round(large["y"] + large["s"] * 0.42, 2),
            "size": 28,
            "delay": "0s",
        },
        {
            "char": "9",
            "x": round(large["x"] + large["s"] * 0.08, 2),
            "y": round(large["y"] + large["s"] * 0.92, 2),
            "size": 18,
            "delay": "1.2s",
        },
    ]

    formula = {
        "x": round(second["x"] + second["s"] * 0.50, 2),
        "y": round(second["y"] + second["s"] * 0.46, 2),
    }

    plus = {
        "cx": round(inner["x"] + inner["s"] / 2, 2),
        "cy": round(inner["y"] + inner["s"] / 2, 2),
        "arm": round(max(inner["s"] * 0.28, 4), 2),
    }

    # Tiny symbols riding a ring just inside the compass bezel.
    ring = []
    symbols = ["θ", "φ", "√5", "9", "θ", "φ", "√5", "9"]
    for i, ch in enumerate(symbols):
        ang = (i / len(symbols)) * 2 * math.pi - math.pi / 2
        ring.append(
            {
                "char": ch,
                "x": round(300 + 248 * math.cos(ang), 2),
                "y": round(300 + 248 * math.sin(ang), 2),
                "delay": f"{i * 0.35}s",
            }
        )

    return {
        "squares": squares,
        "arcs": arcs,
        "glyphs": glyphs,
        "formula": formula,
        "plus": plus,
        "ring": ring,
        "rect": {
            "x": round(x, 2),
            "y": round(y, 2),
            "w": round(width, 2),
            "h": round(height, 2),
        },
    }
