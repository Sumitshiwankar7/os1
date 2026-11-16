/*
 * JSPM UNIVERSITY, PUNE - Operating System Practical Examination
 * SET 1  |  Q.1 (30 Marks)  |  Group A - System Calls
 * Programme: B.Tech - Computer Science and Engineering
 *
 * Question Statement:
 * Write a C program for Linux to demonstrate Unix system calls as follows: (i)
 * Process management: create a child process using fork(); display the process
 * ID and parent process ID of both processes using getpid() and getppid();
 * make the parent wait using wait(); and replace the child image with the ls
 * -l command using exec(). (ii) File management: create a file using open(),
 * write a few lines into it using write(), read the contents back using read()
 * and close the file using close(). (iii) Input/Output: read a string from the
 * keyboard using read() and display it on the screen using write().
 */
/* SET 1 : Unix system calls - process management, file management, I/O */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);    /* unbuffered: keeps printf and write() output in order */

    /* ---------- (i) PROCESS MANAGEMENT ---------- */
    printf("=== (i) Process Management ===\n");

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    }
    else if (pid == 0) {                 /* CHILD */
        printf("Child  : PID = %d, PPID = %d\n", getpid(), getppid());
        printf("Child  : replacing my image with 'ls -l' using exec()\n");
        execlp("ls", "ls", "-l", (char *)NULL);
        perror("exec failed");           /* reached only if exec fails */
        _exit(1);
    }
    else {                               /* PARENT */
        int status;
        printf("Parent : PID = %d, PPID = %d, Child PID = %d\n",
               getpid(), getppid(), pid);
        printf("Parent : waiting for child using wait()...\n");
        wait(&status);
        printf("Parent : child finished (exit status = %d)\n\n",
               WEXITSTATUS(status));
    }

    /* ---------- (ii) FILE MANAGEMENT ---------- */
    printf("=== (ii) File Management ===\n");
    const char *text = "Line 1: Operating System Practical\n"
                       "Line 2: Unix system calls\n"
                       "Line 3: open, write, read, close\n";
    char buffer[256];

    int fd = open("sample.txt", O_CREAT | O_RDWR | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open failed");
        return 1;
    }
    printf("File 'sample.txt' created (fd = %d)\n", fd);

    ssize_t w = write(fd, text, strlen(text));
    printf("Bytes written : %zd\n", w);

    lseek(fd, 0, SEEK_SET);              /* move offset back to the start */

    ssize_t r = read(fd, buffer, sizeof(buffer) - 1);
    if (r < 0) {
        perror("read failed");
        close(fd);
        return 1;
    }
    buffer[r] = '\0';
    printf("Bytes read    : %zd\nFile contents :\n%s", r, buffer);

    close(fd);
    printf("File closed.\n\n");

    /* ---------- (iii) INPUT / OUTPUT ---------- */
    printf("=== (iii) Input/Output using read() and write() ===\n");
    const char *prompt = "Enter a string: ";
    write(STDOUT_FILENO, prompt, strlen(prompt));

    char input[100];
    ssize_t n = read(STDIN_FILENO, input, sizeof(input) - 1);
    if (n < 0) {
        perror("read failed");
        return 1;
    }
    input[n] = '\0';

    const char *msg = "You entered   : ";
    write(STDOUT_FILENO, msg, strlen(msg));
    write(STDOUT_FILENO, input, n);
    if (n == 0 || input[n - 1] != '\n')
        write(STDOUT_FILENO, "\n", 1);

    return 0;
}
