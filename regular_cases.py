from numbers import DeltaNumber, NType


def algorithm_1(n: DeltaNumber):
    pass


def algorithm_2(n: DeltaNumber):
    pass


def algorithm_3(n: DeltaNumber):
    pass


def algorithm_4(n: DeltaNumber):
    pass


def algorithm_5(n: DeltaNumber):
    pass


def regular_cases(n: DeltaNumber):
    if n.is_special:
        return algorithm_5(n)
    elif n.l % 2 == 0:
        if n.ntype in (NType.A_1, NType.A_2, NType.A_3, NType.A_4):
            return algorithm_2(n)
        elif n.ntype in (NType.A_5, NType.A_6):
            return algorithm_1(n)
        else:
            return algorithm_4(n)
    else:
        if n.ntype in (NType.A_1, NType.A_2, NType.A_3, NType.A_4):
            return algorithm_1(n)
        elif n.ntype in (NType.A_5, NType.A_6):
            return algorithm_2(n)
        else:
            return algorithm_3(n)

