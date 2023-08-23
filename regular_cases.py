from number_objects import DeltaNumber, NType


def algorithm_1(n: DeltaNumber):
    # conventions
    m = n.m
    x, y, z = n.p1, n.p2, n.p3
    c = n.c

    # step 1 - define the carry, done in the __init__ of the DeltaNumber object
    # step 2
    if z[1] <= n[2 * m - 2] - 1:
        x[2] = n.D(n[2 * m - 1] - y[1])
    else:
        x[2] = n.D(n[2 * m - 1] - y[1] - 1)
    y[2] = n.D(n[2 * m - 2] - z[1] - 1)
    z[2] = n.D(n[1] - x[2] - y[2] - c[1])
    n.carry(2)

    # steps 3<=i<=m
    for i in range(3, m + 1):
        if z[i - 1] <= n[2 * m - i] - 1:
            x[i] = 1
        else:
            x[i] = 0
        y[i] = n.D(n[2 * m - i] - z[i - 1] - 1)
        z[i] = n.D(n[i - 1] - x[i] - y[i] - c[i - 1])
        n.carry(i)

    # adjustment step
    if c[m] == 1:
        x[m + 1] = 0
    elif c[m] == 0:
        x[m + 1] = 1
    elif c[m] == 2:
        x[m + 1] = 0
        y[m + 1] -= 1
        y[m] -= 1
        z[m] = 0

    return n


def algorithm_2(n: DeltaNumber):
    g = n.g
    m = n.m
    x, y, z = n.p1, n.p2, n.p3
    c = n.c

    # step 1 - define the carry, done in the __init__ of the DeltaNumber object
    # step 2
    if z[1] <= n[2 * m - 3] - 1:
        x[2] = n.D(n[2 * m - 2] - y[1])
    else:
        x[2] = n.D(n[2 * m - 2] - y[1] - 1)
    y[2] = n.D(n[2 * m - 3] - z[1] - 1)
    z[2] = n.D(n[1] - x[2] - y[2] - c[1])
    n.carry(2)

    # steps 3<=i<=m-1
    for i in range(3, m):
        if z[i - 1] <= n[2 * m - i - 1] - 1:
            x[i] = 1
        else:
            x[i] = 0
        y[i] = n.D(n[2 * m - i - 1] - z[i - 1] - 1)
        z[i] = n.D(n[i - 1] - x[i] - y[i] - c[i - 1])
        n.carry(i)

    # step m
    x[m] = 0
    y[m] = n.D(n[m - 1] - z[m - 1] - c[m - 1])
    n.carry(m)

    # adjustment step
    # c[m] is in (0, 1, 2). if c[m] == 1, no adjustment needed, and c[m] == 2 only if n is special.
    if c[m] == 0:
        if y[m] != 0:
            x[m + 1] = x[m] = 1
            y[m] -= 1
        else:
            if y[m - 1] != 0:
                x[m + 1] = 1  # also assigns x[m]
                y[m + 1] -= 1  # also assigns y[m - 1]
                y[m] = g - 2  # only assigns y[m]
                z[m] += 1  # also assigns z[m - 1]
            elif z[m - 1] != 0:
                y[m + 1] = y[m] = 0
                z[m] -= 1
            else:
                x[m + 2] -= 1
                x[m + 1] = 1
                y[m + 1] = g - 1
                y[m] = g - 4
                z[m + 2] = 0
                z[m] = 2

    return n


def algorithm_3(n: DeltaNumber):
    g = n.g
    m = n.m
    x, y, z = n.p1, n.p2, n.p3
    c = n.c

    # step 1 - define the carry, done in the __init__ of the DeltaNumber object

    # step 2
    if z[1] <= n[2 * m - 3] - 1:
        x[3] = n.D(n[2 * m - 2] - y[1])
    else:
        x[3] = n.D(n[2 * m - 2] - y[1] - 1)
    y[2] = n.D(n[2 * m - 3] - z[1] - 1)
    z[2] = n.D(n[1] - x[2] - y[2] - c[1])
    n.carry(2)

    # steps 3<=i<=m-1
    for i in range(3, m):
        if z[i - 1] <= n[2 * m - i - 1] - 1:
            x[i + 1] = 1
        else:
            x[i + 1] = 0
        y[i] = n.D(n[2 * m - i - 1] - z[i - 1] - 1)
        z[i] = n.D(n[i - 1] - x[i] - y[i] - c[i - 1])
        n.carry(i)

    # step m
    x[m + 1] = 0
    y[m] = n.D(n[m - 1] - z[m - 1] - x[m] - c[m - 1])
    n.carry(m)

    # adjustment step
    # c[m] is in (0, 1, 2). if c[m] == 0, no adjustment is needed.
    if c[m] == 1:
        x[m + 1] = 1
    elif c[m] == 2:
        if y[m - 1] != 0:
            if z[m - 1] != g - 1:
                y[m + 1] -= 1
                y[m] -= 1
                z[m] += 1
            else:
                x[m + 1] = 1
                y[m + 1] -= 1
                z[m] = 0
        elif z[m - 1] != g - 1:
            x[m + 2] -= 1
            y[m + 1] = g -1
            y[m] -= 1
            z[m] += 1
        else:
            x[m + 2] -= 1
            x[m + 1] = 1
            y[m + 1] = g - 1
            z[m] = 0

    return n


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
        else:  # B types
            return algorithm_4(n)
    else:
        if n.ntype in (NType.A_1, NType.A_2, NType.A_3, NType.A_4):
            return algorithm_1(n)
        elif n.ntype in (NType.A_5, NType.A_6):
            return algorithm_2(n)
        else:  # B types
            return algorithm_3(n)


if __name__ == '__main__':
    n = DeltaNumber(120205690315959428539, 10)
    regular_cases(n)
    print(n)
    print(n.p1)
    print(n.p2)
    print(n.p3)
    print(f"{n.p1} + {n.p2} + {n.p3} == {n.p1 + n.p2 + n.p3}")
    assert n.p1 + n.p2 + n.p3 == n
