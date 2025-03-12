#include <stdio.h>

int main () {

    char *argv[100];

    argv[0] = "hello";
    argv[1] = "world";

    printf("argv[0] %s, argv[1] %s\n", argv[0], argv[1]);
}