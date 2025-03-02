# include <stdio.h>
# include <limits.h>

int main () {
    char a = 'A';
    int b = 121;
    float c = 0.3;
    double d = 0.5;
    long int e = 20L;
    short f = 5;

    unsigned int g = 10;
    unsigned short h = 5;
    unsigned long int i = 20L;

    int j, k = 10;

    int32_t l = 10;

    printf("long max: %ld, int max: %d\n", LONG_MAX, INT_MAX);
    printf("%d, %c\n", b, b);
    printf("%f, %f\n", c, d);
    printf("OK\n");
}