#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>

int main () {
    // implement ls | wc | wc using pipe syscall (and another syscall dup2 to link pipe)
    int fildes[2];
    if (pipe(fildes) != 0) {
        perror("pipe error");
    } // set up the pipe

    printf("fildes[0]: %d, fildes[1]: %d\n", fildes[0], fildes[1]);

    pid_t pid = fork();
    if (pid == 0) {
        // child

        // setup to write to stdout (1)?
        close(fildes[0]); // close stdin in this child process as fork duplicates it
        dup2(fildes[1], 1); // duplicate the pipe out to stdout

        execlp("ls", "ls", NULL);
    }

    // setup to read to stdin (0) from pipe?
    close(fildes[1]);

    int status = 0;
    waitpid(pid,&status, 0); // wait for the child (ls)

    int fildes_2[2]; // second pipe
    if (pipe(fildes_2) != 0) {
        perror("pipe failed");
    }

    pid = fork();
    if (pid == 0) {
        close(fildes_2[0]);
        dup2(fildes[0], 0); // copied from parent which has pipe stdout from ls in 1
        dup2(fildes_2[1], 1); // where we write to

        execlp("wc", "wc", NULL);

    }

    close(fildes_2[1]);

    status = 0;
    waitpid(pid, &status, 0);

    dup2(fildes_2[0], 0); // duplicate pipe in to stdin.. whys this neede d? 

    execlp("wc", "wc", NULL); // execute from parent.
}