#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <errno.h>

/*
Usage:
  ./os_ipc --exec        # parent forks; child execs /bin/ls; parent waits
  ./os_ipc --pipe        # parent->child pipe: "Hello from parent"
*/

void demo_exec() {
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork failed");
        exit(1);
    }
    if (pid == 0) {
        // Child: exec `ls -l`
        char *argv[] = {"/bin/ls", "-l", NULL};
        execv("/bin/ls", argv);
        perror("execv failed");
        exit(1);
    } else {
        // Parent: wait for child
        int status = 0;
        waitpid(pid, &status, 0);
        printf("Parent: child exited with status %d\n", status);
    }
}

void demo_pipe() {
    int fds[2];
    if (pipe(fds) == -1) {
        perror("pipe");
        exit(1);
    }
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        exit(1);
    }
    if (pid == 0) {
        // Child: read
        close(fds[1]);
        char buf[1024] = {0};
        ssize_t n = read(fds[0], buf, sizeof(buf)-1);
        if (n >= 0) {
            buf[n] = '\0';
            printf("Child received: %s\n", buf);
        } else {
            perror("read");
        }
        close(fds[0]);
        exit(0);
    } else {
        // Parent: write
        close(fds[0]);
        const char *msg = "Hello from parent";
        if (write(fds[1], msg, strlen(msg)) == -1) {
            perror("write");
        }
        close(fds[1]);
        waitpid(pid, NULL, 0);
    }
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s [--exec|--pipe]\n", argv[0]);
        return 1;
    }
    if (strcmp(argv[1], "--exec") == 0) {
        demo_exec();
    } else if (strcmp(argv[1], "--pipe") == 0) {
        demo_pipe();
    } else {
        fprintf(stderr, "Unknown option: %s\n", argv[1]);
        return 1;
    }
    return 0;
}
