from number_objects import DeltaNumber, NType


def algorithm_1(n: DeltaNumber):
    # conventions
    g = n.g
    m = n.l // 2

    # step 1
    x1, y1, z1 = n.p1[1], n.p2[1], n.p3[1]
    n.carry[1] = c1 = (x1 + y1 + z1) // g

    # step 2
    if z1 <= n[2 * m - 2] - 1:
        x2 = n.D(n[2 * m - 1] - y1)
    else:
        x2 = n.D(n[2 * m - 1] - y1 - 1)
    y2 = n.D(n[2 * m - 2] - z1 - 1)
    z2 = n.D(n[1] - x2 - y2 - n.carry[1])
    c2 = (x2 + y2 + z2 + n.carry[1] - n[1]) // g
    n.p1[2], n.p2[2], n.p3[2], n.carry[2] = x2, y2, z2, c2

    # steps 3<=i<=m
    for i in range(3, m + 1):
        if n.p3[i - 1] <= n[2 * m - i] - 1:
            xi = 1
        else:
            xi = 0
        yi = n.D(n[2 * m - i] - n.p3[i - 1] - 1)
        zi = n.D(n[i - 1] - xi - yi - n.carry[i - 1])
        ci = (xi + yi + zi + n.carry[i - 1] - n[i - 1]) // g
        n.p1[i], n.p2[i], n.p3[i], n.carry[i] = xi, yi, zi, ci

    # step m+1
    n.p1[m+1] = 0

    # TODO: The adjustment step
    return n


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


if __name__ == '__main__':
    n = DeltaNumber(135_948_762, 10)
    regular_cases(n)
    print(n)
    print(n.p1)
    print(n.p2)
    print(n.p3)
    assert n.p1 + n.p2 + n.p3 == n
