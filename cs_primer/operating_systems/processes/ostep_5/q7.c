#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main () {

    close(STDOUT_FILENO);

    printf("opening pid %d\n", getpid());

    int rc = fork();

    if (rc < 0) {
        fprintf(stderr, "fork failed\n");
        return 1;
    }
    else if (rc == 0) {
        // close(STDOUT_FILENO);
        printf("child pid %d\n", getpid());
    }
    else {
    }
    return 0;
}

// output

// parent x: 100
// parent x: 300
// child x: 100
// child x: 200

// fork duplicates the parent process, including the value of x. The child process has its own copy of x, so changing x in the child process does not affect the value of x in the parent process.