#include <stdio.h>

struct user {
    int age;
    short postcode;
    char* name; // name is a characer pointer. name will reside somewhere else.
};
// each struct must be the same size.
// array of structs; c compiler finds fixed size, go to n times that for the nth thing, then find the field


int main () {
    struct user u = {
        25, 10000, "Johnson bronson"
    };
    struct user u2 = {
        17, 20000, "Daniel"
    };
    struct user *p = &u2;
    printf("%s is %d years old and lives in postcode %d\n", u.name, u.age, u.postcode);
    printf("%s is %d years old and lives in postcode %d\n", p->name, p->age, p->postcode);

    printf("%p %p %p %p\n", &u, &(u.age), &(u.postcode), &(u.name)); // mem locs

    struct user users[2] = {1, 10000, "Johnfefgwegergegr", 2, 20000, "Daniel"};

    printf("%s is %d years old and lives in postcode %d\n", users[0].name, users[0].age, users[0].postcode);

    printf("one Struct is %lu bytes\n", sizeof(struct user)); // 4 + (2 +2 for pad) + 8 = 16
    printf("users array is at %p, \%s\ is located at %p\n", users, users[1].name, &users[1].name);
    // users array is at 0x16b413220, Daniel is located at 0x16b413238 18 hex = 24 dec -> 16 + 8 = 24
    printf("ok\n");
    // user name is just a POINTER, always 8 bytes. so johnefewgeughe can be a name, its stored somewher else and is variable length.
}