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


class DeltaNumber:
    def __init__(self, n, g):
        self.n = n
        self.g = g
        n_in_base = base_repr(n, g)
        self.n_in_base = n_in_base
        self.l = len(n_in_base)
        self._reversed_n_in_base = ''.join(reversed(n_in_base))

    def __getitem__(self, item):
        return int(self._reversed_n_in_base.__getitem__(item), base=self.g)

    def __repr__(self):
        return f'DeltaNumber: {self.n_in_base}'

    @property
    def assign_type(self):
        l = self.l
        g = self.g

        def D(a):
            return a % g

        # A types
        if self[l - 2] not in (0, 1, 2):
            if D(self[0] - self[l - 1] - self[l - 2] + 1) != 0:
                return NType.A_1
            else:
                return NType.A_2
        else:
            if self[l - 1] != 1:
                if D(self[0] - self[l - 1] + 2) != 0:
                    return NType.A_3
                else:
                    return NType.A_4
            elif self[l - 2] == 0:
                if self[l - 3] <= 3 and D(self[0] - self[l - 3]) != 0:
                    return NType.A_5
                elif self[l - 3] <= 2 and D(self[0] - self[l - 3]) == 0:
                    return NType.A_6

        # B types
        if self[l - 1] == 1:
            if self[l - 2] <= 2:
                if self[l - 3] <= 4 and D(self[0] - self[l - 3]) != 0:
                    return NType.B_1
                elif self[l - 3] <= 3 and D(self[0] - self[l - 3]) == 0:
                    return NType.B_2
            elif self[l - 2] in (1, 2):
                if self[l - 3] == 3:
                    if D(self[0] - 3) != 0:
                        return NType.B_6
                    elif self[0] == 3:
                        return NType.B_7
                elif self[0] == 0:
                    if self[l - 3] in (0, 1):
                        return NType.B_3
                    elif self[l - 3] in (2, 3):
                        return NType.B_4
                elif self[l - 3] in (0, 1, 2):
                    return NType.B_5
