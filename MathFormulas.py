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
    n = abs(n)
    print(n)
    while n > 1:
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
def bin_to_dec(a: str):
    res = 0
    for i, b in enumerate(a):
        if b not in '01':
            raise ValueError(f'{a} is not a binary number!')
        if int(b):
            res += 2 ** (len(a) - i - 1)
    return res
def dec_to_bin(n: float):
    res, _pow = '', floor(log2(n))
    while n:
        res += str(int(n >= 2 ** _pow))
        if n >= 2 ** _pow:
            n -= 2 ** _pow
        _pow -= 1
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
