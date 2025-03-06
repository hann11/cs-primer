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
        printf("Killed process %d\n", currentpid);
    }
    else {
        printf("Failed to kill process %d\n", currentpid);
    }
}


int do_command(char *filepath, char *input) {
    char *argv[] = { filepath, input, NULL };
    execvp(filepath, argv);
    return 0;
}

int main() {
    signal(SIGINT, handle_sigint);
    printf("Starting shell, pid is %d\n", getpid());
    char input[MAX_INPUT];
    while (shell_loop < 3) {
        shell_loop++;
        printf("shell > ");
        fgets(input, MAX_INPUT, stdin);
        // printf("Your input was %s", input);

        char *command, *do_what_with;
        command = strtok(input, " ");
        do_what_with = strtok(NULL, " ");


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

        else {
            // child
            
            if (strcmp(command, "echo") == 0) {
                printf("%s", do_what_with);
                return 0;
            }
            if (strcmp(command, "sleep") == 0) {
                int res = do_command(command, do_what_with);
                return 0;
            }
            else {
                printf("Command not found\n");
                return 1;
            }
        }
        
    }
}