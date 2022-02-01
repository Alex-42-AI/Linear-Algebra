from math import floor, log, ceil, factorial, log2
from random import randrange
def round_if_possible(n, d=0):
    if isinstance(n, (int, complex)):
        return n
    if isinstance(n, float):
        return (round(n, d) if d > 0 else int(n)) if abs(n - round(n, d)) <= 5 * 10 ** -13 else n
    raise TypeError('Numbers only!')
def sum_in_arithmetic_progression(a_1: float, a_n: float, d=1):
    return round_if_possible((a_n ** 2 - a_1 ** 2 + d * (a_1 + a_n)) / (2 * d))
def sum_in_geometric_progression(a_1: float, a_n: float, q=2):
    return round_if_possible((q * a_n - a_1) / (q - 1))
def conjecture(n: int):
    print(n)
    while n ** 2 - 1:
        if n % 2:
            n = 3 * n + 1
        else:
            while not n % 2:
                n //= 2
        print(n)
def GCF(*args: int):
    res, args = 1, list(filter(bool, args))
    if not args:
        return 1
    for i in range(2, min(abs(i) for i in args) + 1):
        res += (i - res) * all(not arg % i for arg in args)
    return res
def SCD(*args: int):
    res = 1
    args = [i for i in args if i]
    for arg in args:
        res *= abs(arg)
    for i in range(res, max(abs(i) for i in args) - 1, -1):
        res += (i - res) * all(not i % arg for arg in args)
    return res
def bin_to_dec(a):
    if isinstance(a, str):
        try:
            a = int(a)
        except ValueError:
            raise ValueError('Unsupported value! Argument should contain digits only or be a number!')
    res = 0
    for i in range(len(str(a))):
        if str(a)[i] not in '01':
            raise ValueError(f'{a} is not a binary number!')
        res += int(str(a)[len(str(a)) - i - 1]) * 2 ** i
    return res
def dec_to_bin(n: int):
    res = ''
    while n:
        res += str(10 ** floor(log(n, 2)))
        n -= 2 ** floor(log(n, 2))
    return res
def hex_to_dec(a):
    if isinstance(a, int):
        a = str(a)
    if not isinstance(a, str):
        raise TypeError(f'Unsupported type {type(a)}. Expected type \'str\' or type \'int\'.')
    pairs = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    res = 0
    for i in range(len(a)):
        res += pairs[a[i]] * 16 ** (len(a) - i - 1)
    return res
def dec_to_hex(a: int):
    res = ''
    pairs = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    while a:
        res = pairs[a % 16] + res
        a //= 16
    return res
def custom_sqrt(n: float):
    imaginary = n < 0
    n = abs(n)
    if n == n ** 2:
        return n
    a = randrange(int(ceil(n)))
    if not a:
        a = 1
    first, second = a, n / a
    while round(second - first, 15):
        second, first = 2 * n / (second + first), second
    return complex(f'{round_if_possible(second)}j') if imaginary else round_if_possible(second)
def cbrt(n):
    if type(n) in (complex, float, int):
        if n == n ** 3:
            return n
        if isinstance(n, complex):
            return n ** (1 / 3)
        return round_if_possible(abs(n) ** (1 / 3) * (-1) ** (n < 0))
    raise TypeError(f"Inappropriate type! Expected a numerical value, got {type(n)} instead!")
def combinations(n: int, k: int):
    if n < k:
        return 0
    p = 1
    for i in range(n - k + 1, n + 1):
        p *= i
    p //= factorial(k)
    return p
def variations(n: int, k: int):
    if n < k:
        return 0
    p = 1
    for i in range(n - k, n + 1):
        p *= i
    return p
def intersection(*args: list):
    res = []
    for el in args[0]:
        if all(el in arg for arg in args[1:]):
            res.append(el)
    return res
def rotate_matrix(Matrix: iter, times: int):
    if times >= 0:
        for _ in range(times):
            res = [[0 for _ in range(len(Matrix))] for _ in range(len(Matrix))]
            for i in range(len(Matrix)):
                for j in range(len(Matrix)):
                    res[i][j] = Matrix[len(Matrix) - j - 1][i]
            Matrix = [row.copy() for row in res]
    else:
        for _ in range(-times):
            res = [[0 for _ in range(len(Matrix))] for _ in range(len(Matrix))]
            for i in range(len(Matrix)):
                for j in range(len(Matrix)):
                    res[i][j] = Matrix[j][len(Matrix) - i - 1]
            Matrix = [row.copy() for row in res]
    return Matrix
def maximum_seating(seats: iter):
    if not all(isinstance(i, int) for i in seats):
        raise TypeError('Integers expected!')
    total, seat = 0, 0
    while seat in range(len(seats)):
        if not seats[seat]:
            try:
                if not (seats[seat + 1] or seats[seat + 2]):
                    total += 1
                    seats[seat] = 1
                    seat += 2
            except IndexError:
                total += 1
                seats[seat] = 1
        else:
            seat += 2
        seat += 1
    return total
