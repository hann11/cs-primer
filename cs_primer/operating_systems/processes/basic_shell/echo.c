#include <stdio.h>
#include <unistd.h>

int main ()
{

    char *filepath = "/bin/echo"; // /bin/sleep
    char *argv[] = { filepath, "Hello twiz", NULL }; // "5", NULL

    execve (filepath, argv, NULL);
  
  return 0;
}