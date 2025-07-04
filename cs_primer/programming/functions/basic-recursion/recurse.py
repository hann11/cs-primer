"""
Implement the following functions, using recursion.

If you find it easier to use iteration, do that first! Then, rewrite it recursively :)

If the recursive approach seems obvious, try to also write it iteratively. Seeing
the connection between the two is highly worthwhile.

This is just for practice. In reality, most or all of these would be solved well enough
or better with iteration. But by getting some extra reps on easier problems, we'll
be better prepared for harder problems where recursion is a good fit.
"""


def factorial(n):
    """
    Calculate the product of the first n integers

    >>> factorial(3)  # 1 * 2 * 3
    6
    >>> factorial(10)  # 1 * 2 * ... * 10
    3628800
    """
    if n == 1:
        return 1
    return n * factorial(n - 1)


def palindrome(letters):
    """
    Determine if the given phrase is a palindrome. As a stretch goal, support phrases
    such as "A man, a plan, a canal — Panama!"

    >>> palindrome("racecar")
    True

    >>> palindrome("hello")
    False

    >>> palindrome("acdcebeijge")
    False

    >>> palindrome("amanaplanacanalpanama")
    True
    """
    if len(letters) <= 3:
        return letters[0] == letters[-1]  # TODO: can this be refined?

    return letters[0] == letters[-1] and palindrome(letters[1:-1])


def gcd(a, b):
    """
    Determine the greatest common divisor of two integers a and b. One approach is
    described in Euclid's Elements roughly as:

    - Repeatedly subtract the smaller number from the larger one, until no longer possible
    - If the remainder is zero, then the smaller number must be the GCD
    - Otherwise, repeat the process, using the number you were subtracting as the new "larger"
        number, and the remainder as the new "smaller" number

    For example if a = 1071 and b = 462 (taken from Wikipedia):

    - Subtracting 462 twice from 1071 leaves a remainder of 147
    - Subtracting 147 three times from 462 leaves a remainder of 21
    - Subtracting 21 seven ties from 147 leaves a remainder of 0

    So, 21 divides both 147 and 462, and is the greatest number to do this.


    PLAN:
    Given a = 1071, b = 462; a = max, b = min
    subtract b from a until you get a remainder (r) gcd(a,b)
    subtract r from b until you get a remainder (g) gcd(r,b)
    subtract g from r until you get a remainder (e)

    if e is zero, return g

    >>> gcd(1071, 462)
    21

    >>> gcd(15, 9)
    3

    >>> gcd(9, 15)
    3

    >>> gcd(3, 5)
    1
    """

    large = max(a, b)
    small = min(a, b)

    rem = large % small

    if rem == 0:
        return small

    return gcd(small, rem)


def filter_recursive(f, xs):
    """
    Given a predicate function f (a function which returns True or False) and a list
    xs, return a new list with only the items of xs where f(x) is True.

    Below is an iterative approach. See if you can convert it to recursive, for practice.

    def filter_iter(f, xs):
        out = []
        for x in xs:
            if f(x):
                out.append(x)
        return out

    >>> filter_recursive(lambda x: x > 0, [-1, 3, -2, 5])
    [3, 5]
    >>> filter_recursive(lambda x: False, [1, 2])
    []

    BASE CASE:
    probably have 1 item in the list. append IF it hits f(x), add to list with +

    if len(xs) == 1:
        return [f(x)] if f(x) else []
    """
    pass


def reduce(f, xs, init=None):
    """
    Apply the function f cumulatively to the items of xs, reducing to a single value.

    If initializer is provided, use it as the first value. Otherwise, use only the
    values in xs.

    Below is an iterative approach. See if you can convert it to recursive, for practice.

    def reduce_iter(f, xs, init=None):
        xs = iter(xs)
        out = next(xs) if init is None else init
        for x in xs:
            out = f(out, x)
        return out

    >>> reduce(lambda acc, x: acc + x, [1, 2, 3, 4])
    10
    >>> def mirror(d, x):
    ...     d[x] = x
    ...     return d
    >>> reduce(mirror, ['foo', 'bar'], {})
    {'foo': 'foo', 'bar': 'bar'}
    """
    pass


def rabbit_pairs(n):
    """
    A newly born breeding pair of rabbits are placed in a field. At the age of one month,
    the pair produces another breeding pair of rabbits. All pairs will breed every month,
    and somehow never die. How many pairs will exist at month n?

    >>> rabbit_pairs(1)
    1

    >>> rabbit_pairs(2)  # first pair have mated, but not yet had babies
    1

    >>> rabbit_pairs(3)  # first babies are born, but not yet mated
    2

    >>> rabbit_pairs(4)  # original pair have another pair, so 1 is added to existing population of 2
    3

    >>> rabbit_pairs(5)  # two pairs have had babies, so 2 is added to existing population of 3
    5

    >>> rabbit_pairs(6)  # three pairs have babies, so 3 is added to existing population of 5
    8

    >>> rabbit_pairs(20)
    6765

    PLAN/ANALYSIS:
    a pair placed at the start, they can breed at the end of month 1
    at end of month two, they've produced a pair of breeding rabbits, so 1 pair can breed now
    at end of month 3, the 2 pairs can breed
    at end of month 4, first pair have another pair, so now 3
    end of month 5, 2 more pairs, 5
    end of month 6, 3 more pairs, 8
    end of 7, 5 more pairs, 13
    """

    if n <= 2:
        return 1

    return rabbit_pairs(n - 1) + rabbit_pairs(n - 2)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("ok")
