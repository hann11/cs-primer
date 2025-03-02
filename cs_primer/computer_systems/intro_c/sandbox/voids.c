#include <stdio.h>

struct Box {
    char* name;
    void* value; // can be anything. definitely an address. follow address to get value, can be of any type
};

int main () {
    struct Box b1 = {"foo", "box"};
    int n = 5;
    struct Box b2 = {"bar", &n}; //can't put 2nd val as integer, must be void pointer, address to ANYTHING.
    printf("values are: %s and %d\n", (char*)b1.value, *(int*)b2.value); // need to know the actual type for printing
    printf("ok\n");
}