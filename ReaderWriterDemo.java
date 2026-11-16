/*
 * JSPM UNIVERSITY, PUNE - Operating System Practical Examination
 * SET 5  |  Q.1 (30 Marks)  |  Group B - Reader-Writer Synchronization Using Java Locks
 * Programme: B.Tech - Computer Science and Engineering
 *
 * Question Statement:
 * Implement the Reader-Writer synchronization problem in Java using
 * ReentrantReadWriteLock. Create a shared resource (a counter or a data
 * string), three reader threads and two writer threads. Readers may read
 * concurrently, whereas a writer must have exclusive access. Display messages
 * showing when each thread acquires and releases the read or write lock, and
 * explain how the locks ensure data consistency.
 */
/* SET 5 : Reader-Writer synchronization using ReentrantReadWriteLock
   Compile : javac ReaderWriterDemo.java
   Run     : java ReaderWriterDemo                                          */
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class ReaderWriterDemo {

    private static int sharedCounter = 0;                        // shared resource
    private static final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
    private static final int ROUNDS = 2;                         // operations per thread

    static void log(String msg) {
        System.out.printf("[%5d ms] %s%n", System.currentTimeMillis() - START, msg);
    }
    private static final long START = System.currentTimeMillis();

    static class Reader extends Thread {
        private final int id;
        Reader(int id) { super("Reader-" + id); this.id = id; }

        @Override public void run() {
            try {
                for (int i = 0; i < ROUNDS; i++) {
                    Thread.sleep((long) (Math.random() * 300));
                    log("Reader " + id + " waiting for READ lock");
                    rwLock.readLock().lock();
                    try {
                        log("Reader " + id + " ACQUIRED read lock  (active readers = "
                                + rwLock.getReadLockCount() + ")");
                        log("Reader " + id + " reads counter = " + sharedCounter);
                        Thread.sleep(400);                       // reading takes time
                    } finally {
                        log("Reader " + id + " RELEASING read lock");
                        rwLock.readLock().unlock();
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    static class Writer extends Thread {
        private final int id;
        Writer(int id) { super("Writer-" + id); this.id = id; }

        @Override public void run() {
            try {
                for (int i = 0; i < ROUNDS; i++) {
                    Thread.sleep((long) (Math.random() * 300));
                    log("Writer " + id + " waiting for WRITE lock");
                    rwLock.writeLock().lock();
                    try {
                        log("Writer " + id + " ACQUIRED write lock (exclusive access)");
                        int old = sharedCounter;
                        Thread.sleep(300);                       // writing takes time
                        sharedCounter = old + 10;
                        log("Writer " + id + " updated counter " + old + " -> " + sharedCounter);
                    } finally {
                        log("Writer " + id + " RELEASING write lock");
                        rwLock.writeLock().unlock();
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread[] threads = {
            new Reader(1), new Reader(2), new Reader(3),
            new Writer(1), new Writer(2)
        };
        for (Thread t : threads) t.start();
        for (Thread t : threads) t.join();
        System.out.println("\nFinal value of shared counter = " + sharedCounter
                + "  (expected 2 writers x " + ROUNDS + " updates x 10 = " + (2 * ROUNDS * 10) + ")");
    }
}
