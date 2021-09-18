-fpie -fpic -fPIC: 编译选贤

-pie: 链接选项

# https://stackoverflow.com/questions/3544035/what-is-the-difference-between-fpic-and-fpic-gcc-parameters
-fpic 跟 -fPIC 都会生成position independented code, 

# https://stackoverflow.com/questions/2463150/what-is-the-fpie-option-for-position-independent-executables-in-gcc-and-ld
-fpie, -fPIE

PIE 用于支持ASLR(address space layout randomization), 在PIE之前, 只有PIC的动态库能够被加载在内存的任意一个地址;
PIE 跟PIC非常类似,但不同于PIC的是,PLT(produre linkage table)不会被创建,而是通过PC-relative resolution来进行重定向;
PIE跟-static是不兼容的;
gcc/linker都使用了PIE之后, 编译以及链接代码都是位置无关的了. 所有对全局变量的引用都通过GOT来处理;

```bash
bash main.sh
# no-pie 两次执行main的地址是不变的
2
Breakpoint 1 at 0x400506: file main.c, line 4.

Breakpoint 1, main () at main.c:4
4	    puts("hello");
pc = 0x400506

Breakpoint 1, main () at main.c:4
4	    puts("hello");
pc = 0x400506


# pie 两次执行main的地址是变化的
Breakpoint 1 at 0x659: file main.c, line 4.

Breakpoint 1, main () at main.c:4
4	    puts("hello");
pc = 0x557b977d0659

Breakpoint 1, main () at main.c:4
4	    puts("hello");
pc = 0x55fba2304659
```


