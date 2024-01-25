from LinearAlgebra.Vectors import Vector2D, Vector3D
from MathFormulas import round_if_possible
def inversions(*args: float):
    Inversions = 0
    for i in range(len(args)):
        for arg in args[i:]:
            Inversions += args[i] > arg
    return Inversions
def legitMatrix(matrix):
    if not isinstance(matrix, list):
        return False
    for row in matrix:
        if not isinstance(row, list):
            return False
    return True
def rectangularMatrix(matrix):
    try:
        a = len(matrix[0])
        for row in matrix:
            if a != len(row):
                return False
        return True
    except IndexError:
        return True
def identity_matrix(n: int):
    res = []
    for i in range(abs(n)):
        res.append([])
        for j in range(abs(n)):
            res[i].append(int(i == j))
    return Matrix(res)
class Matrix:
    def __init__(self, matrix: (iter, Vector2D)):
        self.__curr_index = -1
        if isinstance(matrix, Vector2D):
            self.__Matrix, self.__rows, self.__cols = [[matrix.x()], [matrix.y()]], 2, 1
            if isinstance(matrix, Vector3D):
                self.__Matrix += [matrix.z()]
                self.__rows += 1
        else:
            if not legitMatrix(matrix):
                raise TypeError('This isn\'t an actual matrix!')
            if not rectangularMatrix(matrix):
                raise ValueError('All matrix rows should have the same number of elements!')
            if not onlyNums(matrix):
                raise ValueError('Matrices can only contain numbers!')
            self.__Matrix, self.__rows, self.__cols = matrix, len(matrix), 0
            if self.__rows:
                self.__cols = len(matrix[0])
    def square(self):
        return self.__rows == self.__cols
    def transposed(self):
        return Matrix([[self.__Matrix[i][j] for i in range(self.__rows)] for j in range(self.__cols)])
    def copy(self):
        return Matrix(self.__Matrix)
    def rows(self):
        return self.__rows
    def cols(self):
        return self.__cols
    def neutralizingElementsUnderMainDiagonal(self):
        res, total_inversions = self.copy(), 0
        for row in range(self.__rows - 1):
            if not res[row][row]:
                total_inversions += 1
                i = row
                for r in range(row, self.__rows):
                    if res[r][row]:
                        break
                    i += 1
                    if i == self.__rows:
                        return res, total_inversions
                res[row], res[i] = res[i], res[row]
            RemoveFromMatrix = Matrix([[0 for _ in range(self.__rows)] for _ in range(row + 1)])
            for row1 in range(row + 1, self.__rows):
                RemoveFromMatrix.append([])
                for col in range(self.__rows):
                    RemoveFromMatrix[row1].append(round_if_possible(res[row][col] * res[row1][row] / res[row][row]))
            res -= RemoveFromMatrix
        return res, total_inversions
    def linearlyDependent(self):
        matrix = self.neutralizingElementsUnderMainDiagonal()[0]
        for i in range(matrix.__rows):
            if not matrix[i][i]:
                return True
        return False
    def determinant(self):
        if self.square():
            res = self.neutralizingElementsUnderMainDiagonal()
            res, p = res[0] * (-1) ** res[1], 1
            for i, r in enumerate(res):
                p *= r[i]
            return round_if_possible(p)
        raise ValueError('Square matrices only!')
    def append(self, v: iter):
        self.__Matrix.append(list(v))
        if not self.__rows:
            self.__cols = len(v)
        self.__rows += 1
    def determinantRec(self):
        if self.square():
            if self.__rows == 1:
                return round_if_possible(self.__Matrix[0][0])
            if self.linearlyDependent():
                return 0
            if self.__rows == 2:
                return round_if_possible(self.__Matrix[0][0] * self.__Matrix[1][1] - self.__Matrix[0][1] * self.__Matrix[1][0])
            if self.__rows == 3:
                return round_if_possible(self.__Matrix[0][0] * self.__Matrix[1][1] * self.__Matrix[2][2] + self.__Matrix[0][2] * self.__Matrix[1][0] * self.__Matrix[2][1] + self.__Matrix[2][0] * self.__Matrix[0][1] * self.__Matrix[1][2] - self.__Matrix[0][2] * self.__Matrix[1][1] * self.__Matrix[2][0] - self.__Matrix[0][0] * self.__Matrix[1][2] * self.__Matrix[2][1] - self.__Matrix[2][2] * self.__Matrix[0][1] * self.__Matrix[1][0])
            det = 0
            for k in range(self.__rows):
                if self.__Matrix[0][k]:
                    newMatrix = Matrix([])
                    for row in range(1, self.__rows):
                        newMatrix.append([])
                        for column in range(self.__rows):
                            if column == k:
                                continue
                            newMatrix[row - 1].append(self.__Matrix[row][column])
                    newMatrix.__cols = self.__cols - 1
                    det += (-1) ** k * self.__Matrix[0][k] * newMatrix.determinantRec()
            return round_if_possible(det)
        raise ValueError('Square matrices only!')
    def inverseMatrix(self):
        if self.determinant():
            res = Matrix([self.__Matrix[i].copy() for i in range(self.__rows)])
            E_n = identity_matrix(res.__rows)
            for row in range(res.__rows - 1):
                if not res.__Matrix[row][row]:
                    i = 0
                    for Row in range(res.__rows):
                        if res.__Matrix[Row][row]:
                            break
                        i += 1
                    res.__Matrix[row], res.__Matrix[i] = res.__Matrix[i], res.__Matrix[row]
                    E_n[row], E_n[i] = E_n[i], E_n[row]
                toRemoveFromSelf, toRemoveFromE_n = Matrix([[0 for _ in range(res.__rows)] for _ in range(row + 1)]), Matrix([[0 for _ in range(res.__rows)] for _ in range(row + 1)])
                for row1 in range(row + 1, res.__rows):
                    toRemoveFromSelf.append([]), toRemoveFromE_n.append([])
                    for col in range(res.__rows):
                        a, b = round_if_possible(res.__Matrix[row][col] * round_if_possible(res.__Matrix[row1][row]) / round_if_possible(res.__Matrix[row][row])), round_if_possible(E_n[row][col] * res.__Matrix[row1][row] / res.__Matrix[row][row])
                        toRemoveFromSelf[row1].append(a), toRemoveFromE_n[row1].append(b)
                res -= toRemoveFromSelf
                E_n -= toRemoveFromE_n
            for row in range(res.__rows - 1, 0, -1):
                for row1 in range(row - 1, -1, -1):
                    for col in range(res.__rows):
                        A = 0
                        if res.__Matrix[row1][row]:
                            A = round_if_possible(res.__Matrix[row1][row] * E_n[row][col] / res.__Matrix[row][row])
                        E_n[row1][col] -= A
            for r in range(res.__rows):
                for c in range(res.__rows):
                    E_n[r][c] = round_if_possible(E_n[r][c] / res.__Matrix[r][r])
            return E_n
        raise ValueError('This matrix has a determinant of zero!')
    def __reversed__(self):
        return self.inverseMatrix()
    def __iter__(self):
        return self
    def __next__(self):
        if self.__curr_index < self.__rows - 1:
            self.__curr_index += 1
            return self.__Matrix[self.__curr_index]
        self.__curr_index = -1
        raise StopIteration()
    def __getitem__(self, i: int):
        if isinstance(i, slice):
            return Matrix(self.__Matrix[i])
        i %= self.__rows
        for j, r in enumerate(self.__Matrix):
            if j == i:
                return r
    def __setitem__(self, key, value: iter):
        if self.__rows != len(value):
            raise Exception('Can\'t assign the row with a different length than the rest!')
        self.__Matrix[key] = list(value)
    def __neg__(self):
        return -1 * self
    def __add__(self, other):
        if self.__rows == other.__rows and self.__rows == other.__rows:
            res = Matrix([[] for _ in range(self.__rows)])
            for i in range(self.__rows):
                res.__Matrix[i] = [self.__Matrix[i][j] for j in range(self.__rows)]
            res.__rows, res.__cols = self.__rows, self.__rows
            for I in range(res.__rows):
                for J in range(other.__rows):
                    res.__Matrix[I][J] = round_if_possible(res.__Matrix[I][J] + other.__Matrix[I][J])
            return res
        raise ValueError('Two matrices can have sum or difference only if they have the same dimensions!')
    def __sub__(self, other):
        if isinstance(other, Matrix):
            return self + Matrix((other * -1).__Matrix)
        try:
            return self + Matrix((Matrix(other) * -1).__Matrix)
        except TypeError or ValueError:
            raise ValueError('Can\'t subtract!')
    def __mul__(self, other):
        if isinstance(other, (int, float, complex)):
            return Matrix([[*map(lambda x: x * other, (r[i] for i in range(self.__cols)))] for r in self.__Matrix])
        if isinstance(other, Matrix):
            if self.__cols == other.__rows:
                return Matrix([[sum(self[r][k] * other[k][c] for k in range(self.__cols)) for c in range(other.__cols)] for r in range(self.__rows)])
            raise ValueError('These matrices can\'t be multiplied, because of their dimentions! Don\'t forget, that matrices don\'t always commute!')
        raise TypeError(f"Unsupported type: {type(other)}!")
    def __rmul__(self, other):
        return other * self if isinstance(other, Matrix) else self * other
    def __truediv__(self, other):
        if isinstance(other, (int, float, complex)):
            return self * (other ** -1)
        elif isinstance(other, Matrix):
            if other.determinantRec():
                return self * other.inverseMatrix()
            raise ZeroDivisionError('Can\'t divide by a matrix with a zero determinant!')
    def __pow__(self, power: int):
        if self.square():
            if power < 0:
                return (self ** -power).inverseMatrix()
            if not power:
                return identity_matrix(self.__rows)
            res = Matrix([self.__Matrix[i].copy() for i in range(self.__rows)])
            for _ in range(power - 1):
                res *= self
            return res
        raise Exception('A matrix can be powered to a number only if it\'s a square matrix!')
    def __eq__(self, other):
        if isinstance(other, (int, float, complex)):
            return self.determinantRec() == other if self.square() else False
        if isinstance(other, Matrix):
            if (self.__rows, self.__cols) != (other.__rows, other.__cols):
                return False
            for i in range(self.__rows):
                for j in range(self.__cols):
                    if self.__Matrix[i][j] != other.__Matrix[i][j]:
                        return False
            return True
        return False
    def __len__(self):
        return self.__rows
    def __str__(self):
        res = ''
        for r in self:
            res += str(tuple(r)) + '\n'
        return res
    def __repr__(self):
        return str(self)
def onlyNums(matrix: Matrix):
    if legitMatrix(matrix):
        for row in matrix:
            for element in row:
                if not isinstance(element, (int, float, complex)):
                    return False
        return True
M0 = Matrix([[7, 4, -3], [2, 6, -1], [0, 4, -1]])
M1 = Matrix([[-2, 4, 5], [3, 5, -3], [6, 2, 7]])
M2 = Matrix([[-8, 2, 4], [1, 4, 6]])
M2.transpose()
print((M0 - 2 * M1) * M2)
