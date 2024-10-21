https://learnxinyminutes.com/docs/c/

## type definitions and literals

C types arent about programming safeguard
its more for the compiler to do diff things based on the type

`char a = 'A';` one byte value
`int b;`
`float c;`
`double d;`

# character

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

# int

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

# floats and doubles

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
long int e = 20L;
can also omit the int

can also do short int f = 5, and omit int

short/long is machine dependent
weird to have this flexibility

short should be <= int <= long

int atleast 16 bits, long atleast 32 bits,

to understand a bit further:
