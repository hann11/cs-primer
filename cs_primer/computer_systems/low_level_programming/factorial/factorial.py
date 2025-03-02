def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


print(f"Factorial of 0 is {factorial(0)}")
print(f"Factorial of 1 is {factorial(1)}")
print(f"Factorial of 2 is {factorial(2)}")
print(f"Factorial of 3 is {factorial(3)}")
print(f"Factorial of 5 is {factorial(5)}")
print(f"Factorial of 10 is {factorial(10)}")
