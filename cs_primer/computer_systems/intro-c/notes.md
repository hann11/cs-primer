https://learnxinyminutes.com/docs/c/

## type definitions and literals

C types arent about programming safeguard
its more for the compiler to do diff things based on the type

`char a = 'A';` one byte value
`int b;`
`float c;`
`double d;`

### character

```
# include <stdio.h>

int main () {
    char a = 'A';
    printf("%d\n", a);
    printf("OK\n");
}
```

returns

```
65
ok
```

defined as a char, but returns a 1 byte integer.
however can print as character
printf("%c\n", a); returns `A`
printf("%d, %c\n", a, a); returns '65, A'

'A' is shorthand for the integer 65
can also do char a = 65; and the above still works

### int

meant to be the natural integer for your system, which changes one system to another.

one can do

```
int main () {
    char a = 'A';
    int b = 65;
    printf("%d, %c\n", b, b);
    printf("OK\n");
}
```

returns the same as above for the A char. The only difference is the size in bytes.

Ints can also be defined in hexadecimal (0xf) -> not ascii so won't print the character

Can also do octal: 033

Binary not in the spec.

### floats and doubles

```
int main () {
    char a = 'A';
    int b = 121;
    float c = 0.3;
    double d = 0.5;
    printf("%d, %c\n", b, b);
    printf("%f, %f\n", c, d);
    printf("OK\n");
}
```

```
121, y
0.300000, 0.500000
OK
```

there are keywords long and short for int
if something small enough to fit into an int;
`long int e = 20L;`
can also omit the int

can also do short int f = 5, and omit int

short/long is machine dependent
weird to have this flexibility

short should be <= int <= long

int atleast 16 bits, long atleast 32 bits,

to understand a bit further:

input:
`printf("long max: %d, int max: %d\n", LONG_MAX, INT_MAX);`
output:

```
types.c:12:43: warning: format specifies type 'int' but the argument has type 'long' [-Wformat]
    printf("long max: %d, int max: %d\n", LONG_MAX, INT_MAX);
                      ~~                  ^~~~~~~~
                      %ld
/Library/Developer/CommandLineTools/usr/lib/clang/15.0.0/include/limits.h:47:19: note: expanded from macro 'LONG_MAX'
#define LONG_MAX  __LONG_MAX__
                  ^~~~~~~~~~~~
<built-in>:47:22: note: expanded from macro '__LONG_MAX__'
#define __LONG_MAX__ 9223372036854775807L
                     ^~~~~~~~~~~~~~~~~~~~
1 warning generated.
```

returns
`long max: -1, int max: 2147483647`
-1 due to overflow

note it still compiles, but with the warning.
one can change to
`printf("long max: %ld, int max: %d\n", LONG_MAX, INT_MAX);`

and returns
`long max: 9223372036854775807, int max: 2147483647`

can also do unsigned qualifiers

can do c declaration to have more than one variable

## loops

while and for are interchangeable

```
int main () {
    int n = 5;
    while (n) { // evaluate if nonzero
        printf("%d\n", n); // continue if nonzero
        n--;
    }
    printf("ok\n");
}
```

even if you start with n = 0, you can run the loop once

```
int main () {
    int n = 0;
    do {
        printf("%d\n", n);
        n--;
    } while (n > 0);
    printf("ok\n");
}
```

when will you use a for loop?

```
int main () {
    for (int i = 0; i < 5; i++) { // int i = 0 is the initialisation
        printf("%d\n", i);
    }
    printf("ok\n");
}
```

for and while will give the same machine code

do while will have diff machine code

## compiler flags

## pointers and arrays

consider memory for a process as a long set of cells
0 to 2^(32, 48, whatever)
each byte is a spot in memory

if there is an int at spot 40, it'll take 4 bytes (40, 41,42,43) store the value of n = 5

you can also refer to n by it's location
say a function will modify n in place - impossible if you just pass n into a function.
the n will just be copied and won't update the n at spot 40 inplace.
need to pass the memory address inc(&n) <- get the location of n. the value is still 5. inc can then de-reference that, change it, etc.

if you have an indeterminate length thing like a string, quite hard to not do anything but point to the start.

can dereference the pointer and follow it.
if two functions operate on a string, normally referencing the starting location of the first byte.

if we run

```
# include <stdio.h>

int main () {
   int n = 5;
   printf("n = %d, &n = %p\n", n, &n);
}
```

returns

```
n = 5, &n = 0x16d52b21c
```

&n is the memory address of n

we can follow and de-reference it.

we can declare a pointer under int n = 5;
`int *p = &n;`

we can also get and dereference a pointer
`int foo = *p`
print foo, returns 5.

diff name for the same physical thing in memory
retreivd from address
see the basic operation of obatining address and dereferencing

### arrays

arrays are syntax for pointers basically

think array as name of starting location for a thing

```
int main () {
    int arr[10];

    printf("arr = %p, arr+1 = %p\n", arr, arr+1);
}
```

returns the in memory address of arr, then arr + 1 which is 4 bytes more than arr. takes to the next integer.

```
int main () {
    int arr[10];

    arr[3] = 42;

    printf("arr[3] = %d\n", arr[3]);
    // printf("arr = %p, arr+1 = %p\n", arr, arr+1);
}
```

syntax says take the location of this sequence of integers in memory
the integers i the array are sequential in memory
arr[3] will be 42.

if we print arr + 3, we will get the memory address of arr + 3 ( 12 bytes in bc ints)
if we print \*(arr+3), we will get the actual value of arr[3] = 42

## macros/preprocessor

define functions/macros, it'll replace the text where you call it in the code as a preprocessing step bfore compiling

conditional inclusing

#define DEBUG 1

it'll do the below
#if DEBUG ==1
do xyz
#endif
