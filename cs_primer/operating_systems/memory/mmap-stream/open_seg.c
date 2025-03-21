#include <sys/mman.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h> 

int main () {
    int fd = shm_open("/shmobj", O_RDWR);
    // ftruncate(fd, 4096);
    printf("Opened shared memory object with fd %d\n", fd);
    if (fd == -1) {
        perror("shm_open");
        return 1;
    }

    ftruncate(fd, 4096);

    int *arr = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    printf("arr = %p\n", arr);
    printf("arr[0] = %d\n", arr[0]);
    printf("arr[1] = %d\n", arr[1]);

    arr[0] = 1;
    arr[1] = 2;

    close(fd);
}