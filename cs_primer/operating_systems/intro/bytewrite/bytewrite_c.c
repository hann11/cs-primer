#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

// Write a byte to a file

int main() {
    // printf("OK\n");

    // struct stat st;
    // long long int file_size, blocks;
    // int counter = 0;

    // // create an empty file file.txt
    // FILE *f = fopen("file.txt", "w");
    // fclose(f);

    // stat("file.txt", &st);

    // file_size = st.st_size;
    // blocks = st.st_blocks;

    // // create a file file.txt and write 1 byet to it

    // while(counter < 1048577) { // 1MiB
    //     FILE *g = fopen("file.txt", "a");
    //     fputc('a', g);
    //     fclose(g);

    //     stat("file.txt", &st);

    //     // if stat.blocks is incremented, print the number of blocks and the size of the file

    //     if (st.st_blocks > blocks) {
    //         printf("INCREMENT: Size of file: %lld, number of blocks: %lld\n", st.st_size, st.st_blocks);
    //         blocks = st.st_blocks;
    //     }
    //     counter++;
    // }

    int f = open("/tmp/foo", O_WRONLY | O_CREAT | O_TRUNC);
    if (f < 0) {
        perror("open");
        exit(1);
    }
    struct stat st;
    int prior_blocks = -1;
    for (int i = 0; i < 1048577; i++) {
        write(f, ".", 1);
        fstat(f, &st);
        if (st.st_blocks > prior_blocks) {
            printf("Size: %lld, blocks: %lld, on disk: %lld\n, inode: %lld\n", st.st_size, st.st_blocks, st.st_blocks * 512, st.st_ino);
            prior_blocks = st.st_blocks;
        }
    }

}

