from Personal.MathFormulas import round_if_possible, GCF
def inversions(*args: float):
    Inversions = 0
    for i in range(len(args)):
        for arg in args[i:]:
            Inversions += args[i] > arg
    return Inversions
def LegitMatrix(matrix):
    if isinstance(matrix, str) or isinstance(matrix, int) or isinstance(matrix, float) or isinstance(matrix, dict) or isinstance(matrix, tuple):
        return False
    for row in matrix:
        if not isinstance(row, list):
            return False
    return True
def RectangularMatrix(matrix):
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
    def __init__(self, Matrix1: iter):
        if not LegitMatrix(Matrix1):
            raise TypeError('This isn\'t an actual matrix!')
        if not RectangularMatrix(Matrix1):
            raise ValueError('All matrix rows should have the same number of elements!')
        if not OnlyNums(Matrix1):
            raise ValueError('Matrices can only contain numbers!')
        self.__Matrix, self.__rows, self.__cols, self.__curr_index = Matrix1, len(Matrix1), 0, -1
        if self.__rows:
            self.__cols = len(Matrix1[0])
    def square(self):
        return self.__rows == self.__cols
    def transpose(self):
        transposed = []
        for _ in range(self.__cols):
            transposed.append([])
        for col in range(self.__cols):
            for row in range(self.__rows):
                transposed[col].append(self.__Matrix[row][col])
        self.__Matrix, self.__rows, self.__cols = transposed, self.__cols, self.__rows
    def copy(self):
        return Matrix(self.__Matrix)
    def rows(self):
        return self.__rows
    def cols(self):
        return self.__cols
    def NeutralizingElementsUnderMainDiagonal(self):
        Copy, Inversions = self.copy(), 0
        for row in range(self.rows() - 1):
            if not Copy[row][row]:
                Inversions += 1
                I = row
                for r in range(row, self.rows()):
                    if Copy[r][row]:
                        break
                    I += 1
                    if I == self.rows():
                        for row1 in range(Copy.rows()):
                            d = GCF(*Copy[row1]) * (-1) ** (len([el for el in Copy[row1] if el < 0]) > len([el for el in Copy[row1] if el > 0]))
                            for col in range(Copy.cols()):
                                Copy[row1][col] = round_if_possible(Copy[row1][col] / d)
                        return Copy, Inversions
                Copy[row], Copy[I] = Copy[I], Copy[row]
            RemoveFromMatrix = Matrix([[0 for _ in range(self.rows())] for _ in range(row + 1)])
            for row1 in range(row + 1, self.rows()):
                RemoveFromMatrix.append([])
                for col in range(self.rows()):
                    a = round_if_possible(Copy[row][col] * Copy[row1][row] / Copy[row][row])
                    RemoveFromMatrix[row1].append(a)
            Copy -= RemoveFromMatrix
        for row in range(Copy.rows()):
            d = GCF(*Copy[row]) * (-1) ** (len([el for el in Copy[row] if el < 0]) > len([el for el in Copy[row] if el > 0]))
            for col in range(Copy.cols()):
                Copy[row][col] = round_if_possible(Copy[row][col] / d)
        return Copy, Inversions
    def LinearlyDependent(self):
        matrix = self.NeutralizingElementsUnderMainDiagonal()[0]
        for i in range(matrix.rows()):
            if not matrix[i][i]:
                return True
        return False
    def DeterminantByNeutralizingElements(self):
        if self.square():
            Res = self.NeutralizingElementsUnderMainDiagonal()
            res, p = Res[0] * (-1) ** Res[1], 1
            for i, r in enumerate(res):
                p *= r[i]
            return round_if_possible(p)
        raise ValueError('Square matrices only!')
    def append(self, v: iter):
        self.__Matrix.append(list(v))
        if not self.rows():
            self.__cols = len(v)
        self.__rows += 1
    def BruteForceDeterminant(self):
        if self.square():
            if self.rows() == 1:
                return round_if_possible(self.__Matrix[0][0])
            if self.LinearlyDependent():
                return 0
            if self.rows() == 2:
                return round_if_possible(self.__Matrix[0][0] * self.__Matrix[1][1] - self.__Matrix[0][1] * self.__Matrix[1][0])
            if self.rows() == 3:
                return round_if_possible(self.__Matrix[0][0] * self.__Matrix[1][1] * self.__Matrix[2][2] + self.__Matrix[0][2] * self.__Matrix[1][0] * self.__Matrix[2][1] + self.__Matrix[2][0] * self.__Matrix[0][1] * self.__Matrix[1][2] - self.__Matrix[0][2] * self.__Matrix[1][1] * self.__Matrix[2][0] - self.__Matrix[0][0] * self.__Matrix[1][2] * self.__Matrix[2][1] - self.__Matrix[2][2] * self.__Matrix[0][1] * self.__Matrix[1][0])
            det = 0
            for k in range(self.rows()):
                if self.__Matrix[0][k]:
                    New_Matrix = Matrix([])
                    for row in range(1, self.rows()):
                        New_Matrix.append([])
                        for column in range(self.rows()):
                            if column == k:
                                continue
                            New_Matrix[row - 1].append(self.__Matrix[row][column])
                    det += (-1) ** k * self.__Matrix[0][k] * New_Matrix.BruteForceDeterminant()
            return round_if_possible(det)
        raise ValueError('Square matrices only!')
    def InverseMatrix(self):
        if self.DeterminantByNeutralizingElements():
            res = Matrix([self.__Matrix[i].copy() for i in range(self.rows())])
            IdentityMatrix = identity_matrix(res.__rows)
            for row in range(res.rows() - 1):
                if not res.__Matrix[row][row]:
                    I = 0
                    for Row in range(res.rows()):
                        if res.__Matrix[Row][row]:
                            break
                        I += 1
                    res.__Matrix[row], res.__Matrix[I] = res.__Matrix[I], res.__Matrix[row]
                    IdentityMatrix[row], IdentityMatrix[I] = IdentityMatrix[I], IdentityMatrix[row]
                RemoveFromMatrix, RemoveFromIdentityMatrix = Matrix([[0 for _ in range(res.rows())] for _ in range(row + 1)]), Matrix([[0 for _ in range(res.rows())] for _ in range(row + 1)])
                for row1 in range(row + 1, res.rows()):
                    RemoveFromMatrix.append([]), RemoveFromIdentityMatrix.append([])
                    for col in range(res.rows()):
                        a, b = round_if_possible(res.__Matrix[row][col] * round_if_possible(res.__Matrix[row1][row]) / round_if_possible(res.__Matrix[row][row])), round_if_possible(IdentityMatrix[row][col] * res.__Matrix[row1][row] / res.__Matrix[row][row])
                        RemoveFromMatrix[row1].append(a), RemoveFromIdentityMatrix[row1].append(b)
                res -= RemoveFromMatrix
                IdentityMatrix -= RemoveFromIdentityMatrix
            for row in range(res.rows() - 1, 0, -1):
                for row1 in range(row - 1, -1, -1):
                    for col in range(res.rows()):
                        A = 0
                        if res.__Matrix[row1][row]:
                            A = round_if_possible(res.__Matrix[row1][row] * IdentityMatrix[row][col] / res.__Matrix[row][row])
                        IdentityMatrix[row1][col] -= A
            for r in range(res.rows()):
                for c in range(res.rows()):
                    IdentityMatrix[r][c] = round_if_possible(IdentityMatrix[r][c] / res.__Matrix[r][r])
            return IdentityMatrix
        raise ValueError('This matrix has a determinant of zero!')
    def __iter__(self):
        return self
    def __next__(self):
        if self.__curr_index < self.__rows - 1:
            self.__curr_index += 1
            return self.__Matrix[self.__curr_index]
        raise StopIteration()
    def __getitem__(self, i: int):
        i %= self.rows()
        for j, r in enumerate(self.__Matrix):
            if j == i:
                return r
    def __setitem__(self, key, value: iter):
        if self.cols() != len(value):
            raise Exception('Can\'t assign the row with a different length than the rest!')
        self.__Matrix[key] = list(value)
    def __neg__(self):
        return self.copy() * -1
    def __add__(self, other):
        if self.rows() == other.rows() and self.cols() == other.cols():
            res = Matrix([[] for _ in range(self.rows())])
            for i in range(self.rows()):
                res.__Matrix[i] = [self.__Matrix[i][j] for j in range(self.cols())]
            res.__rows, res.__cols = self.rows(), self.cols()
            for I in range(res.rows()):
                for J in range(other.cols()):
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
        res = Matrix([[] for _ in range(self.__rows)])
        for i in range(self.__rows):
            res.__Matrix[i] = [self.__Matrix[i][j] for j in range(self.__cols)]
        res.__rows, res.__cols = self.__rows, self.__cols
        if isinstance(other, float) or isinstance(other, int) or isinstance(other, complex):
            for I in range(res.__rows):
                for J in range(res.__cols):
                    res.__Matrix[I][J] = round_if_possible(res.__Matrix[I][J] * other)
            return res
        elif isinstance(other, Matrix):
            if res.__cols == other.__rows:
                ResultMatrix = Matrix([[] for _ in res.__Matrix])
                ResultMatrix.__rows, ResultMatrix.__cols = res.__rows, other.__cols
                for I in range(res.__rows):
                    for J in range(other.__cols):
                        ResultMatrix[I].append([])
                        s = 0
                        for k in range(res.__cols):
                            s += res.__Matrix[I][k] * other.__Matrix[k][J]
                        ResultMatrix.__Matrix[I][J] = round_if_possible(s)
                return ResultMatrix
            return 'These matrices can\'t be multiplied! Don\'t forget, that matrices don\'t always commute!'
    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, complex):
            return self * (other ** -1)
        elif isinstance(other, Matrix):
            if other.BruteForceDeterminant():
                return self * other.InverseMatrix()
            raise ZeroDivisionError('Can\'t divide by a matrix with a zero determinant!')
    def __pow__(self, power: int):
        if self.square():
            if power < 0:
                return self.__Matrix.InverseMatrix(self.__Matrix.matrix_to_power(self.__Matrix, -power))
            if not power:
                return identity_matrix(self.__rows)
            Matrix1 = Matrix([self.__Matrix[i].copy() for i in range(self.__rows)])
            for _ in range(power - 1):
                Matrix1 *= self
            return Matrix1
        raise Exception('A matrix can be powered to a number only if it\'s a square matrix!')
    def __eq__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, complex):
            return self.BruteForceDeterminant() == other if self.square() else False
        if isinstance(other, Matrix):
            if (self.__rows, self.__cols) == (other.__rows, other.__cols):
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
        for I in range(self.__rows):
            res += str(tuple(self.__Matrix[I])) + '\n' * (I < self.__rows - 1)
        return res
    def __repr__(self):
        return str(self)
def OnlyNums(matrix: Matrix):
    if LegitMatrix(matrix):
        for row in matrix:
            for element in row:
                if not (isinstance(element, int) or isinstance(element, float) or isinstance(element, complex)):
                    return False
        return True
