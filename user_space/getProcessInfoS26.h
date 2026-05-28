#ifndef _USER_GETPROCESSINFOS26_H
#define _USER_GETPROCESSINFOS26_H

#include <linux/unistd.h>
#include <sys/types.h>

struct processInfoS26 {
    int flag;
    pid_t pid;
    pid_t pid_parent;
    long p_counter;
    long nice;
    long uid;
    int priority;
    long weight;
};

_syscall1(int, getProcessInfoS26, struct processInfoS26 *, data);

#endif
