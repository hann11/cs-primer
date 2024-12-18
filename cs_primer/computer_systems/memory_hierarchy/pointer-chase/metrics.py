import csv
import math
import time

import numpy as np


class User(object):
    def __init__(
        self,
        user_id: int,
        age: int,
        payments: float,
    ):
        self.user_id = user_id
        self.age = age
        self.payments = payments


def average(list_of_data):
    total = 0
    for a in list_of_data:
        total += a
    return total / len(list_of_data)


def stddev_payment_amount(list_of_data, mean):
    squared_diffs = 0
    for u in list_of_data:
        diff = u - mean
        squared_diffs += diff * diff
    return math.sqrt(squared_diffs / len(list_of_data))


def load_data():
    ages = []
    payments = []
    with open("users.csv") as f:
        for line in csv.reader(f):
            _, _, age, _, _ = line
            ages.append(int(age))
    with open("payments.csv") as f:
        for line in csv.reader(f):
            amount, _, _ = line
            payments.append(
                float(int(amount) // 100) + (int(amount) % 100) / 100
            )
    return np.array(ages), np.array(payments)


if __name__ == "__main__":
    t = time.perf_counter()
    ages, payments = load_data()
    print(f"Data loading: {time.perf_counter() - t:.3f}s")
    t = time.perf_counter()
    mean_payment = np.mean(payments)
    assert abs(np.mean(ages) - 59.626) < 0.01
    assert abs(np.std(payments) - 288684.849) < 0.01
    assert abs(mean_payment - 499850.559) < 0.01
    print(f"Computation {time.perf_counter() - t:.3f}s")
