import os


def main():
    print(os.listdir())
    with open("a.out", "rb") as f:
        data = f.read()
    print(data)


if __name__ == "__main__":
    main()
