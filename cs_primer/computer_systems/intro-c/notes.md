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

## structs in C

group a bunch of variables together - for convenience, or value if you have a bunch of structs like an array of structs, maybe rows in a DB. types vary within the struct. lots might follow the pattern e.g rdb.

consider as objects without methods.

// each struct must be the same size.
// array of structs; c compiler finds fixed size, go to n times that for the nth thing, then find the field

frequently might work on pointers to structs
if invoking functions, passing struct as arg or return value; the entire struct will copy. large struct, it'll copy onto stack taking time/space.
so just reference them
s

syntatic sugar; struct user \* p = &u2;

how are the structs laid out?
age 4bytes, postcode 2bytes, char pointer 8bytes.
struct should be laid out with space (contiguously)

```
printf("%p %p %p %p\n", &u, &(u.age), &(u.postcode), &(u.name)); // mem locs
```

```
0x16f8ff240 0x16f8ff240 0x16f8ff244 0x16f8ff248
```

age at the start of the struct location.
short should be 2bytes but its 4bytes in after age. just so the char pointer 8bytes is properly aligned! compiler takes care of it

struct just lays out data in memory, nice to access things by name.

array of structs would be nice.

consider how the arrays are laid out too. C needs to be able to do this referencing in constant time, say array of ararys (multid array of structs)
don't want to iterate thru. thus need fixed size, contiguous layout for constant time indexing.
compiler figures out struct size, how to get to start, then how to address postcode for example.

## malloc

c standard lib function

can manage heap memory.

not a syscall, but might perform syscalls if needs more space from the OS.

given your heap, large amount of ubnstructured space. might want to use some of that space and not care about whats used around it.
stack is for fn locals

if u want 10bytes somewhere, malloc will find it. gives you 10bytes free, gives starting byte location, as a void pointer.

how it works; linked list (free list) if you had a notion of the avail regions of memory, you can have a structure to allocate over free space for the user to store data.
when something is freed from malloc, add a node to the free list. it won't clear the mem, just shows mem alloc theres afree spot for xbytes next time.

complicatons with multithreads, we'll mayb see this in OS.

## void pointer

might want a situation that something is a given type. dynamic typing; don't need to worrya bout it. consider python

l = [1, 3.4, "foo", []] <- any python object can go in a list or dict values.

```
class Box:
    def __init__(self, name, value): # dont specify types
        self.name = name
        self.value = value
```

b = Box("foo", 3)
b2 = Box("bar", b) - can literally do anything with the types bc its not strictly typed

type system to protect or compiler needs to lay things out in memory in particular

in C can be generic by working with memory addresses. The Void pointer does this. Doesn't care about the type.

C compiler gives 8bytes for a pointer

```
voids.c:12:39: warning: format specifies type 'char *' but the argument has type 'void *' [-Wformat]
    printf("values are: %s and %d\n", b1.value, b2.value); // need to know the actual type for printing
```

cast to char pointer to fix.

wnt to be generic; array to contain anything; need to use generic pointers. cast to type just as you need it.

eg2. hypothetically; alot of thought into quicksort, its a good impl. did it over integers. do you need another quicksort over strings or floats? core logic implemented. want to use it generically.
solvable with voids.

man 3 qsort

qsort fn;
qsort of anything (void \*base) - notjust voids 8bytes, or structs 20/32bytes, int 4bytes. variable length.
\*base is the generic pointer to array of "things", just a memory address. needs to know how many elements in the array, and how big each one is.

say array of 10 32bit ints. size_t nel is 10, size_t width is 4. then qsort can operate over anytype. looks at byte byte byte, compare.

howto compare strings?
qsort expects you to provide reference to comparison function , int (\*compare), must be afunction that accepts two args, two strings / ints, accepts as void pointers, and then applies.

just suply a comparsion fn like string compare, int compare etc - requires work but the logic for quicksort is generic. pretty nice.

rememb; void pointer is specific name, diff to the name void for fn. indication to compiler that this is an address, but not a typed pointer or address to specific thing.
