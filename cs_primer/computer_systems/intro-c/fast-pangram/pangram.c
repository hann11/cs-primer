#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>


bool ispangram(char *s) {
  // TODO implement this!

  int bitvec = 0;

  while (*s != '\0') {
    if (isalpha(*s)) { // if alpha
      char lower = tolower(*s); // lowercase it if applicable
      // note think can use ASCII stuff; check if uppercase (between 'A' and 'Z'), then lower it -32
      // then check if between 'a' and 'z'
      bitvec |= (1 << (lower - 'a'));
    }
    s++;
  }
  return bitvec == 0x3ffffff;
}

bool ispangramchar(char *s) {
  char c;
  while (*s != '\0') {
    if (isalpha(*s)) {
      char lower = tolower(*s);
      printf("%c\n", lower);
    }
    c = *s;
    printf("%c\n", c);
    s++;
  }
  return false;
}

int main() {
  size_t len;
  ssize_t read;
  char *line = NULL;
  while ((read = getline(&line, &len, stdin)) != -1) {
    // printf("%s", line);
    // ispangramchar(line);
    if (ispangram(line))
      printf("%s", line);
  }

  if (ferror(stdin))
    fprintf(stderr, "Error reading from stdin");

  free(line);
  fprintf(stderr, "ok\n");
}
