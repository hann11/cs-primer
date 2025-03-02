#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
// #include <sys/types.h>

#define SLEEP_SEC 0
#define NUM_MULS 10000
#define NUM_MALLOCS 100
#define MALLOC_SIZE 100

// TODO define this struct
struct profile_times {
  int process_id;
};

// TODO populate the given struct with starting information
void profile_start(struct profile_times *t) {
  t->process_id = getpid();
}

// TODO given starting information, compute and log differences to now
void profile_log(struct profile_times *t) {
  printf("Process ID: %d\n", t->process_id);
}

int main(int argc, char *argv[]) {
  struct profile_times t;

  // TODO profile doing a bunch of floating point muls
  float x = 1.0;
  printf("Multiplying %d times\n", NUM_MULS);
  profile_start(&t);
  for (int i = 0; i < NUM_MULS; i++)
    x *= 1.1;
  profile_log(&t);

  // TODO profile doing a bunch of mallocs
printf("Mallocing %d times\n", NUM_MALLOCS);
  profile_start(&t);
  void *p;
  for (int i = 0; i < NUM_MALLOCS; i++)
    p = malloc(MALLOC_SIZE);
  profile_log(&t);

  // TODO profile sleeping
  printf("Sleeping for %d seconds\n", SLEEP_SEC);
  profile_start(&t);
  sleep(SLEEP_SEC);
  profile_log(&t);
}
