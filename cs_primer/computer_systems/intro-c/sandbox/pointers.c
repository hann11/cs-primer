# include <stdio.h>

// int main () {
//     int n = 5;
//     int *p = &n;

//     int foo = *p;
//     printf("n = %d, foo = %d, &n = %p\n", n, foo, p);
// }

int main () {
    int arr[10];

    arr[3] = 42;
    arr[1] = 10;

    // printf("arr[-2] = %d\n", arr[-2]);
    printf("arr = %p, arr+1 = %p\n", arr, arr+1);
    printf("*arr = %d, *(arr+1) = %d\n", *arr, *(arr+1));
}

// int main () {
//     int n = 5;
//     int *p = &n;
//     int **q = &p;
//     int ***r = &q;

//     printf("n = %d, *p = %p, **q = %p, ***r = %p\n", n, p, q, r);
// }