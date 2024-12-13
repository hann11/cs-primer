#include <assert.h>
#include <stdio.h>

extern int fac(int n);

int main(void) {
  assert(fac(0) == 1);
  assert(fac(1) == 1);
  assert(fac(2) == 2);
  assert(fac(3) == 6);
  assert(fac(5) == 120);
  assert(fac(10) == 3628800);
  printf("OK\n");
}
