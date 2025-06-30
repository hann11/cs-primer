def verify(number: str) -> bool:
    """
    Verify the check digit and return True if it is valid, False if not.

    PLAN
    1. Reverse the number, drop off the check digit
    2. Iterate through the reversed number, if % 2 == 0, double or whatever, keep the sum
    3. Compute check digit with (10 - (s mod10)) mod10, verify equal to given check digit
    """
    sum = 0

    # move left to right and sum
    for i, digit in enumerate(reversed(number)):
        to_add_check = (1 + (i % 2)) * int(
            digit
        )  # can just use a lookup table here instead
        sum += to_add_check // 10 + to_add_check
    # verify check digit
    return sum % 10 == 0


if __name__ == "__main__":
    try:
        assert verify("17893729974")
        assert not verify("17893729975")
        print("Test successful")
    except AssertionError:
        print("Test failed")
