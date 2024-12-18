given `assert(bitcount(0) == 0);`

looks like return value int, function argument int

`assert(bitcount(0xffffffff) == 32);` just runs forever with the function declaration int bitcount(int x) { ... }

means that x is not decreasing

shift operators for signed integers does an arithmetic shift which fills in the higher order bits with int. not necessarily c specific, its a 2's complement.

need to tell c to treat as unsigned int
remove the arithmetic properties, just count the bits

## faster

x & x-1 deletes the rightmost bit

rather than looping 32 times, increment count and delete bits

## advanced

what the compiler is capable of
instruction called popcount which can do this in a single instruction
`cc -03 -fomit-frame-pointer -march=native -c bitcount.c`

`objdump -d bitcount.o` to see the disassembly

clang found the instruction popcntl
can make changes where it doesnt pattern match to popcntl

might want to be explicit about using this instruction
can include `#include <nmmintrin.h>` and rather than the function bitcount do `return __builtin_popcount(n);`

if we don't use the architecture flag -march=native, we get a different result. compiler is conservative, wants it to run on any machine, that might not have popcount.