def longest_substring(digits: str):
    if digits.isdigit():
        longest, d = None, 0
        while d in range(len(digits)):
            if int(digits[d]) % 2:
                so_far, curr = '', 0
                while (int(digits[d]) + curr) % 2:
                    so_far += digits[d]
                    d += 1
                    curr += 1
                    if d == len(digits):
                        break
                d -= 1
            else:
                so_far, curr = '', 0
                while not (int(digits[d]) + curr) % 2:
                    so_far += digits[d]
                    d += 1
                    curr += 1
                    if d == len(digits):
                        break
                d -= 1
            if longest is None:
                longest = so_far
            elif len(so_far) > len(longest):
                longest = so_far
            d += 1
        return longest
    raise ValueError('Digits expected!')
def permutations_where_els_match_indexes(n: int):
    return int(factorial(n) * sum((-1) ** k / factorial(k + 1) for k in range(n)))
def permutations(iterable: list):
    def predicate(Iter: list):
        sort = sorted(Iter)
        for I, EL in enumerate(Iter):
            if EL == sort[I]:
                return True
        return False
    res = []
    if len(iterable) <= 1:
        return [iterable.copy()]
    for el in iterable:
        iterable.remove(el)
        a = permutations(iterable)
        for permutation in a:
            for i in range(len(permutation) + 1):
                permutation.insert(i, el)
                if permutation not in res:
                    res += [permutation.copy()]
                permutation.pop(i)
    return res
def Josephus_problem_iter(I: iter):
    if not I:
        return []
    while True:
        res = []
        for i, el in enumerate(I):
            if not i % 2:
                res.append(el)
        if len(I) % 2:
            I = [res[-1]] + res[:-1]
        else:
            I = res.copy()
        if len(I) == 1:
            return res[0]
def Josephus_problem_number(n: int):
    return 2 * (n - 2 ** floor(log2(n))) + 1
def Josephus_problem_number_recursive(n: int):
    if n == n ** 2:
        return 1
    if n % 2:
        return 2 * Josephus_problem_number_recursive((n - 1) // 2) + 1
    return 2 * Josephus_problem_number_recursive(n // 2) - 1
class Rational:
    def __init__(self, a: int, b: int):
        if not b:
            raise ZeroDivisionError
        self.a, self.b = a // GCF(a, b), abs(b) // GCF(a, b)
        self.value = round_if_possible(a / b)
    def reciprocal(self):
        return Rational(self.b, self.a)
    def __neg__(self):
        return Rational(-self.a, self.b)
    def __add__(self, other):
        if isinstance(other, Rational):
            return Rational(self.a * other.b + other.a * self.b, self.b * other.b)
        if isinstance(other, int):
            return Rational(other * self.b + self.a, self.b)
        if isinstance(other, (float, complex)):
            return self.value + other
        raise TypeError(f'Addition not defined between type Rational and type {type(other)}!')
    def __sub__(self, other):
        if isinstance(other, (Rational, int)):
            return self + -other
        if isinstance(other, (float, complex)):
            return self.value - other
        raise TypeError(f'Subtraction undefined between type Rational and type {type(other)}!')
    def __mul__(self, other):
        if isinstance(other, Rational):
            return Rational(self.a * other.a, self.b * other.b)
        if isinstance(other, int):
            return Rational(other * self.a, self.b)
        if isinstance(other, (float, complex)):
            return self.value * other
        raise TypeError(f'Multiplication not defined between type Rational and type {type(other)}!')
    def __truediv__(self, other):
        if isinstance(other, Rational):
            return Rational(self.a * other.b, other.b * self.a)
        if isinstance(other, int):
            return Rational(self.a, other * self.b)
        if isinstance(other, (float, complex)):
            return self.value / other
        raise TypeError(f'Division not defined between type Rational and type {type(other)}!')
    def __eq__(self, other):
        if isinstance(other, Rational):
            return self.value == other.value
        if isinstance(other, float):
            return self.value == other
    def __str__(self):
        return f'{self.a}/{self.b}'
    def __repr__(self):
        return str(self)
class Set:
    def __init__(self, els: iter):
        self.__sequence, self.__types = [], []
        for el in els:
            if el not in self.__sequence:
                self.__sequence.append(el)
                if type(el) not in self.__types:
                    self.__types.append(type(el))
    def add(self, item):
        if item not in self.__sequence:
            self.__sequence.append(item)
            if type(item) not in self.__types:
                self.__types.append(type(item))
    def remove(self, item):
        if item in self.__sequence:
            self.__sequence.remove(item)
            for el in self.__sequence:
                if isinstance(el, type(item)):
                    return
            self.__types.remove(type(item))
    def __contains__(self, item):
        return item in self.__sequence
    def __len__(self):
        return len(self.__sequence)
    def __eq__(self, other):
        if isinstance(other, Set):
            for el in self.__sequence:
                if el not in other:
                    return False
            return len(self) == len(other)
        if isinstance(other, (list, tuple, set, range)):
            return self == Set(*other)
        return False
    def __add__(self, other):
        if isinstance(other, Set):
            res = Set(self.__sequence)
            for el in other.__sequence:
                if el not in self.__sequence:
                    res.add(el)
            return res
    def __mul__(self, other):
        res = Set([])
        for el in self.__sequence:
            if el in other:
                res.add(el)
        return res
    def __str__(self):
        return '{' + ', '.join(self.__sequence) + '}'
    def __repr__(self):
        return str(self)