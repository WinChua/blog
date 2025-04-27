#include <stdio.h>
#include <unistd.h>

int abc __attribute__((section(".my_section"))) = 3;
int main(int argc, char * argv[]) {
  pid_t pid = getpid();
  printf("addr of abc: %p\npid: %d\n", &abc, pid);
  sleep(1000000);
  return 0;
}
