#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main () {
    int x = 100;

    int rc = fork();

    if (rc < 0) {
        fprintf(stderr, "fork failed\n");
        return 1;
    }
    else if (rc == 0) {
        printf("child x: %d\n", x);
        x = 200;
        printf("child x: %d\n", x);
    }
    else {
        printf("parent x: %d\n", x);
        x = 300;
        printf("parent x: %d\n", x);
    }
    return 0;
}

// output

// parent x: 100
// parent x: 300
// child x: 100
// child x: 200

// fork duplicates the parent process, including the value of x. The child process has its own copy of x, so changing x in the child process does not affect the value of x in the parent process.