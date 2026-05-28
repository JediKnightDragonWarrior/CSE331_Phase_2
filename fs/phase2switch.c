#include <linux/kernel.h>
#include <linux/linkage.h>

int phase2switchflag = 1;

asmlinkage long sys_set_fair_share(int flag)
{
	phase2switchflag = flag;
	printk("Fair Share Scheduler mode set to: %d\n", flag);
	return 0;
}
