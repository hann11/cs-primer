// spawn a basic "shell" and take in text and echo back with fgets and printf

#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <signal.h>

#define MAX_INPUT 4096

int shell_loop = 0;
volatile int currentpid = 0;

void handle_sigint(int sig) {

    if (kill(currentpid, SIGKILL) == 0) {
        printf("Killed child process %d\n", currentpid);
    }
    else {
        printf("Failed to kill process %d\n", currentpid);
    }
}

int do_pipe (char *argv[], int argn) {
    int j = 0;
    while (j < argn) {
        if (strcmp("|", argv[j]) == 0) {
            return j;
        }
        j++;
    }
    return 0;
}

int exc_pipe ()

int main() {
    signal(SIGINT, handle_sigint);
    printf("Starting shell, pid is %d\n", getpid());
    char input[MAX_INPUT];
    while (shell_loop < 3) {
        shell_loop++;
        printf("shell > ");
        fgets(input, MAX_INPUT, stdin);

        if (strcmp(input, "exit\n") == 0) {
            printf("Exiting shell\n");
            break;
        }

        if (strcmp(input, "help\n") == 0) {
            printf("Default help: just use it!\n");
            continue;
        }

        int argn = 0;

        char *argv[100];

        argv[0] = strtok(input, " \t\n");

        while (argv[argn] != NULL) {
            argn++;
            argv[argn] = strtok(NULL, " \t\n");
        }

        

        // fork
        currentpid = fork();

        if (currentpid > 0) {
            // parent
            int status;
            waitpid(currentpid, &status, 0);
        }

        else if (currentpid == 0) {
            // child
            int do_pipe_true = do_pipe(argv, argn);

            if (do_pipe_true > 0) {

                int pipe_idx = do_pipe_true + 1;

                int m = 0;

                // todo need first part to pass


                //second part.
                char *pipe_args[5];
                while (pipe_idx < argn) {
                    pipe_args[m] = argv[pipe_idx];
                    m++;
                    pipe_idx++;

                }
                pipe_args[m] = NULL;

                execvp(pipe_args[0], pipe_args);
                
            }
            else {
                // printf("no pipe\n");
                execvp(argv[0], argv);
            }
            

        }

        else {
            perror("failed to fork");
        }
        
    }
}