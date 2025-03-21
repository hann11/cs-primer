#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

#define SIZE (1 << 13) // Test with this many bytes of data

int main () {
  int checksum, max, sock, n;
  unsigned short port = 9876;
  struct timespec start, end;
  struct sockaddr_in server;

  max = SIZE / sizeof(int);

  // construct the client socket, and connect
  sock = socket(AF_INET, SOCK_STREAM, 0);
  memset(&server, 0, sizeof(server));
  server.sin_family = AF_INET;
  server.sin_addr.s_addr = inet_addr("127.0.0.1");
  server.sin_port = htons(port);
  connect(sock, (struct sockaddr *)&server, sizeof(server));

  int fd = shm_open("/shmobj", O_RDWR);

  printf("Opened shared memory object with fd %d\n", fd);
  if (fd == -1) {
      perror("shm_open");
      return 1;
  }

  int *arr = mmap(NULL, SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  printf("arr = %p\n", arr);
  printf("arr[0] = %d\n", arr[0]);
  
  close(fd);

  // receive a bunch of data
  clock_gettime(CLOCK_MONOTONIC, &start);
  checksum = 0;
  for (int i = 0; i < max; i++) {
    n = arr[i];
    checksum ^= n;
    // recv(sock, &n, 4, 0);
  }
  clock_gettime(CLOCK_MONOTONIC, &end);

  float secs =
      (float)(end.tv_nsec - start.tv_nsec) / 1e9 + (end.tv_sec - start.tv_sec);
  float mibs = (float)SIZE / secs / (1 << 20);

  printf("Received at %.3f MiB/s. Checksum: %d\n", mibs, checksum);
}
