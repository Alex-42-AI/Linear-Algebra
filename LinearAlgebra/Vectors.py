from __future__ import annotations

from math import sin, cos, acos, atan2, sqrt

Point = tuple[float, float]


def clamp(x: float, lo: float = -1, hi: float = 1) -> float:
    return max(lo, min(x, hi))


class Vector2D:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.__x, self.__y = float(x), float(y)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    def polar(self) -> Point:
        if not self:
            return 0, 0

        return abs(self), atan2(self.y, self.x)

    @classmethod
    def polar_to_planar(cls, radius: float, angle: float) -> Vector2D:
        return cls(cos(angle), sin(angle)) * radius

    def copy(self) -> Vector2D:
        return Vector2D(self.x, self.y)

    def normalized(self) -> Vector2D:
        if self:
            r = abs(self)

            return Vector2D(self.x / r, self.y / r)

        return self.copy()

    def dot_product(self, other: Vector2D) -> float:
        if isinstance(other, Vector2D):
            return self.x * other.x + self.y * other.y

        raise TypeError("Another vector expected")

    def angle_with(self, other: Vector2D) -> float:
        if isinstance(other, Vector2D):
            if not (self and other):
                return 0

            return acos(clamp(self.dot_product(other) / (abs(self) * abs(other))))

        raise TypeError("Another vector expected")

    def projection(self, other: Vector2D) -> Vector2D:
        if isinstance(other, Vector2D):
            if not (self and other):
                return Vector2D()

            return self.dot_product(other) * other / abs(other) ** 2

        raise TypeError("Another vector expected")

    def rotated(self, theta: float) -> Vector2D:
        return Vector2D(self.x * cos(theta) - self.y * sin(theta), self.x * sin(theta) + self.y * cos(theta))

    def parallel(self, other: Vector2D) -> bool:
        if isinstance(other, Vector2D):
            if isinstance(other, Vector3D) and other.z:
                return False

            return self.x * other.y == other.x * self.y

        raise TypeError("Another vector expected")

    def perpendicular(self, other: Vector2D) -> bool:
        if isinstance(other, Vector2D):
            return not self.dot_product(other)

        return False

    def mixed_product(self, v1: Vector2D, v2: Vector2D) -> float:
        if isinstance(v1, Vector2D) and isinstance(v2, Vector2D):
            if not isinstance(v1, Vector3D):
                v1 = Vector3D(v1.x, v1.y, 0)

            if not isinstance(v2, Vector3D):
                v2 = Vector3D(v2.x, v2.y, 0)

            return v2.z * (self.x * v1.y - self.y * v1.x) + v1.z * (self.y * v2.x - self.x * v2.y)

        raise TypeError("Two vectors expected")

    def __bool__(self) -> bool:
        return bool(abs(self))

    def __neg__(self) -> Vector2D:
        return -1 * self

    def __abs__(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other: Vector2D) -> Vector2D:
        if isinstance(other, Vector3D):
            return other + self

        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)

        raise TypeError("Another vector expected")

    def __sub__(self, other: Vector2D) -> Vector2D:
        if isinstance(other, Vector2D):
            return self + -other

        raise TypeError("Another vector expected")

    def __mul__(self, other: float | Vector2D) -> Vector2D:
        if isinstance(other, (int, float)):
            return Vector2D(self.x * other, self.y * other)

        if isinstance(other, Vector2D):
            if not isinstance(other, Vector3D):
                other = Vector3D(other.x, other.y, 0)

            return Vector3D(self.y * other.z, -self.x * other.z, self.x * other.y - self.y * other.x)

        raise TypeError(f"A real number or another vector expected")

    def __rmul__(self, other: float | Vector2D) -> Vector2D:
        res = self * other

        if isinstance(other, Vector2D):
            res *= -1

        return res

    def __truediv__(self, other: float) -> Vector2D:
        if isinstance(other, (int, float)):
            return Vector2D(self.x / other, self.y / other)

        raise TypeError("Vector division with a number only defined for real numbers")

    def __eq__(self, other: Vector2D) -> bool:
        if type(other) == Vector2D:
            return (self.x, self.y) == (other.x, other.y)

        return False

    def __str__(self) -> str:
        return f'V({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"


