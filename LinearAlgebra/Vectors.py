from math import asin, sqrt
class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        if type(x) not in [int, float] or type(y) not in [int, float]:
            raise TypeError('Real numerical values expected!')
        self.__x, self.__y = x, y
    def x(self):
        return self.__x
    def y(self):
        return self.__y
    def polar(self):
        radius = abs(self)
        angle = asin(self.__y / radius)
        return radius, angle
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
        if isinstance(other, Vector3D):
            return Vector3D(self.__x - other.x(), self.__y - other.y(), -other.z())
        if isinstance(other, Vector2D):
            return Vector2D(self.__x - other.__x, self.__y - other.__y)
        raise TypeError('Subtraction only defined between vectors!')
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.__x * other, self.__y * other)
        if isinstance(other, Vector3D):
            return Vector3D(self.__y * other.z(), -self.__x - other.z(), self.__x * other.y() - self.__y * other.x())
        if isinstance(other, Vector2D):
            return Vector3D(0, 0, self.__x * other.__y - self.__y * other.__x)
        raise TypeError('A real number or another vector expected!')
    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.__x / other, self.__y / other)
        raise TypeError('Vector division only defined for real numbers!')
    def __eq__(self, other):
        if isinstance(other, Vector3D):
            return (self.__x, self.__y, 0) == (other.x(), other.y(), other.z())
        if isinstance(other, Vector2D):
            return (self.__x, self.__y) == (other.__x, other.__y)
        return (self.__x, self.__y) == other
    def __str__(self):
        return f'V({self.__x}, {self.__y})'
    def __repr__(self):
        return str(self)
class Vector3D(Vector2D):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y)
        if type(z) not in [int, float]:
            raise TypeError('Real numerical values expected!')
        self.__z = z
    def z(self):
        return self.__z
    def polar(self):
        radius = abs(self)
        angle_x_y, angle_x_z = asin(self.y() / sqrt(self.x() ** 2 + self.y() ** 2)), asin(self.__z / sqrt(self.x() ** 2 + self.__z ** 2))
        return radius, angle_x_y, angle_x_z
    def copy(self):
        return Vector3D(self.x(), self.y(), self.__z)
    def dot_product(self, other):
        if isinstance(other, Vector3D):
            return self.x() * other.x() + self.y() * other.y() + self.__z * other.__z
        if isinstance(other, Vector2D):
            return self.x() * other.x() + self.y() * other.y()
        raise TypeError('Another vector expected!')
    def parallel(self, other):
        if isinstance(other, Vector2D):
            if not self.__z:
                return self.x() * other.y() == other.x() * self.y()
            if isinstance(other, Vector3D):
                return self.x() * other.y() == other.x() * self.y() and self.x() * other.__z == other.x() * self.__z and self.y() * other.__z == other.y() * self.__z
            return False
        raise TypeError('Vector expected!')
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
        if isinstance(other, int) or isinstance(other, float):
            return Vector3D(self.x() * other, self.y() * other, self.__z * other)
        if isinstance(other, Vector3D):
            return Vector3D(self.y() * other.__z - self.__z * other.y(), self.__z * other.x() - self.x() - other.__z, self.x() * other.y() - self.y() * other.x())
        if isinstance(other, Vector2D):
            return Vector3D(-self.__z * other.y(), self.__z * other.x(), self.x() * other.y() - self.y() * other.x())
        raise TypeError('A real number or another vector expected!')
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