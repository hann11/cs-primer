# include <stdio.h>

// int main () {
//     int n = 5;
//     int *p = &n;

//     int foo = *p;
//     printf("n = %d, &n = %p\n", foo, p);
// }

// int main () {
//     int arr[10];

//     arr[3] = 42;

//     printf("arr[-2] = %d\n", arr[-2]);
//     // printf("arr = %p, arr+1 = %p\n", arr, arr+1);
// }

int main () {
    int n = 5;
    int *p = &n;
    int **q = &p;
    int ***r = &q;

    printf("n = %d, *p = %p, **q = %p, ***r = %p\n", n, p, q, r);
}