class Vector3D(Vector2D):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        super().__init__(x, y)
        self.__z = float(z)

    @property
    def z(self) -> float:
        return self.__z

    def polar(self) -> tuple[float, float, float]:
        if not self:
            return 0, 0, 0

        r = abs(self)

        return r, atan2(self.y, self.x), acos(clamp(self.z / r))

    def polar_to_planar(self, radius: float, angle: float) -> None:
        raise NotImplementedError(
            "Vector2D.polar_to_planar is 2D-only — use Vector3D.from_spherical or Vector3D.from_cylindrical")

    @classmethod
    def polar_to_spherical(cls, r: float, theta: float, phi: float) -> Vector3D:
        return cls(r * sin(phi) * cos(theta), r * sin(phi) * sin(theta), r * cos(phi))

    def cylindrical(self) -> tuple[float, float, float]:
        return sqrt(self.x ** 2 + self.y ** 2), atan2(self.y, self.x), self.z

    @classmethod
    def cylindrical_to_spacial(cls, rho: float, theta: float, z: float) -> Vector3D:
        return cls(rho * cos(theta), rho * sin(theta), z)

    def copy(self) -> Vector3D:
        return Vector3D(self.x, self.y, self.z)

    def normalized(self) -> Vector3D:
        if self:
            r = abs(self)

            return Vector3D(self.x / r, self.y / r, self.z / r)

        return self.copy()

    def dot_product(self, other) -> float:
        if isinstance(other, Vector3D):
            return self.x * other.x + self.y * other.y + self.z * other.z

        if isinstance(other, Vector2D):
            return super().dot_product(other)

        raise TypeError("Another vector expected")

    def angle_with(self, other: Vector2D) -> float:
        return acos(clamp(self.dot_product(other) / (abs(self) * abs(other))))

    def projection(self, other: Vector3D) -> Vector3D:
        if not isinstance(other, Vector2D):
            raise TypeError("Another vector expected")

        if not isinstance(other, Vector3D):
            other = Vector3D(other.x, other.y, 0)

        if not (self and other):
            return Vector3D()

        return other * self.dot_product(other) / (abs(other) ** 2)

    def rotated(self, theta: float, phi: float) -> Vector3D:
        x = cos(theta) * self.x - sin(theta) * self.y

        return Vector3D(cos(phi) * x + sin(phi) * self.z, sin(theta) * self.x + cos(theta) * self.y,
                        cos(phi) * self.z - sin(phi) * x)

    def parallel(self, other) -> bool:
        if isinstance(other, Vector2D):
            if not self.z:
                return self.x * other.y == other.x * self.y

            if isinstance(other, Vector3D):
                return self.x * other.y == other.x * self.y and self.x * other.z == other.x * self.z and self.y * other.z == other.y * self.z

            return False

        raise TypeError("Another vector expected")

    def mixed_product(self, v1: Vector2D, v2: Vector2D) -> float:
        if isinstance(v1, Vector2D) and isinstance(v2, Vector2D):
            if not isinstance(v1, Vector3D):
                v1 = Vector3D(v1.x, v1.y, 0)

            if not isinstance(v2, Vector3D):
                v2 = Vector3D(v2.x, v2.y, 0)

            return (self.x * v1.y - self.y * v1.x) * v2.z + (self.z * v1.x - self.x * v1.z) * v2.y + (
                    self.y * v1.z - self.z * v1.y) * v2.x

        raise TypeError("Two vectors expected")

    def __abs__(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __add__(self, other) -> Vector3D:
        if isinstance(other, Vector3D):
            return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

        if isinstance(other, Vector2D):
            return Vector3D(self.x + other.x, self.y + other.y, self.z)

        raise TypeError("Another vector expected")

    def __mul__(self, other) -> Vector3D:
        if isinstance(other, (int, float)):
            return Vector3D(self.x * other, self.y * other, self.z * other)

        if isinstance(other, Vector3D):
            return Vector3D(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                            self.x * other.y - self.y * other.x)

        if isinstance(other, Vector2D):
            return Vector3D(-self.z * other.y, self.z * other.x, self.x * other.y - self.y * other.x)

        raise TypeError("A real number or another vector expected")

    def __rmul__(self, other) -> Vector3D:
        return self * other

    def __truediv__(self, other: float) -> Vector3D:
        if isinstance(other, (int, float)):
            return Vector3D(self.x / other, self.y / other, self.z / other)

        raise TypeError("Vector division only defined for real numbers")

    def __eq__(self, other: Vector3D) -> bool:
        if type(other) == Vector3D:
            return (self.x, self.y, self.z) == (other.x, other.y, other.z)

        return False

    def __str__(self) -> str:
        return f"V({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return f"Vector3D({self.x}, {self.y}, {self.z})"
