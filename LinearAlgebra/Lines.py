from __future__ import annotations

from math import sqrt

Point = tuple[float, float]


class Line2D:
    def __init__(self, a: float, b: float, c: float) -> None:
        self.__a, self.__b, self.__c = float(a), float(b), float(c)

        if not (self.a or self.b):
            raise ValueError("Impossible line" if self.c else "Useless line")

        if self.a:
            self.__a, self.__b, self.__c = 1, self.b / self.a, self.c / self.a

        else:
            self.__a, self.__b, self.__c = self.a / self.b, 1, self.c / self.b

    @property
    def a(self) -> float:
        return self.__a

    @property
    def b(self) -> float:
        return self.__b

    @property
    def c(self) -> float:
        return self.__c

    def copy(self) -> Line2D:
        return Line2D(self.a, self.b, self.c)

    @classmethod
    def from_points(cls, p0: Point, p1: Point) -> Line2D:
        return cls(p0[1] - p1[1], p1[0] - p0[0], p0[0] * p1[1] - p1[0] * p0[1])

    def perpendicular(self, c: float = None, a_neg: bool = False) -> Line2D:
        if c is None:
            c = self.c

        a, b = (-self.b, self.a) if a_neg else (self.b, -self.a)

        return Line2D(a, b, float(c))

    def parallel(self, other: Line2D) -> bool:
        if not isinstance(other, Line2D):
            return False

        return self.a * other.b == other.a * self.b

    def find_x(self, y: float = 0) -> float:
        try:
            return -(self.b * y + self.c) / self.a

        except ZeroDivisionError:
            return float("inf")

    def find_y(self, x: float = 0) -> float:
        try:
            return -(self.a * x + self.c) / self.b

        except ZeroDivisionError:
            return float("inf")

    def slope_y_as_f_x(self) -> Point:
        if not self.b:
            return float("inf"), -self.c / self.a

        return -self.a / self.b, -self.c / self.b

    def slope_x_as_f_y(self) -> Point:
        if not self.a:
            return float("inf"), -self.c / self.b

        return -self.b / self.a, -self.c / self.a

    def intersection(self, other: Line2D) -> Point:
        if self.parallel(other):
            return float("inf"), float("inf")

        if self.a:
            y = (other.a * self.c - self.a * other.c) / (self.a * other.b - other.a * self.b)
            x = -(self.b * y + self.c) / self.a

        else:
            x = Line2D(other.a, other.b, other.c - self.c / self.b).find_x()
            y = other.find_y(x)

        return x, y

    def distance(self, point: Point) -> float:
        return abs(self(point)) / sqrt(self.a ** 2 + self.b ** 2)

    def same_side(self, p0: Point, p1: Point) -> bool:
        return self(p0) * self(p1) > 0

    def __hash__(self) -> int:
        return hash((self.a, self.b, self.c))

    def __call__(self, point: Point) -> float:
        return self.a * point[0] + self.b * point[1] + self.c

    def __contains__(self, item: Point) -> bool:
        return not (self.a * item[0] + self.b * item[1] + self.c)

    def __eq__(self, other: Line2D) -> bool:
        if type(other) is not Line2D:
            return False

        return (self.a, self.b, self.c) == (other.a, other.b, other.c)

    def __str__(self) -> str:
        b_sign, c_sign = "+-"[self.b < 0], "+-"[self.c < 0]
        a = "x" if self.a else ""
        b = "" if abs(self.b) == 1 else str(abs(self.b))

        return f"{a} {b_sign} {b}y {c_sign} {abs(self.c)} = 0"

    def __repr__(self) -> str:
        return f"Line2D({self.a}, {self.b}, {self.c})"
