#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

bool ispangram(char *s) {

  int bitvec = 0;
  char c;

  while (*s != '\0') { // deference the pointer
    c = *s;
    if ('A' <= c && c <= 'Z') { // convert to lower case
      c += 32;
    }
    if ('a' <= c && c <= 'z') {
      bitvec |= (1 << (c - 'a'));
    }
    s++;
  }
  return bitvec == 0x3ffffff;
}

int main() {
  size_t len;
  ssize_t read;
  char *line = NULL;
  while ((read = getline(&line, &len, stdin)) != -1) {
    if (ispangram(line))
      printf("%s", line);
  }

  if (ferror(stdin))
    fprintf(stderr, "Error reading from stdin");

  free(line);
  fprintf(stderr, "ok\n");
}
