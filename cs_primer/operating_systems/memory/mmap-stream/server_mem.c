#include <stdlib.h>
#include <stdio.h>
#include <sys/socket.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

#define SIZE (1 << 14) // Test with this many bytes of data

int main () {
  int checksum, max, sock, conn, n;
  unsigned short port = 9876;
  struct sockaddr_in self, client;
  unsigned int clientlen;

  srand(0x1234);
  max = SIZE / sizeof(int);

  // construct the server socket, bind and listen for connections
  sock = socket(AF_INET, SOCK_STREAM, 0);
  memset(&self, 0, sizeof(self));
  self.sin_family = AF_INET;
  self.sin_addr.s_addr = htonl(INADDR_ANY);
  self.sin_port = htons(port);
  bind(sock, (struct sockaddr *)&self, sizeof(self));
  listen(sock, 10);

  int fd = shm_open("/shmobj", O_RDWR);

  printf("Opened shared memory object with fd %d\n", fd);
  if (fd == -1) {
      perror("shm_open");
      return 1;
  }

  ftruncate(fd, SIZE);
  

  int *arr = mmap(NULL, SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  printf("arr = %p\n", arr);
  printf("arr[0] = %d\n", arr[0]);

  close(fd);

  // accept a new connection and stream it a bunch of random integers
  for (;;) {
    conn = accept(sock, (struct sockaddr *)&client, &clientlen);
    printf("Connection accepted\n");
    checksum = 0;
    for (int i = 0; i < max; i++) {
      n = rand();
      checksum ^= n;
      // send(conn, &n, 4, 0);
      arr[i] = n;
    }
    printf("Sent %d random ints to client, checksum %d\n", max, checksum);
  }
}
