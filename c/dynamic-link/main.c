#include <stdio.h>
#include "inc/lib.h"

int main() {
	printf("main(%p), hello(%p), world(%p)\n", main, &hello, world);
	printf("hello-main=%d, world-main=%d, world-hello=%d\n", (void*)&hello-(void*)main, (void*)world-(void*)main,
			(void*)world-(void*)&hello);
}
