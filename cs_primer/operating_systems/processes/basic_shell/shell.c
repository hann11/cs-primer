// spawn a basic "shell" and take in text and echo back with fgets and printf

#include <stdio.h>
#include <unistd.h>

#define MAX_INPUT 4096

int main() {
    char input[MAX_INPUT];
    while (1) {
        printf("shell> ");
        // fgets(input, MAX_INPUT, stdin);
        // printf("%s", input);
        printf("forking and execing sleep 5\n");
        int pid = fork();
        printf("pid: %d\n", pid);

        if (pid == 0) {
            printf("child process\n");
            execlp("sleep", "sleep", "5", NULL);
        } else {
            printf("parent process\n");
        }
    }
}