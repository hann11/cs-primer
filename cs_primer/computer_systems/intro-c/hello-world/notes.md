if you try compile an empty C file, `cc test.c``

```
Undefined symbols for architecture arm64:
  "_main", referenced from:
      <initial-undefines>
ld: symbol(s) not found for architecture arm64
clang: error: linker command failed with exit code 1 (use -v to see invocation)
```

you need an entrypoint, a main function.

`cc` means for c compiler. attempts to construct an executable file

clang is a driver to do a few tings with C, we will revisit

Entrypoint: main function `int main() {}`. If compile this, it will work. You get a file ./a.out.

use the -o flag to write to a diff filename: `cc test.c -o test` will write to the file ./test

why does the entrypoint have the int return value? unix derived OS make use of an integer exit code. 0 is success, non-zero is non-success.

if you run `./test && echo 'foo'`, returns `foo`

if edit the main function to `int main() { return 1; }`, returns nothing, because we returned non-zero. That's why we have int in function.

If one writes and **compiles** and runs `int main() { printf("Hello, World!\n");}`, we get the error

```
test.c:1:13: error: call to undeclared library function 'printf' with type 'int (const char *, ...)'; ISO C99 and later do not support implicit function declarations [-Wimplicit-function-declaration]
int main() {printf("Hello, World!\n");}
            ^
test.c:1:13: note: include the header <stdio.h> or explicitly provide a declaration for 'printf'
1 error generated.
```

^ We need to include header that includes the function printf. There aren't really builtin functions in C.
One can look at printf in the manual `man 3 printf`. Need to write the 3, otherwise gives a diff CLI utility.

Note `printf` doesn't include carriage return implicitly.
