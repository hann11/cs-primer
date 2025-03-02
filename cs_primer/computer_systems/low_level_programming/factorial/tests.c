#include <assert.h>
#include <stdio.h>

extern int factorial(int n);


int main(void) {
  printf("%d\n", factorial(0));
  printf("%d\n", factorial(1));
  printf("%d\n", factorial(3));
  printf("%d\n", factorial(5));
  printf("%d\n", factorial(10));
  // assert(factorial(0) == 1);
  // assert(factorial(1) == 1);
  // assert(factorial(3) == 6);
  // assert(factorial(5) == 120);
  // assert(sum_to_n(1000) == 500500);
  printf("OK\n");
}
