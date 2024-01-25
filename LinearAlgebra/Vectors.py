from math import asin, acos, sqrt
class Vector2D:
    def __init__(self, x: int | float = 0.0, y: int | float = 0.0):
        self.__x, self.__y = x, y
    def x(self):
        return self.__x
    def y(self):
        return self.__y
    def polar(self):
        if not self:
            return 0, 0
        radius = abs(self)
        return radius, asin(self.__y / radius)
    def copy(self):
        return Vector2D(self.__x, self.__y)
    def dot_product(self, other):
        if isinstance(other, Vector2D):
            return self.__x * other.__x + self.__y * other.__y
        raise TypeError('Another vector expected!')
    def parallel(self, other):
        if isinstance(other, Vector2D):
            if isinstance(other, Vector3D):
                if other.z():
                    return False
            return self.__x * other.__y == other.__x * self.__y
        raise TypeError('Vector expected!')
    def perpendicular(self, other):
        if isinstance(other, Vector2D):
            return not self.dot_product(other)
        raise TypeError('Another vector expected!')
    def mixed_product(self, v1, v2):
        if isinstance(v1, Vector2D):
            if isinstance(v1, Vector3D):
                if isinstance(v2, Vector3D):
                    return v2.z() * (self.__x * v1.y() - self.__y * v1.x()) + v1.z() * (self.__y * v2.x() - self.__x * v2.y())
                if isinstance(v2, Vector2D):
                    return v1.z() * (self.__y * v2.__x - self.__x * v2.__y)
                raise TypeError('Two vectors expected!')
            if isinstance(v2, Vector3D):
                return v2.z() * (self.__x * v1.__y - self.__y * v1.__x)
            if isinstance(v2, Vector2D):
                return 0
            raise TypeError('Two vectors expected!')
        raise TypeError('Two vectors expected!')
    def __bool__(self):
        return bool(abs(self))
    def __neg__(self):
        return Vector2D(-self.__x, -self.__y)
    def __abs__(self):
        return sqrt(self.__x ** 2 + self.__y ** 2)
    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.__x + other.x(), self.__y + other.y(), other.z())
        if isinstance(other, Vector2D):
            return Vector2D(self.__x + other.__x, self.__y + other.__y)
        raise TypeError('Another vector expected!')
    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return self + -other
        raise TypeError('Subtraction only defined between vectors!')
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2D(self.__x * other, self.__y * other)
        if isinstance(other, Vector3D):
            return Vector3D(self.__y * other.z(), -self.__x * other.z(), self.__x * other.y() - self.__y * other.x())
        if isinstance(other, Vector2D):
            return Vector3D(0, 0, self.__x * other.__y - self.__y * other.__x)
        raise TypeError(f'Unsupported type: {type(other)}!')
    def __rmul__(self, other):
        res = self * other
        if isinstance(other, Vector2D):
            res *= -1
        return res
    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.__x / other, self.__y / other)
        raise TypeError('Vector division only defined for real numbers!')
    def __eq__(self, other):
        if isinstance(other, Vector3D):
            return (self.__x, self.__y, 0) == (other.x(), other.y(), other.z())
        if isinstance(other, Vector2D):
            return (self.__x, self.__y) == (other.__x, other.__y)
        return (self.__x, self.__y) == other or (self.__x, self.__y, 0) == other
    def __str__(self):
        return f'V({self.__x}, {self.__y})'
    def __repr__(self):
        return str(self)
