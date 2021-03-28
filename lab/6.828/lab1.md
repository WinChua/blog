# AT&T asm
* 操作数顺序: src在左,dst在右
* 立即数: 加上 $ 前缀
* 寻址: immed32(base, indexpointer, indexscale) => base + indexpointer * indexscale + immed32
* 寄存器: %eax
* 寄存器寻址: (%eax)

# PC 物理内存分布(32 bit, 4GB为例子)
1. 第一代pc机器只有1MB的物理内存, 为了兼容初代PC, 把内存前1MB保留:
```
    ......................
    ......................
    ......................
    +--------------------+ 0x00100000 (1MB)
    |                    |                 0x00000010 => 8B
    |      BIOS ROM      | 0x000ffff0
    |                    | 
    +--------------------+ 0x000F0000 (960KB)
    |   16bits devices   |
    |   expansion ROMs   |
    +--------------------+ 0x000C0000 (768KB)
    |    VGA Display     | 
    +--------------------+ 0x000A0000 (640KB)
    |                    | 
    +--------------------+ 0x00000000 (0KB)
```

# PC 32bit boot
1. PC 在 0x000ffff0 的物理地址处开始执行. 为什么要在0x000ffff0执行第一条指令呢?这事80x86的设计,由于bios通过硬件映射到0x000f0000 ~ 0x000fffff, 把0x000ffff0作为第一条执行的指令能够保证PC在启动或者重启的时候永远执行BIOS
2. BIOS负责将一些PCI, VGA初始化, 然后寻找第一个能够启动的磁盘(bootable)
3. 磁盘的最小传输单位是sector, 大小事512byte, 可启动磁盘的第一个sector称为boot sector, 这个sector中会存储如何将kern转载进内存的代码;
4. 当BIOS找到了第一个bootable的sector的时候, 会将boot sector加载到0x7c00 ~ 0x7dff, 然后jmp到0x7c00的位置,开始加载kernel; (为什么是0x7c00呢? 其实任意一个地址都可以,只是一个约定)
5. boot sector中存储的代码一般称为boot loader, 主要负责两件事情:
5.1 将cpu从real mode切换到protected mode
5.2 从磁盘中加载kernel


# boot loader 如何从磁盘中加载kernel?
1. kernel的代码放在bootable disk的第一个sector之后的位置,是一个elf格式的文件
2. 首先从第一个sector开始读区第一个page(4KB),到0x10000, 位置上面, 把0x10000看成struct ELF *
2.1 可以读出kernel具有多少个segment(program header),以及header数组的偏移位置, 数组的每一项存储的是一个struct Proghdr * 指针
2.2 每一个Proghdr有三个主要字段:
* 当前prog的大小;
* 应该加载到内存的目标地址(load address);
* 在文件中的偏移字节数, 注意elf文件中记录的是当前proghdr在文件中的偏移字节数量, 但是在readseg的时候, 需要除以sectsize, 换算成在第几个sector中
2.3 当所有的proghdr加载完成之后,调用 0x10000->e_entry();

# kernel
* 在开始执行kernel的代码的时候, mmu还没有设置起来, 我们需要使用物理地址,可以看下kernel文件中跟proghdr相关的信息:

    [root@VM_55_102_centos ~/6.828/lab/obj/kern]# readelf -l kernel

    Elf file type is EXEC (Executable file)
    Entry point 0x10000c
    There are 3 program headers, starting at offset 52
    
    Program Headers:
      Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
      LOAD           0x001000 0xf0100000 0x00100000 0x075e9 0x075e9 R E 0x1000
      LOAD           0x009000 0xf0108000 0x00108000 0x0a948 0x0a948 RW  0x1000
      GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RWE 0x10
    
     Section to Segment mapping:
      Segment Sections...
       00     .text .rodata .stab .stabstr
       01     .data .bss
       02
可以看到kernel文件 中VirtAddr与PhysAddr不是一一对应的.
为了把低地址空间留给应用程序, kernel的地址通常会映射在一个比较高的位置, 而且这些位置通常不存在对应的物理内存, 于是需要在BOIS之上(1MB)到地方存储kernel的代码
然后通过MMU将高地址映射到(1MB)的地方,也要求了机器内存需要大于1MB

* 在起初, 需要使用静态指定的页表映射, JOS中静态指定了, 0x00000000 ~ 0x00400000 映射到了0x00000000 ~ 0x00400000 以及 0xf0000000 ~ 0xf0400000
由于当前中断处理还没有设置, 当进程使用了这个范围之外的内存时,将会导致JOS coredump
