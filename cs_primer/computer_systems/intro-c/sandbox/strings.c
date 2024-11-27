#include <stdio.h>

void print_string(char *s) {
    char c;
    while (*s != '\0') {
        c = *s;
        printf("%p\n", s);
        printf("%c\n", c);
        s++;
    }
}

int main() {
    print_string("hello sir my name is dallet");
}