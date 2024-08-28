class V:
    def __init__(self, *args) -> None:
        self.args = args
    def __str__(self) -> str:
        return "(" + ", ".join([str(x) for x in self.args]) + ")"
    def __add__(self, other: "V") -> "V":
        return V(*(a + b for a, b in zip(self.args, other.args)))
    def __sub__(self, other: "V") -> "V":
        return V(*(a - b for a, b in zip(self.args, other.args)))
    def __mul__(self, other: "V") -> "V":
        if type(other) in (int, float):
            return V(*([other * a for a in self.args]))
        return V(*(a * b for a, b in zip(self.args, other.args)))
    def __rmul__(self, other: int|float) -> "V":
        return self.__mul__(other)
    def __iter__(self):
        return iter(self.args)
    def __hash__(self):
        return hash(self.args)
    def __eq__(self, other: "V"):
        if not isinstance(other, self.__class__):
            return False
        for a, b in zip(self.args, other.args):
            if a != b:
                return False
        return True

V.ZERO = V(0, 0, 0)
V.ONE = V(1, 1, 1)
V.FORWARD = V(1, 0, 0)
V.BACKWARD = V(-1, 0, 0)
V.LEFT = V(0, 1, 0)
V.RIGHT = V(0, -1, 0)
V.UP = V(0, 0, 1)
V.DOWN = V(0, 0, -1)

if __name__ == "__main__":
    print(V(1, 2, 3))
    print(V(1, 2, 3) + V(4, 5, 6))
    print(V(1, 2, 3) - V(4, 5, 6))
    print(V(1, 2, 3) * V(4, 5, 6))
    print(V.UP)
    print(V(1, 2, 3) * V.LEFT)
    print(V(1, 2, 3) * 3)
    print(3 * V(1, 2, 3))
    print(*V(1, 2, 3))
    print(V(1, 2, 3) == V(1, 2, 3))
    print(V(1, 2, 3) == V(1, 2, 0))
    print(V(1, 2, 3) in (V(1, 2, 3), V(1, 2, 4)))
    print(V(1, 0, 3) in (V(1, 2, 3), V(1, 2, 4)))