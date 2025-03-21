#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#include "cputime.h"

struct thread_data {
    int *arr;
    int start;
    int end;
    long long sum;
};

void *sum_array(void *arg) {
    struct thread_data *data = (struct thread_data *)arg;
    data->sum = 0;
    for (int i = data->start; i < data->end; i++) {
        data->sum += data->arr[i];
    }
    return NULL;
}

int main() {
    int n = 1 << 28;
    printf("Summing %d random integers\n", n);
    int *arr = malloc(n * sizeof(int));
    if (arr == NULL) {
        perror("Failed to allocate memory");
        return EXIT_FAILURE;
    }

    // Populate array with N random integers
    srand(1234);
    for (int i = 0; i < n; i++) {
        arr[i] = rand();
    }

    struct profile_times t;
    profile_start(&t);

    // // without threads:
    // struct thread_data data = {arr, 0, n, 0};
    // sum_array(&data);
    // printf("Total sum: %lld\n", data.sum);

    // With threads
    struct thread_data data1 = {arr, 0, n / 2, 0};
    struct thread_data data2 = {arr, n / 2, n, 0};

    // Create threads
    pthread_t thread1, thread2;
    pthread_create(&thread1, NULL, sum_array, &data1);
    pthread_create(&thread2, NULL, sum_array, &data2);

    // Wait for threads to finish
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    // Combine results
    long long total_sum = data1.sum + data2.sum;
    printf("Total sum (thread): %lld\n", total_sum);

    profile_log(&t);

    // Clean up
    free(arr);
    return 0;
}