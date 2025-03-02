#include <stdio.h>

int frame_count = 0;

// int foo(int *n) {
//     frame_count++;
//     printf("frame count: %d\n", frame_count);

//     printf("n = %p\n", n);
//     printf("&n = %p\n", &n);

//     int m = *n;

//     int j = m + 1;


//     if (frame_count == 5) {
//         return 0;
//     }

//     return foo(&j);
// }

// int main () {
//     int p = 0;
//     int f = foo(&p);
// }


void foo(int n, long int stack_start) {

    if (n%10000 == 0) {
        // printf("stack pos: %p\n", &n);
        printf("frame count: %d\n", n);
        // printf("stack start: %ld\n", stack_start);

        // printf("stack size: %ld\n", stack_start - (long)&n);
    }

    foo(n+1, stack_start);
}

int main () {
    int n = 0;
    foo(n, (long)&n);
}