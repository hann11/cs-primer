#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/mman.h>

// plan
// 1. formulate what expect to see after running this base code (before TODO)
// associate n = 0 in memory in the base process
// fork (duplicate) parent process, get new memory mappings for child (diff physical memory)
// in child: write n = rand() to the location of n in (virutal??) memory
// n in child will be the rand int, &n will be a virutal memory loc
// in parent, n will be zero, &n will be the same? virtual memory location

// what heppens: child writes and READS rand() int to address x
// parent reads 0 from address x
// address x is mapped to different physical memory in parent and child, but same "virtual" address

// plan:
// designate a spot in physical memory that will point to same virtual mem in parent and child
// do this mmap in the root before forking, so parent and child share it
// use relevant mmap() args to achieve this
// man 2 mmap (returns a void pointer to mem loc)
// just need an integer worth of memory
// void * mmap(void *addr, size_t len, int prot, int flags, int fd, off_t offset);
// *addr; don't care (NULL)
// size_t: sizeof(int)
// prot: (protections): allow read and write (PROT_READ | PROT_WRITE)
// flags: MAP_SHARED (share mods)
// fd: don't care (-1)
// off_t: 0

// once got this pointer obj, write the integer to there in child (parent should have same map)
//points to same physical mem in parent and child.


int n = 0;

int main () {
  int stat;
  srand(time(NULL));

  int *ptr = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANON, -1, 0);
  printf("mmap ptr: %p\n", ptr);

  if (fork() == 0) {
    // as the child, write a random number to shared memory (TODO!)
    *ptr = rand();
    printf("Child has written %d to address %p\n", *ptr, ptr);
    exit(0);
  } else {
    // as the parent, wait for the child and read out its number
    wait(&stat);
    printf("Parent reads %d from address %p\n", *ptr, ptr);
  }
}
