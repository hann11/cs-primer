# include <stdio.h>
# include <stdlib.h>

int main() {
    int sts;
    sts = system("ls");
    printf("sts = %d\n", sts);
}