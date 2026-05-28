#include <stdio.h>
#include <linux/unistd.h>
#include <errno.h>

_syscall1(long, set_fair_share, int, flag)

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <1 for default, 2 for fair share>\n", argv[0]);
        return 1;
    }

    int flag = atoi(argv[1]);
    
    long res = set_fair_share(flag);
    if (res < 0) {
        perror("System call failed");
        return 1;
    }
    
    printf("Scheduler switched to mode %d successfully.\n", flag);
    return 0;
}
