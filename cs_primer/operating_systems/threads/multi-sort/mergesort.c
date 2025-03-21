#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#include "cputime.h"

void merge(int *arr, int n, int mid) {
  int left = 0, right = mid, i;
  int *x = malloc(n * sizeof(int));
  // copy the ith item from either the left or right part
  for (i = 0; i < n; i++) {
    if (right == n)
      x[i] = arr[left++];
    else if (left == mid)
      x[i] = arr[right++];
    else if (arr[right] < arr[left])
      x[i] = arr[right++];
    else
      x[i] = arr[left++];
  }
  // transfer from temporary array back to given one
  for (i = 0; i < n; i++)
    arr[i] = x[i];
  free(x);
}

void msort(int *arr, int n) {
  if (n < 2)
    return;
  int mid = n / 2;
  msort(arr, mid);
  msort(arr + mid, n - mid);
  // sort the two halves
  merge(arr, n, mid);
}

struct msort {
  int *arr;
  int n;
};

void *msort_thread(void *arg) {
  // Cast the void * arg to struct msort *
  struct msort *data = (struct msort *)arg;
  // Access data in struct
  msort(data->arr, data->n);
  return NULL;
}

// basic idea: thread msort based on half the array.

int main () {
  int n = 1 << 24;
  int *arr = malloc(n * sizeof(int));
  // populate array with n many random integers
  srand(1234);
  for (int i = 0; i < n; i++)
    arr[i] = rand();

  fprintf(stderr, "Sorting %d random integers\n", n);

  // actually sort, and time cpu use
  struct profile_times t;
  profile_start(&t);


  // create 4 threads
  struct msort data1 = {arr, n / 4};
  struct msort data2 = {arr + n / 4, n / 4};
  struct msort data3 = {arr + n / 2, n / 4};
  struct msort data4 = {arr + 3 * n / 4, n / 4};

  pthread_t thread1, thread2, thread3, thread4;
  pthread_create(&thread1, NULL, msort_thread, &data1);
  pthread_create(&thread2, NULL, msort_thread, &data2);
  pthread_create(&thread3, NULL, msort_thread, &data3);
  pthread_create(&thread4, NULL, msort_thread, &data4);

  pthread_join(thread1, NULL);
  pthread_join(thread2, NULL);
  pthread_join(thread3, NULL);
  pthread_join(thread4, NULL);

  merge(arr, n / 2, n / 4);
  merge(arr + n / 2, n / 2, n / 4);

  merge(arr, n, n / 2);

  // create 2 threads

  // struct msort data1 = {arr, n / 2};
  // struct msort data2 = {arr + n / 2, n / 2};


  // pthread_t thread1, thread2;
  // pthread_create(&thread1, NULL, msort_thread, &data1);
  // pthread_create(&thread2, NULL, msort_thread, &data2);

  // pthread_join(thread1, NULL);
  // pthread_join(thread2, NULL);

  // merge(arr, n, n / 2);


  // //create 8 threads

  // struct msort data1 = {arr, n / 8};
  // struct msort data2 = {arr + n / 8, n / 8};
  // struct msort data3 = {arr + 2 * n / 8, n / 8};
  // struct msort data4 = {arr + 3 * n / 8, n / 8};
  // struct msort data5 = {arr + 4 * n / 8, n / 8};
  // struct msort data6 = {arr + 5 * n / 8, n / 8};
  // struct msort data7 = {arr + 6 * n / 8, n / 8};
  // struct msort data8 = {arr + 7 * n / 8, n / 8};

  // pthread_t thread1, thread2, thread3, thread4, thread5, thread6, thread7, thread8;

  // pthread_create(&thread1, NULL, msort_thread, &data1);
  // pthread_create(&thread2, NULL, msort_thread, &data2);
  // pthread_create(&thread3, NULL, msort_thread, &data3);
  // pthread_create(&thread4, NULL, msort_thread, &data4);
  // pthread_create(&thread5, NULL, msort_thread, &data5);
  // pthread_create(&thread6, NULL, msort_thread, &data6);
  // pthread_create(&thread7, NULL, msort_thread, &data7);
  // pthread_create(&thread8, NULL, msort_thread, &data8);

  // pthread_join(thread1, NULL);
  // pthread_join(thread2, NULL);
  // pthread_join(thread3, NULL);
  // pthread_join(thread4, NULL);
  // pthread_join(thread5, NULL);
  // pthread_join(thread6, NULL);
  // pthread_join(thread7, NULL);
  // pthread_join(thread8, NULL);

  // merge(arr, n / 4, n / 8);
  // merge(arr + n / 4, n / 4, n / 8);
  // merge(arr + n / 2, n / 4, n / 8);
  // merge(arr + 3 * n / 4, n / 4, n / 8);

  // merge(arr, n / 2, n / 4);
  // merge(arr + n / 2, n / 2, n / 4);

  // merge(arr, n, n / 2);

  // // 16 threads

  // struct msort data1 = {arr, n / 16};
  // struct msort data2 = {arr + n / 16, n / 16};
  // struct msort data3 = {arr + 2 * n / 16, n / 16};
  // struct msort data4 = {arr + 3 * n / 16, n / 16};
  // struct msort data5 = {arr + 4 * n / 16, n / 16};
  // struct msort data6 = {arr + 5 * n / 16, n / 16};
  // struct msort data7 = {arr + 6 * n / 16, n / 16};
  // struct msort data8 = {arr + 7 * n / 16, n / 16};
  // struct msort data9 = {arr + 8 * n / 16, n / 16};
  // struct msort data10 = {arr + 9 * n / 16, n / 16};
  // struct msort data11 = {arr + 10 * n / 16, n / 16};
  // struct msort data12 = {arr + 11 * n / 16, n / 16};
  // struct msort data13 = {arr + 12 * n / 16, n / 16};
  // struct msort data14 = {arr + 13 * n / 16, n / 16};
  // struct msort data15 = {arr + 14 * n / 16, n / 16};
  // struct msort data16 = {arr + 15 * n / 16, n / 16};

  // pthread_t thread1, thread2, thread3, thread4, thread5, thread6, thread7, thread8, thread9, thread10, thread11, thread12, thread13, thread14, thread15, thread16;

  // pthread_create(&thread1, NULL, msort_thread, &data1);
  // pthread_create(&thread2, NULL, msort_thread, &data2);
  // pthread_create(&thread3, NULL, msort_thread, &data3);
  // pthread_create(&thread4, NULL, msort_thread, &data4);
  // pthread_create(&thread5, NULL, msort_thread, &data5);
  // pthread_create(&thread6, NULL, msort_thread, &data6);
  // pthread_create(&thread7, NULL, msort_thread, &data7);
  // pthread_create(&thread8, NULL, msort_thread, &data8);
  // pthread_create(&thread9, NULL, msort_thread, &data9);
  // pthread_create(&thread10, NULL, msort_thread, &data10);
  // pthread_create(&thread11, NULL, msort_thread, &data11);
  // pthread_create(&thread12, NULL, msort_thread, &data12);
  // pthread_create(&thread13, NULL, msort_thread, &data13);
  // pthread_create(&thread14, NULL, msort_thread, &data14);
  // pthread_create(&thread15, NULL, msort_thread, &data15);
  // pthread_create(&thread16, NULL, msort_thread, &data16);

  // pthread_join(thread1, NULL);
  // pthread_join(thread2, NULL);
  // pthread_join(thread3, NULL);
  // pthread_join(thread4, NULL);
  // pthread_join(thread5, NULL);
  // pthread_join(thread6, NULL);
  // pthread_join(thread7, NULL);
  // pthread_join(thread8, NULL);
  // pthread_join(thread9, NULL);
  // pthread_join(thread10, NULL);
  // pthread_join(thread11, NULL);
  // pthread_join(thread12, NULL);
  // pthread_join(thread13, NULL);
  // pthread_join(thread14, NULL);
  // pthread_join(thread15, NULL);
  // pthread_join(thread16, NULL);


  // merge(arr, n / 8, n / 16);
  // merge(arr + n / 8, n / 8, n / 16);
  // merge(arr + 2 * n / 8, n / 8, n / 16);
  // merge(arr + 3 * n / 8, n / 8, n / 16);
  // merge(arr + 4 * n / 8, n / 8, n / 16);
  // merge(arr + 5 * n / 8, n / 8, n / 16);
  // merge(arr + 6 * n / 8, n / 8, n / 16);
  // merge(arr + 7 * n / 8, n / 8, n / 16);

  // merge(arr, n / 4, n / 8);
  // merge(arr + n / 4, n / 4, n / 8);
  // merge(arr + n / 2, n / 4, n / 8);
  // merge(arr + 3 * n / 4, n / 4, n / 8);

  // merge(arr, n / 2, n / 4);
  // merge(arr + n / 2, n / 2, n / 4);

  // merge(arr, n, n / 2);




  // msort(arr, n); // (no threads)

  profile_log(&t);

  // assert that the output is sorted
  for (int i = 0; i < n - 1; i++)
    if (arr[i] > arr[i + 1]) {
      printf("error: arr[%d] = %d > arr[%d] = %d", i, arr[i], i + 1,
             arr[i + 1]);
      return 1;
    }
    return 0;
}
