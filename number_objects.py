def base_repr(n: int, g: int) -> str:
    base_g_digits = []

    while n:
        n, mod = divmod(n, g)
        if mod < 10:
            digit = str(mod)
        elif mod <= 36:
            digit = chr(mod + 55)
        else:
            raise Exception('base bigger than 36 given!')
        base_g_digits.append(digit)

    return ''.join(reversed(base_g_digits)) or '0'


class NumberArray:
    def __init__(self, g, number_of_digits):
        self.g = g
        self.l = number_of_digits
        self._digit_array = ['.' for i in range(number_of_digits)]

    @property
    def array_access_bias(self):
        raise NotImplementedError()

    def __getitem__(self, item):
        if isinstance(item, slice):
            raise TypeError(f"{self.__class__.__name__} object is not subscriptable")
        if not 0 + self.array_access_bias <= item <= self.l - 1 + self.array_access_bias:
            raise IndexError(f"{self.__class__.__name__} indexes must be between: {0 + self.array_access_bias}"
                             f" and: {self.l - 1 + self.array_access_bias}")

        digit = self._digit_array.__getitem__(item - self.array_access_bias)
        if digit == '.':
            return '.'
        else:
            return int(digit, base=self.g)

    @property
    def _int_value(self) -> int:
        if '.' in self._digit_array:
            raise ValueError(f"{self} still has undetermined digits")
        return int("".join(reversed(self._digit_array)), base=self.g)

    def __eq__(self, other):
        return self._int_value == other

    def __add__(self, other):
        return self._int_value + other

    def __radd__(self, other):
        return self._int_value + other

    def __repr__(self):
        """
        an array is arranged from left to right,
        but the Nth digit of a number is Nth from the right,
        so we reverse the array when we present it.
        """
        return f'{self.__class__.__name__}: {"".join(reversed(self._digit_array))}, g={self.g}'


class NumberConstructor(NumberArray):
    def __init__(self, g, number_of_digits, *digits):
        super().__init__(g, number_of_digits)

        for i, d in enumerate(digits):
            self[i+1] = d

    @property
    def array_access_bias(self):
        """in the article, the first digit of the palindromes and carries is 1"""
        return 1

    def __setitem__(self, key, value: int or str):
        if not 0 + self.array_access_bias <= key <= self.l - 1 + self.array_access_bias:
            raise IndexError(f"{self.__class__.__name__} indexes must be between 1 and: {self.l}")
        value = str(value)
        self._digit_array.__setitem__(key - self.array_access_bias, value)


class CarryColumn(NumberConstructor):
    def __init__(self, g, number_of_digits, *digits):
        super().__init__(g, number_of_digits, *digits)


class Palindrome(NumberConstructor):
    def __init__(self, g, number_of_digits, *digits):
        super().__init__(g, number_of_digits, *digits)

    def __setitem__(self, key, value: int or str):
        """
        Since this is a palindrome, we need to set the
        (key)'th digit from the right and the (key)'th digit from the left
        """
        super().__setitem__(key, value)
        self._digit_array.__setitem__(self.l - 1 - (key - self.array_access_bias), str(value))


class NType:
    A_1 = 'A_1'
    A_2 = 'A_2'
    A_3 = 'A_3'
    A_4 = 'A_4'
    A_5 = 'A_5'
    A_6 = 'A_6'

    B_1 = 'B_1'
    B_2 = 'B_2'
    B_3 = 'B_3'
    B_4 = 'B_4'
    B_5 = 'B_5'
    B_6 = 'B_6'
    B_7 = 'B_7'


