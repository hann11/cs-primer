import math


class Vec(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def magnitude(self):
        return math.sqrt(self.a**2 + self.b**2)

    def __add__(self, v2):
        return Vec(self.a + v2.a, self.b + v2.b)

    def __repr__(self):  # print
        return f"<{self.a},{self.b}>"

    def __eq__(self, v2):  # must have this to ensure equality
        return (self.a, self.b) == (v2.a, v2.b)

    def __mul__(self, x: int):
        return Vec(self.a * x, self.b * x)


if __name__ == "__main__":
    v1 = Vec(3, 2)
    v2 = Vec(1, 1)
    v3 = Vec(8, -6)
    v4 = Vec(4, 3)
    assert v3.magnitude() == 10.0
    print(v1.__add__(v2))
    print(v1 + v2)
    print(v4)
    print(v1 + v2 == v4)
    print(v1 * 4)
    # assert v1 + v2 == Vec(4, 3)
    # assert v1 * 2 == Vec(6, 4)
