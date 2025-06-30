class MyRange:
    def __init__(self, n: int):
        self.counter = 0
        self.max = n

    def __next__(self):
        self.check()
        next = self.counter
        self.counter += 1
        return next

    def __iter__(self):
        return self

    def check(self):
        if self.counter == self.max:
            raise StopIteration("End")


def my_range(n):
    i = 0
    while i < n:
        yield i
        i += 1


b = my_range(5)
print(type(b))
next(b)
next(b)
print(next(b))
for x in my_range(5):
    print(x)
