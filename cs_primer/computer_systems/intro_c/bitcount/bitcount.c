#include <assert.h>
#include <stdio.h>

int bitcount(unsigned int x) {
    int b = 0;
    while (x) { // while bits are left, do something. truth is nonzero in C, no bool type
        b += x & 0x01;
        x >>= 1;
    }
    return b;
}

int main() {
    printf("%lu\n", sizeof(unsigned int));
    assert(bitcount(0) == 0);
    assert(bitcount(1) == 1);
    assert(bitcount(3) == 2);
    assert(bitcount(8) == 1);
    // harder case:
    assert(bitcount(0xffffffff) == 32); // note this just keeps running with int bitcount(int x)
    printf("OK\n");
}