class Vector3D(Vector2D):
    def __init__(self, x: int | float = 0.0, y: int | float = 0.0, z: int | float = 0.0):
        super().__init__(x, y)
        self.__z = z
    def z(self):
        return self.__z
    def polar(self):
        if not self:
            return 0, 0, 0
        cos_a = self.x() / sqrt(self.x() ** 2 + self.y() ** 2)
        cos_b = self.x() / sqrt(self.x() ** 2 + self.__z ** 2)
        a1, a2 = asin(self.y() / sqrt(self.x() ** 2 + self.y() ** 2)), acos(cos_a)
        b1, b2 = asin(self.__z / sqrt(self.x() ** 2 + self.__z ** 2)), acos(cos_b)
        if cos_a >= 0:
            a = a1
        else:
            a = (-1) ** (a1 < 0) * a2
        if cos_b >= 0:
            b = b1
        else:
            b = (-1) ** (b1 < 0) * b2
        return abs(self), a, b
    def copy(self):
        return Vector3D(self.x(), self.y(), self.__z)
    def dot_product(self, other):
        if isinstance(other, Vector3D):
            return self.x() * other.x() + self.y() * other.y() + self.__z * other.__z
        if isinstance(other, Vector2D):
            return super().dot_product(other)
        raise TypeError('Another vector expected!')
    def parallel(self, other):
        if isinstance(other, Vector2D):
            if not self.__z:
                return self.x() * other.y() == other.x() * self.y()
            if isinstance(other, Vector3D):
                return self.x() * other.y() == other.x() * self.y() and self.x() * other.__z == other.x() * self.__z and self.y() * other.__z == other.y() * self.__z
            return False
        raise TypeError('Vector expected!')
    def mixed_product(self, v1: Vector2D, v2: Vector2D):
        if isinstance(v1, Vector3D):
            if isinstance(v2, Vector3D):
                return (self.x() * v1.y() - self.y() * v1.x()) * v2.__z + (self.__z * v1.x() - self.x() * v1.__z) * v2.y() + (self.y() * v1.__z - self.__z * v1.y()) * v2.x()
            return (self.__z * v1.x() - self.x() * v1.__z) * v2.y() + (self.y() * v1.__z - self.__z * v1.y()) * v2.x()
        if isinstance(v2, Vector3D):
            return (self.x() * v1.y() - self.y() * v1.x()) * v2.__z + self.__z * (v1.x() * v2.y() - v1.y() * v2.x())
        return self.__z * (v1.x() * v2.y() - v1.y() * v2.x())
    def __neg__(self):
        return Vector3D(-self.x(), -self.y(), -self.__z)
    def __abs__(self):
        return sqrt(self.x() ** 2 + self.y() ** 2 + self.__z ** 2)
    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.x() + other.x(), self.y() + other.y(), self.__z + other.__z)
        if isinstance(other, Vector2D):
            return Vector3D(self.x() + other.x(), self.y() + other.y(), self.__z)
        raise TypeError('Another vector expected!')
    def __sub__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.x() - other.x(), self.y() - other.y(), self.__z - other.__z)
        if isinstance(other, Vector2D):
            return Vector3D(self.x() - other.x(), self.y() - other.y(), self.__z)
        raise TypeError('Subtraction only defined between vectors!')
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector3D(self.x() * other, self.y() * other, self.__z * other)
        if isinstance(other, Vector3D):
            return Vector3D(self.y() * other.__z - self.__z * other.y(), self.__z * other.x() - self.x() * other.__z, self.x() * other.y() - self.y() * other.x())
        if isinstance(other, Vector2D):
            return Vector3D(-self.__z * other.y(), self.__z * other.x(), self.x() * other.y() - self.y() * other.x())
        raise TypeError('A real number or another vector expected!')
    def __rmul__(self, other):
        return self * other
    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector3D(self.x() / other, self.y() / other, self.__z / other)
        raise TypeError('Vector division only defined for real numbers!')
    def __eq__(self, other):
        if isinstance(other, Vector3D):
            return (self.x(), self.y(), self.__z) == (other.x(), other.y(), other.__z)
        if isinstance(other, Vector2D):
            return (self.x(), self.y(), self.__z) == (other.x(), other.y(), 0)
        return (self.x(), self.y(), self.z()) == other
    def __str__(self):
        return f'V({self.x()}, {self.y()}, {self.__z})'
