#include <assert.h>
#include <stdio.h>

extern int call_add(int a, int b);

int main(void) {
  assert(call_add(5, 10) == 15);
  assert(call_add(1, 2) == 3);
  printf("OK\n");
}
