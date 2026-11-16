/*
 * JSPM UNIVERSITY, PUNE - Operating System Practical Examination
 * SET 4  |  Q.1 (30 Marks)  |  Group B - Synchronization Using Semaphores
 * Programme: B.Tech - Computer Science and Engineering
 *
 * Question Statement:
 * Solve the Producer-Consumer problem with a bounded buffer of size 5 (C with
 * POSIX threads and semaphores, or Java Semaphore class). Use counting
 * semaphores empty and full and a binary semaphore mutex. Create two producer
 * threads and two consumer threads, each producing/consuming 5 items, and
 * display messages showing the buffer operations. Explain how the semaphores
 * avoid race conditions, buffer overflow and buffer underflow.
 */
/* SET 4 : Producer-Consumer (bounded buffer, size 5) using POSIX threads + semaphores
   Compile : gcc set4_producer_consumer.c -o pc -pthread
   Run     : ./pc                                                              */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define BUFFER_SIZE     5
#define NUM_PRODUCERS   2
#define NUM_CONSUMERS   2
#define ITEMS_PER_THREAD 5

int buffer[BUFFER_SIZE];
int in = 0, out = 0, count = 0;      /* count is only for display */

sem_t empty;                         /* counts EMPTY slots  (init = 5) */
sem_t full;                          /* counts FILLED slots (init = 0) */
sem_t mutex;                         /* binary semaphore for mutual exclusion (init = 1) */

void *producer(void *arg)
{
    int id = *(int *)arg;
    for (int i = 1; i <= ITEMS_PER_THREAD; i++) {
        int item = id * 100 + i;              /* e.g. P1 -> 101..105 */
        usleep(rand() % 200000);              /* simulate production time */

        sem_wait(&empty);                     /* wait for a free slot  (prevents overflow)  */
        sem_wait(&mutex);                     /* enter critical section (prevents race)     */

        buffer[in] = item;
        printf("Producer %d produced item %d -> buffer[%d]  (items in buffer = %d)\n",
               id, item, in, ++count);
        in = (in + 1) % BUFFER_SIZE;

        sem_post(&mutex);                     /* leave critical section */
        sem_post(&full);                      /* one more filled slot   */
    }
    return NULL;
}

void *consumer(void *arg)
{
    int id = *(int *)arg;
    for (int i = 1; i <= ITEMS_PER_THREAD; i++) {
        sem_wait(&full);                      /* wait for an item (prevents underflow) */
        sem_wait(&mutex);

        int item = buffer[out];
        printf("    Consumer %d consumed item %d <- buffer[%d]  (items in buffer = %d)\n",
               id, item, out, --count);
        out = (out + 1) % BUFFER_SIZE;

        sem_post(&mutex);
        sem_post(&empty);                     /* one more empty slot */

        usleep(rand() % 300000);              /* simulate consumption time */
    }
    return NULL;
}

int main(void)
{
    pthread_t prod[NUM_PRODUCERS], cons[NUM_CONSUMERS];
    int pid[NUM_PRODUCERS], cid[NUM_CONSUMERS];

    sem_init(&empty, 0, BUFFER_SIZE);
    sem_init(&full, 0, 0);
    sem_init(&mutex, 0, 1);

    printf("Producer-Consumer: buffer size = %d, %d producers, %d consumers, %d items each\n\n",
           BUFFER_SIZE, NUM_PRODUCERS, NUM_CONSUMERS, ITEMS_PER_THREAD);

    for (int i = 0; i < NUM_PRODUCERS; i++) {
        pid[i] = i + 1;
        pthread_create(&prod[i], NULL, producer, &pid[i]);
    }
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        cid[i] = i + 1;
        pthread_create(&cons[i], NULL, consumer, &cid[i]);
    }

    for (int i = 0; i < NUM_PRODUCERS; i++) pthread_join(prod[i], NULL);
    for (int i = 0; i < NUM_CONSUMERS; i++) pthread_join(cons[i], NULL);

    printf("\nAll threads finished. Items left in buffer = %d\n", count);

    sem_destroy(&empty);
    sem_destroy(&full);
    sem_destroy(&mutex);
    return 0;
}
