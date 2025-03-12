#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>

int main () {
    // implement ls | wc using pipe syscall (and another syscall to link pipe)

    pid_t pid = fork();

    if (pid == 0) { // do it in the child

        int fildes[2];
        if (pipe(fildes) != 0) {
            perror("pipe error");
        } // set up the pipe

        pid_t pid_fork = fork();
        if (pid_fork == 0) {
            // child

            // setup to write to stdout (1)?
            close(fildes[0]); // close stdin in this process as fork duplicates it
            dup2(fildes[1], 1); // duplicate the pipe out to stdout

            execlp("ls", "ls", NULL);
        }

        // setup to read to stdin (0) from pipe?
        close(fildes[1]);

        int status = 0;
        waitpid(pid_fork,&status, 0); // wait for the child (ls)

        dup2(fildes[0], 0); // duplicate pipe in to stdin.. whys this neede d? 

        execlp("wc", "wc", NULL); // execute from parent.

    }

    else {
        int status = 0;
        waitpid(pid, &status, 0);
    }
}