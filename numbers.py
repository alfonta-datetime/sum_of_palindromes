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


class PalindromeConstructor:
    def __init__(self, g, number_of_digits, *digits):
        self.g = g
        self.l = number_of_digits
        self._digit_array = ['.' for i in range(number_of_digits)]

        for i, d in enumerate(digits):
            self[i] = d

    def __getitem__(self, item):
        if isinstance(item, slice):
            raise TypeError("PalindromeConstructor does not support slice notation")

        digit = self._digit_array.__getitem__(self.l - 1 - item)
        if digit == '.':
            return '.'
        else:
            return int(digit, base=self.g)

    def __setitem__(self, key, value: int or str):
        value = str(value)
        self._digit_array.__setitem__(key, value)
        self._digit_array.__setitem__(self.l - 1 - key, value)

    def __repr__(self):
        return f'PalindromeConstructor: {"".join(self._digit_array)}'


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
        self.n = n
        self.g = g
        self._ntype = None

        n_in_base = base_repr(n, g)
        self.n_in_base = n_in_base
        self.l = len(n_in_base)
        self._reversed_n_in_base = ''.join(reversed(n_in_base))

        self.p1, self.p2, self.p3 = self.base_palindromes()

    def __getitem__(self, item):
        return int(self._reversed_n_in_base.__getitem__(item), base=self.g)

    def __repr__(self):
        return f'DeltaNumber: {self.n_in_base}'

    def D(self, a):
        return a % self.g

    @property
    def ntype(self):
        if self._ntype:
            return self._ntype

        l = self.l
        g = self.g

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

    def base_palindromes(self) -> (PalindromeConstructor, PalindromeConstructor, PalindromeConstructor):
        l = self.l
        g = self.g

        if self.ntype == NType.A_1:
            p1 = PalindromeConstructor(g, l, self[l - 1])
            p2 = PalindromeConstructor(g, l - 1, self[l - 2] - 1)
            p3 = PalindromeConstructor(g, l - 2, self.D(self[0] - self[l - 1] - self[l - 2] + 1))
        elif self.ntype == NType.A_2:
            p1 = PalindromeConstructor(g, l, self[l - 1])
            p2 = PalindromeConstructor(g, l - 1, self[l - 2] - 2)
            p3 = PalindromeConstructor(g, l - 2, 1)
        elif self.ntype == NType.A_3:
            p1 = PalindromeConstructor(g, l, self[l - 1] - 1)
            p2 = PalindromeConstructor(g, l - 1, g - 1)
            p3 = PalindromeConstructor(g, l - 2, self.D(self[0] - self[l - 1] + 2))
        elif self.ntype == NType.A_4:
            p1 = PalindromeConstructor(g, l, self[l - 1] - 1)
            p2 = PalindromeConstructor(g, l - 1, g - 2)
            p3 = PalindromeConstructor(g, l - 2, 1)
        elif self.ntype == NType.A_5:
            p1 = PalindromeConstructor(g, l - 1, g - 1)
            p2 = PalindromeConstructor(g, l - 2, self[l - 3] + 1)
            p3 = PalindromeConstructor(g, l - 3, self.D(self[0] - self[l - 3]))
        elif self.ntype == NType.A_6:
            p1 = PalindromeConstructor(g, l - 1, g - 1)
            p2 = PalindromeConstructor(g, l - 2, self[l - 3] + 2)
            p3 = PalindromeConstructor(g, l - 3, g - 1)

        elif self.ntype == NType.B_1:
            p1 = PalindromeConstructor(g, l, 1, self[l - 2])
            p2 = PalindromeConstructor(g, l - 2, self[l - 3] - 1)
            p3 = PalindromeConstructor(g, l - 3, self.D(self[0] - self[l - 3]))
        elif self.ntype == NType.B_2:
            p1 = PalindromeConstructor(g, l, 1, self[l - 2])
            p2 = PalindromeConstructor(g, l - 2, self[l - 3] - 2)
            p3 = PalindromeConstructor(g, l - 3, 1)
        elif self.ntype == NType.B_3:
            p1 = PalindromeConstructor(g, l, 1, self[l - 2] - 1)
            p2 = PalindromeConstructor(g, l - 2, g - 2)
            p3 = PalindromeConstructor(g, l - 3, 1)
        elif self.ntype == NType.B_4:
            p1 = PalindromeConstructor(g, l, 1, self[l - 2])
            p2 = PalindromeConstructor(g, l - 2, 1)
            p3 = PalindromeConstructor(g, l - 3, g - 2)
        elif self.ntype == NType.B_5:
            p1 = PalindromeConstructor(g, l, 1, self[l - 2] - 1)
            p2 = PalindromeConstructor(g, l - 2, g - 1)
            p3 = PalindromeConstructor(g, l - 3, self[0])
        elif self.ntype == NType.B_6:
            p1 = PalindromeConstructor(g, l, 1, self[l - 2])
            p2 = PalindromeConstructor(g, l - 2, 2)
            p3 = PalindromeConstructor(g, l - 3, self.D(self[0] - 3))
        elif self.ntype == NType.B_7:
            p1 = PalindromeConstructor(g, l, 1, self[l - 2])
            p2 = PalindromeConstructor(g, l - 2, 1)
            p3 = PalindromeConstructor(g, l - 3, 1)
        else:
            raise TypeError('No NType assigned to self')

        return p1, p2, p3
    
    @property
    def is_special(self):
        if self.p1.l % 2 == 0:
            m = self.p1.l / 2
            return self.p1.l[m] == 0 or self.p1.l[m-1] == 0
        return False
    