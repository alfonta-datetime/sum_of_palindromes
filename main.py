from number_objects import DeltaNumber
from regular_cases import regular_cases
from small_cases import small_cases


def get_palindromes(n: int, g: int) -> (int, int, int):
    """

    :param n: number
    :param g: base
    :return: three palindromes in base g that their sum is n
    """
    n = DeltaNumber(n, g)

    if len(n.l) < 7:
        x, y, z = small_cases(n)
    else:
        x, y, z = regular_cases(n)
    x = ...
    y = ...
    z = ...
    assert x + y + z == n
    return x, y, z
