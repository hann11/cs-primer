Vec = tuple[int]


def init_vec(a, b):
    return a, b


def magnitude(v1):
    return (v1[0] ** 2 + v1[1] ** 2) ** 0.5


def add_vec(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def print_vec(v1):
    print(f"<{v1[0], v1[1]}>")


def vec_equality(v1, v2):
    return v1[0] == v2[0] and v1[1] == v2[1]


def mul_vec(v1, s):
    return v1[0] * s, v1[1] * s


if __name__ == "__main__":
    v1 = init_vec(3, 2)
    v2 = init_vec(1, 1)
    v3 = init_vec(8, -6)
    v4 = init_vec(4, 3)

    assert magnitude(v3) == 10.0
    assert vec_equality(add_vec(v1, v2), v4)
