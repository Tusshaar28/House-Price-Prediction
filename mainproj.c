#include<stdio.h>
#include<signal.h>
#include<unistd.h>
#include<stdlib.h>
#include<time.h>
#include<setjmp.h>


typedef struct threads
{
	jmp_buf context;
	char stack[4096];
	int running;
	int suspended;
	int ready;
	int dead;
	int sleeptime;
	clock_t starttime;
	
} Thread;

Thread main_thread;

Thread my_threads[3];


void func(Thread *t) {
    t->running = 1;
    printf("Thread %p is running currently\n", (void *)t);

    while (((clock() - t->starttime) / CLOCKS_PER_SEC) < t->sleeptime);

    t->running = 0;
    t->dead = 1;
    printf("Thread %p has completed\n", (void *)t);

    if (setjmp(t->context) == 0) {
      
        longjmp(main_thread.context, 1);
    }
}

void threadsleep(Thread* t,int sec) {
    t->sleeptime = sec;
    if (setjmp(t->context) == 0) {
        t->suspended = 1;
        longjmp(main_thread.context, 1);
    }
}

void create(Thread* t, unsigned int stime) {
    t->running = 0;
    t->suspended = 0;
    t->ready = 0;
    t->dead = 0;
    t->sleeptime = stime;

    if (setjmp(t->context) == 0) {
        unsigned char *stackp = &t->stack[4095];
        func(t);

        longjmp(main_thread.context, 1);
    }

    t->ready = 1;
}


void delthread(Thread* t)
 {
    if (t->running) 
	{
        t->running = 0;
        t->suspended = 0;
        printf("Thread %p has been deleted\n", (void*)t);
    } 
	else
	 {
        printf("Thread %p is not running\n", (void*)t);
    }
}

void suspend(Thread* t)
 {
    if (t->running && !t->suspended)
	 {
        t->suspended = 1;
        printf("Thread %p has been suspended\n", (void*)t);
        longjmp(main_thread.context, 1);
    }
	else if (!t->running) 
	{
        printf("Thread %p is not running currently\n", (void*)t);
    } 
	else
	 {
        printf("Thread %p was already suspended\n", (void*)t);
    }
}


void resume(Thread* t) {
    if (t->running && t->suspended) 
	{
        t->suspended = 0;
        printf("Thread %p has been resumed\n", (void*)t);
        longjmp(main_thread.context, 1);
    }
	 else if (!t->running)
	{
        printf("Thread %p is not running\n", (void*)t);
    }
	 else 
	 {
        printf("Thread %p is not suspended\n", (void*)t);
    }
}


void status(Thread* t)
 {
	printf("1 = Yes, 0= No\n");
    printf("Thread %p - Status: %d, Suspended: %d, Ready: %d, Terminated: %d\n",(void*)t,t->running,t->suspended,t->ready,t->dead);
}

int main() {
    
    create(&my_threads[0],5);
    create(&my_threads[1],3);
    create(&my_threads[2],2);

    
    while (!my_threads[0].ready || !my_threads[1].ready || !my_threads[2].ready) {
        usleep(10000);
    }

   
    if (setjmp(main_thread.context) == 0) 
	{
        while (my_threads[0].running || my_threads[1].running || my_threads[2].running)
		 {
            status(&my_threads[0]);
            status(&my_threads[1]);
            status(&my_threads[2]);
            threadsleep(&my_threads[0], 1);
            threadsleep(&my_threads[1], 1); 
            threadsleep(&my_threads[2], 1); 
        }
    }

   
    delthread(&my_threads[0]);
    delthread(&my_threads[1]);
    delthread(&my_threads[2]);

    return 0;
}





