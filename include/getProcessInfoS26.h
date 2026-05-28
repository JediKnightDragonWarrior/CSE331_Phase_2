#ifndef __LINUX_GETPROCESSINFOS26_H
#define __LINUX_GETPROCESSINFOS26_H

#include <linux/types.h>

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

#endif
