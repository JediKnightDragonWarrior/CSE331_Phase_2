#include <linux/kernel.h>
#include <linux/sched.h>
#include <asm/uaccess.h>
#include <asm/system.h>
#include <linux/getProcessInfoS26.h>

asmlinkage int sys_getProcessInfoS26(struct processInfoS26 *data) {
    struct processInfoS26 arg;
    struct task_struct *crr = current;
    long failed_bytes;
    int return_code = -1;

    cli();

    failed_bytes = copy_from_user(&arg, data, sizeof(struct processInfoS26));

    if (failed_bytes || !crr) {
        return return_code;
    }

    if (arg.flag > 0) {
        if (arg.flag <= 26) {
            arg.pid = crr->pid;
            arg.pid_parent = crr->p_pptr->pid;
            arg.p_counter = crr->counter;
            arg.nice = crr->nice;
            arg.uid = crr->uid;
            arg.priority = crr->rt_priority;
            arg.weight = crr->counter + 20 - crr->nice;
        } 
        else if (arg.flag > 26) {
            arg.weight = crr->counter + 20 - crr->nice;
        }
        
        failed_bytes = copy_to_user(data, &arg, sizeof(struct processInfoS26));
        
        if (!failed_bytes) {
            return_code = 0;
        }
    }

    sti();
    
    return return_code;
}