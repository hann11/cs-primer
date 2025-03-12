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

int main() {
    signal(SIGINT, handle_sigint);
    printf("Starting shell, pid is %d\n", getpid());
    char input[MAX_INPUT];
    while (shell_loop < 3) {
        shell_loop++;
        printf("shell > ");
        fgets(input, MAX_INPUT, stdin);

        int argn = 0;

        char *argv[100];

        argv[0] = strtok(input, " ");

        while (argv[argn] != NULL) {
            argn++;
            argv[argn] = strtok(NULL, " ");
        }


        if (strcmp(input, "exit\n") == 0) {
            printf("Exiting shell\n");
            break;
        }

        if (strcmp(input, "help\n") == 0) {
            printf("Default help: just use it!\n");
            continue;
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
            
            execvp(argv[0], argv);

        }

        else {
            perror("failed to fork");
        }
        
    }
}