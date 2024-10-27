#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>


bool ispangram(char *s) {
  // TODO implement this!

  uint32_t bs = 0; // good to be explicit about bit size here
  char c;
  while (*s != '\0') { // dereference the pointer (*s gives the value at that memory location)
    c = tolower(*s++); // post increment, it does tolower on *s then increments after.
    if (c < 'a' || c > 'z') continue; // ascii values are in order for alphabets. won't work with upper and lower mix
    bs |= 1 << (c - 'a'); // will be an integer in range 0-25 inclusive.
  }
  return bs == 0x3ffffff;
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
