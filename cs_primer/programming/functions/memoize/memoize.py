import urllib.request


def memoize(f):
    kv_cache = {}

    def inner(arg):
        if arg in kv_cache:
            print("hit")
        else:
            kv_cache[arg] = f(arg)
        return kv_cache[arg]

    return inner  # now pass your arg in here


def fetch(url):
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
        return content


def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    # print(cache(fetch, "http://google.com")[:80])
    # print(cache(fetch, "http://google.com")[:80])
    cached_fetch = memoize(fetch)
    cached_fetch("http://google.com")
    print(cached_fetch("http://google.com")[:80])

    fib = memoize(fib)

    print(fib(10))
