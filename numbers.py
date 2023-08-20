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


class NumberConstructor:
    def __init__(self, g, number_of_digits, *digits):
        self.g = g
        self.l = number_of_digits
        self._digit_array = ['.' for i in range(number_of_digits)]

        for i, d in enumerate(digits):
            self[i] = d

    def __getitem__(self, item):
        if isinstance(item, slice):
            raise TypeError(f"{self.__class__.__name__} does not support slice notation")
        if not 1 <= item <= self.l:
            raise IndexError(f"{self.__class__.__name__} indexes must be between 1 and: {self.l}")

        # an array is arranged from left to right, but the nth digit
        # of a number is nth from the right.
        # in the article, the first digit of the palindromes and carries is 1.
        digit = self._digit_array.__getitem__(self.l - item)
        if digit == '.':
            return '.'
        else:
            return int(digit, base=self.g)

    def __setitem__(self, key, value: int or str):
        value = str(value)
        self._digit_array.__setitem__(self.l - key, value)

    def __repr__(self):
        return f'{self.__class__.__name__}: {"".join(self._digit_array)}, g={self.g}'


class CarryColumn(NumberConstructor):
    def __init__(self, g, number_of_digits, *digits):
        super().__init__(g, number_of_digits, *digits)


class Palindrome(NumberConstructor):
    def __init__(self, g, number_of_digits, *digits):
        super().__init__(g, number_of_digits, *digits)

    def __setitem__(self, key, value: int or str):
        super().__setitem__(key, value)
        self._digit_array.__setitem__(key - 1, value)


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


class DeltaNumber:
    def __init__(self, n, g):
        self.g = g
        self._ntype = None

        n_in_base = base_repr(n, g)
        self.n_in_base = n_in_base
        self.l = len(n_in_base)
        self._digit_array = list(n_in_base)

        self.p1, self.p2, self.p3 = self.base_palindromes()
        self.carry = CarryColumn(g, self.l)

    def __getitem__(self, item):
        if not 0 <= item <= self.l - 1:
            raise IndexError(f"{self.__class__.__name__} indexes must be between 0 and: {self.l - 1}")
        # an array is arranged from left to right, but the nth digit
        # of a number is nth from the right.
        return int(self._digit_array.__getitem__(self.l - 1 - item), base=self.g)

    def __repr__(self):
        return f'DeltaNumber: {self.n_in_base}, g={self.g}'

    def D(self, a):
        return a % self.g

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
