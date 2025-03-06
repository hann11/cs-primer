#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>

int main(int arg, char *argv[]) {
    printf("opening pid %d\n", getpid());
    int rc = fork();
    if (rc < 0) {
        fprintf(stderr, "fork failed\n");
        exit(1);
    }
    else if (rc == 0) {
        close(STDOUT_FILENO);
        // open("./p3.output", O_CREAT|O_WRONLY|O_TRUNC, S_IRWXU);
        printf("child pid %d\n", getpid());
        char *myargs[3];
        myargs[0] = strdup("wc");
        myargs[1] = strdup("p3.c");
        myargs[2] = NULL;
        execvp(myargs[0], myargs);
        printf("this shouldn't print");
    }
    else {
        int wc = wait(NULL);
        printf("parent pid %d\n", getpid());
    }
    return 0;
}