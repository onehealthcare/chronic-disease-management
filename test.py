class A:
    def __init__(self, a):
        self.a = 1

    def __add__(self, other):
        return self.a + other.a


def add(a: int, b: int):
    return a + b


def divide(a: int, b: int):
    return a / b


def countdown(n: int):
    while n > 0:
        countdown(n)


def main():
    add(1, 2)
    add(1, "a")
    divide(1, 2)
    divide(1, 0)

    a = A(1)
    add(a.a, a.b)


if __name__ == '__main__':
    main()