class DeltaNumber(NumberArray):
    def __init__(self, n, g):
        n_in_base = base_repr(n, g)
        super().__init__(g, len(n_in_base))

        self._ntype = None
        self._digit_array = list(reversed(n_in_base))

        self.p1, self.p2, self.p3 = self.base_palindromes()
        self.c = CarryColumn(g, self.l, (self.p1[1] + self.p2[1] + self.p3[1]) // g)  # step 1 in all algorithms

    @property
    def array_access_bias(self):
        return 0

    def D(self, a):
        return a % self.g

    def carry(self, i):
        """
        carry the sum of the i column of palindromes -
        sum the ith digits of the palindromes and the previous carry, and subtract the corresponding digit of n.
        we floor-divide this number in the base, to get only the second digit.
        """
        self.c[i] = (self.p1[i] + self.p2[i] + self.p3[i] + self.c[i-1] - self[i-1]) // self.g

    @property
    def ntype(self):
        if self._ntype:
            return self._ntype

        l = self.l

        # A types
        if self[l - 2] not in (0, 1, 2):
            if self.D(self[0] - self[l - 1] - self[l - 2] + 1) != 0:
                self._ntype = NType.A_1
            else:
                self._ntype = NType.A_2
        else:
            if self[l - 1] != 1:
                if self.D(self[0] - self[l - 1] + 2) != 0:
                    self._ntype = NType.A_3
                else:
                    self._ntype = NType.A_4
            elif self[l - 2] == 0:
                if self[l - 3] <= 3 and self.D(self[0] - self[l - 3]) != 0:
                    self._ntype = NType.A_5
                elif self[l - 3] <= 2 and self.D(self[0] - self[l - 3]) == 0:
                    self._ntype = NType.A_6

        # B types
        if self[l - 1] == 1:
            if self[l - 2] <= 2:
                if self[l - 3] <= 4 and self.D(self[0] - self[l - 3]) != 0:
                    self._ntype = NType.B_1
                elif self[l - 3] <= 3 and self.D(self[0] - self[l - 3]) == 0:
                    self._ntype = NType.B_2
            elif self[l - 2] in (1, 2):
                if self[l - 3] == 3:
                    if self.D(self[0] - 3) != 0:
                        self._ntype = NType.B_6
                    elif self[0] == 3:
                        self._ntype = NType.B_7
                elif self[0] == 0:
                    if self[l - 3] in (0, 1):
                        self._ntype = NType.B_3
                    elif self[l - 3] in (2, 3):
                        self._ntype = NType.B_4
                elif self[l - 3] in (0, 1, 2):
                    self._ntype = NType.B_5

        return self._ntype

    def base_palindromes(self) -> (Palindrome, Palindrome, Palindrome):
        l = self.l
        g = self.g

        if self.ntype == NType.A_1:
            p1 = Palindrome(g, l, self[l - 1])
            p2 = Palindrome(g, l - 1, self[l - 2] - 1)
            p3 = Palindrome(g, l - 2, self.D(self[0] - self[l - 1] - self[l - 2] + 1))
        elif self.ntype == NType.A_2:
            p1 = Palindrome(g, l, self[l - 1])
            p2 = Palindrome(g, l - 1, self[l - 2] - 2)
            p3 = Palindrome(g, l - 2, 1)
        elif self.ntype == NType.A_3:
            p1 = Palindrome(g, l, self[l - 1] - 1)
            p2 = Palindrome(g, l - 1, g - 1)
            p3 = Palindrome(g, l - 2, self.D(self[0] - self[l - 1] + 2))
        elif self.ntype == NType.A_4:
            p1 = Palindrome(g, l, self[l - 1] - 1)
            p2 = Palindrome(g, l - 1, g - 2)
            p3 = Palindrome(g, l - 2, 1)
        elif self.ntype == NType.A_5:
            p1 = Palindrome(g, l - 1, g - 1)
            p2 = Palindrome(g, l - 2, self[l - 3] + 1)
            p3 = Palindrome(g, l - 3, self.D(self[0] - self[l - 3]))
        elif self.ntype == NType.A_6:
            p1 = Palindrome(g, l - 1, g - 1)
            p2 = Palindrome(g, l - 2, self[l - 3] + 2)
            p3 = Palindrome(g, l - 3, g - 1)

        elif self.ntype == NType.B_1:
            p1 = Palindrome(g, l, 1, self[l - 2])
            p2 = Palindrome(g, l - 2, self[l - 3] - 1)
            p3 = Palindrome(g, l - 3, self.D(self[0] - self[l - 3]))
        elif self.ntype == NType.B_2:
            p1 = Palindrome(g, l, 1, self[l - 2])
            p2 = Palindrome(g, l - 2, self[l - 3] - 2)
            p3 = Palindrome(g, l - 3, 1)
        elif self.ntype == NType.B_3:
            p1 = Palindrome(g, l, 1, self[l - 2] - 1)
            p2 = Palindrome(g, l - 2, g - 2)
            p3 = Palindrome(g, l - 3, 1)
        elif self.ntype == NType.B_4:
            p1 = Palindrome(g, l, 1, self[l - 2])
            p2 = Palindrome(g, l - 2, 1)
            p3 = Palindrome(g, l - 3, g - 2)
        elif self.ntype == NType.B_5:
            p1 = Palindrome(g, l, 1, self[l - 2] - 1)
            p2 = Palindrome(g, l - 2, g - 1)
            p3 = Palindrome(g, l - 3, self[0])
        elif self.ntype == NType.B_6:
            p1 = Palindrome(g, l, 1, self[l - 2])
            p2 = Palindrome(g, l - 2, 2)
            p3 = Palindrome(g, l - 3, self.D(self[0] - 3))
        elif self.ntype == NType.B_7:
            p1 = Palindrome(g, l, 1, self[l - 2])
            p2 = Palindrome(g, l - 2, 1)
            p3 = Palindrome(g, l - 3, 1)
        else:
            raise TypeError('No NType assigned to self')

        return p1, p2, p3

    @property
    def is_special(self):
        if self.p1.l % 2 == 0:
            m = self.p1.l // 2
            return self.p1.l[m] == 0 or self.p1.l[m - 1] == 0
        return False
