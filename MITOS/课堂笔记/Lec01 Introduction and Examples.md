# Lecture 01 Introduction and Examples(Robert)

## 1.1 课程内容简介

> **课程目标**

- O/S DESIGN
- HANDS-ON EXP

> **O/S PURPOSE**

- ABSTRACT H/W:抽象硬件
- MULTIPLEX:复用硬件
- ISOLATION:多个程序件互不干扰
- SHARING
- SECURITY/PERMISSION SYSTEM/ACCESS CONTROL
- GOOD PERFORMANCE
- RANGE OF USER

## 1.2 操作系统结构

> **O/S ORAGNIZATION**

- USERSPACE:用户空间，运行各种各样的应用程序，如文本编辑器vi，C编译器(cc)
- KERNAL: 计算机资源守护者，主要关注点在Kernel、连接Kernal和用户空间程序的接口、Kernel内软件的架构。
  - 当启动计算机时，Kernel总是第一个被启动。Kernel程序只有一个，它维护数据来管理每一个用户空间进程。Kernel同时还维护了大量的数据结构来帮助它管理各种各样的硬件资源，以供用户空间的程序使用。Kernel同时还有大量内置的服务。
  - FS:文件系统通常有一些逻辑分区。目前而言，我们可以认为文件系统的作用是管理文件内容并找出文件具体在磁盘中的哪个位置。文件系统还维护了一个独立的命名空间，其中每个文件都有文件名，并且命名空间中有一个层级的目录，每个目录包含了一些文件。所有这些都被文件系统所管理。
  - PROCESS:进程管理系统。每一个用户空间程序都被称为一个进程，它们有自己的内存和共享的CPU时间。
  - MEM,ALLCO:管理内存的分配。不同的进程需要不同数量的内存，Kernel会复用内存、划分内存，并为所有的进程分配内存。
  - ACCESS CTL:当一个进程想要使用某些资源时，比如读取磁盘中的数据，使用某些内存，Kernel中的Access Control机制会决定是否允许这样的操作。
- 硬件底层资源:CPU、RAM、DISK、NET

![](https://906337931-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MH_0vtckm44OL-Ry80u%2F-MHfa6qidpjQGh_XpuRm%2Fimage.png?alt=media&token=13f0cc46-16b5-4e7e-bfc6-498ff3c6449a)

> **API-KERNAL**

Kernel的API，它决定了应用程序如何访问Kernel。

- system call: 通过所谓的系统调用（System Call）来完成。系统调用与程序中的函数调用看起来是一样的，但区别是系统调用会实际运行到系统内核中，并执行内核中对于系统调用的实现。

- 🙋🌰: `fd = open("out",1)`
  - `open`是一个系统调用，open会跳转到Kernel，Kernel可以获取到open参数，执行一些实现open的kernel代码，最后返回一个文件描述符对象
  - `fd`全称为`file descriptor`,应用程序可以使用这个文件描述符作为handle，来表示相应打开的文件。
- 🙋🌰 `write(fd,"hello\n",6)`:向文件写入数据
  - 向write传递一个由open返回的文件描述符作为参数。
  - 向write传递一个指向要写入数据的指针（数据通常是char型序列）,实际上是内存中的地址。所以这里实际上告诉内核，将内存中这个地址起始的6个字节数据写入到fd对应的文件中。
  - 想要写入字符的数量
- 🙋🌰 `pid = fork();`
  - 创建了一个与调用进程一模一样的新的进程，并返回新进程的process ID/pid

> **Q:系统调用和程序里的函数的区别？**

Robert教授：Kernel的代码总是有特殊的权限。当机器启动Kernel时，Kernel会有特殊的权限能直接访问各种各样的硬件，例如磁盘。而普通的用户程序是没有办法直接访问这些硬件的。所以，当你执行一个普通的函数调用时，你所调用的函数并没有对于硬件的特殊权限。然而，如果你触发系统调用到内核中，内核中的具体实现会具有这些特殊的权限，这样就能修改敏感的和被保护的硬件资源，比如访问硬件磁盘。我们之后会介绍更多有关的细节。

## 1.3 WHY HARD/INTERESTING?
  
- UNFORGNING:内核编程环境较为复杂困难
- TENSIONS
  - EFFICIENT vs ABSTRACT
  - POWERFUL vs SIMPLE
  - FLEXIBLE vs SECURITY
- INTERACTION:系统提供服务间的交互
  - `fd = open()`与 `pid = fork()`

> **课程环境**

- OS-XV6 类unix操作系统
- RISC-V 微处理器，RISC-V指令集
- QEMU硬件仿真，模拟RISC-V

```zsh
make clean
make qemu
```

## 1.4 系统调用

XV6书籍的第二章有一个表格，列举了所有的系统调用的参数和返回值。

```zsh
cd xv6-riscv

// 清除编译
make clean

// 编译
make qemu
```

### 1.4.1 read, write, exit系统调用

```c
// copy.c:copy input to output

# include "kernel/types.h"
# include "user/user.h"

int 
main()
{
    char buf[64];
    
    while(1){
        int n = read(0,buf,sizeof(buf));
        if(n <= 0){
            break;
        }
        write(1,buf,n);
    }
    exit(0);
}
```

这个程序里面执行了3个系统调用，分别是read，write和exit。

> **read**

read系统调用接收3个参数:

- 第一个参数是**文件描述符**，指向一个之前打开的文件。
  - 默认情况下，文件描述符0连接到console的输入，文件描述符1连接到了console的输出。
  - 这里的0，1文件描述符是非常普遍的Unix风格，许多的Unix系统都会从文件描述符0读取数据，然后向文件描述符1写入数据。
- 第二个参数是**指向某段内存的指针**，程序可以通过指针对应的地址读取内存中的数据，这里的指针就是代码中的buf参数。
  - 在代码第10行，程序在栈里面申请了64字节的内存，并将指针保存在buf中，这样read可以将数据保存在这64字节中。
- 第三个参数是代码**读取的最大长度**，sizeof(buf)表示，最多读取64字节的数据。read最多只能从连接到文件描述符0的设备，也就是console中，读取64字节的数据。

read的返回值:可能是读到的字节数

- read可能从一个文件读数据，如果到达了文件的结尾没有更多的内容了
- read会返回0。如果出现了一些错误，比如文件描述符不存在，read或许会返回-1
- 系统调用通常是通过返回-1来表示错误，代码编写过程中应该检查所有系统调用的返回值以确保没有错误

⚠️**注意：** copy程序，或者说read，write系统调用，它们并不关心读写的数据格式，它们就是单纯的读写，而copy程序会按照8bit的字节流处理数据，如何解析它们，完全是用应用程序决定的。所以应用程序可能会解析这里的数据为C语言程序，但是操作系统只会认为这里的数据是按照8bit的字节流。

> **Q:如果read的第三个参数设置成1 + sizeof(buf)会怎样？**

Robert教授：如果第三个参数是65字节，操作系统会拷贝65个字节到你提供的内存中（第二个参数）。但是如果栈中的第65个字节有一些其他数据，那么这些数据会被覆盖，这里是个bug，或许会导致你的代码崩溃，或者一些异常的行为。所以，作为一个程序员，你必须要小心。C语言很容易写出一些编译器能通过的，但是最后运行时出错的代码。虽然很糟糕，但是现实就是这样。

### 1.4.2 open系统调用

最直接的创建文件描述符的方法是open系统调用。

> **open.c**

open的程序，会创建一个叫做output.txt的新文件，并向它写入一些数据，最后退出。我们看不到任何输出，因为它只是向打开的文件中写入数据。

```c
// open.c: create a file,write to it

# include "kernel/types.h"
# include "user/user.h"
# include "kernel/fcntl.h"

int main(){
    int fd = open("output.txt",O_WRONLY | O_CREATE);
    write(fd,"ooo\n",4);
    exit(0);
}
```

```zsh
$ cat output.txt
ooo
```

> **open系统调用**

open系统调用参数:

- 第一个参数:文件名output.txt
- 第二个参数是一些标志位，用来告诉open系统调用在内核中的实现：我们将要创建并写入一个文件

open系统调用返回值

- 返回一个新分配的文件描述符，这里的文件描述符是一个小的数字，可能是2，3，4或者其他的数字。

> **write系统调用**

文件描述符作为第一个参数被传到了write，write的第二个参数是数据的指针，第三个参数是要写入的字节数。数据被写入到了文件描述符对应的文件中。

> **文件描述符**

文件描述符本质上对应了内核中的一个表单数据。内核维护了每个运行进程的状态，内核会为每一个运行进程保存一个表单，表单的key是文件描述符。这个表单让内核知道，每个文件描述符对应的实际内容是什么。

这里比较关键的点是，**每个进程都有自己独立的文件描述符空间**，所以如果运行了两个不同的程序，对应两个不同的进程，如果它们都打开一个文件，它们或许可以得到相同数字的文件描述符，但是因为内核为每个进程都维护了一个独立的文件描述符空间，**这里相同数字的文件描述符可能会对应到不同的文件。**

### 1.4.3 shell

> **概述**

Shell:命令行接口，Shell是一种对于Unix系统管理来说非常有用的接口，它提供了很多工具来管理文件，编写程序，编写脚本。

Shell最常见的功能是：当你输入内容时，是在告诉Shell运行相应的程序。

🙋🌰：当我们输入ls时，实际的意义是要求**Shell运行名为ls的程序**，文件系统中会有一个文件名为ls，这个文件中包含了一些计算机指令，所以实际上，当输入ls时，是在要求Shell运行位于文件ls内的这些计算机指令。

> **Shell 重定向IO**

```zsh
$ ls > out
$ cat out
.              1 1 1024
..             1 1 1024
README         2 2 2226
cat            2 3 24232
copy           2 4 22632
echo           2 5 23048
forktest       2 6 13272
grep           2 7 27528
init           2 8 23792
kill           2 9 22992
ln             2 10 22848
ls             2 11 26424
mkdir          2 12 23152
open           2 13 22480
rm             2 14 23128
sh             2 15 41952
stressfs       2 16 23984
usertests      2 17 157032
grind          2 18 38160
wc             2 19 25312
zombie         2 20 22384
console        3 21 0
output.txt     2 22 4
out            2 23 578
```

**上述指令的实际意义是:** 要求Shell运行ls命令，但是**将输出重定向到一个叫做out的文件中**。这里执行完成之后我们看不到任何的输出，因为输出都送到了out文件。现在我们知道out文件包含了一些数据，我们可以通过cat指令读取一个文件，并显示文件的内容。

> **grep指令**

grep x会搜索输入中包含x的行，我可以告诉shell将输入重定向到文件out，这样我们就可以查看out中的x。

```zsh
$ grep x

$ grep x < out
output.txt     2 22 4

$ grep l < out
kill           2 9 22992
ln             2 10 22848
ls             2 11 2642
```

因为out文件包含了ls的输出，所以我们可以看出有3个文件的文件名包含了l。

> **Q：有一个系统调用和编译器的问题。编译器如何处理系统调用？生成的汇编语言是不是会调用一些由操作系统定义的代码段？**

Robert教授：有一个特殊的RISC-V指令，程序可以调用这个指令，并将控制权交给内核。所以，实际上当你运行C语言并执行例如open或者write的系统调用时，从技术上来说，open是一个C函数，但是这个函数内的指令实际上是机器指令，也就是说我们调用的open函数并不是一个C语言函数，它是由汇编语言实现，组成这个系统调用的汇编语言实际上在RISC-V中被称为ecall。这个特殊的指令将控制权转给内核。之后内核检查进程的内存和寄存器，并确定相应的参数。

### 1.4.4 fork

fork会创建一个新的进程，下面是使用fork的一个简单用例。

> **fork**

```c
// fork.c: create a new process

# include "kernel/types.h"
# include "user/user.h"

int main(){
    int pid;

    pid = fork();

    printf("fork() return %d \n",pid);

    if(pid == 0){
        printf("child\n");
    }else{
        printf("parent\n");
    }
    exit(0);
}
```

- fork会**拷贝当前进程的内存**，并创建一个新的进程，这里的内存包含了进程的指令和数据。之后，我们就有了两个拥有完全一样内存的进程。
- **fork系统调用在两个进程中都会返回**
  - 在原始的进程中，fork系统调用会返回大于0的整数，这个是新创建进程的ID。
  - 在新创建的进程中，fork系统调用会返回0。
- 通过校验pid，如果pid等于0，那么这必然是子进程。调用进程通常称为父进程，父进程看到的pid必然大于0。所以父进程会打印“parent”，子进程会打印“child”。之后两个进程都会退出。

运行fork 之后如下为输出

```zsh
$ fork
ffoorrkk(() )r erteutrnur n4  
0pa re
nt
child
```

上述输出像是乱码，实际状况是：fork系统调用之后，**两个进程都在同时运行**，QEMU实际上是在模拟多核处理器，所以这两个进程实际上就是同时在运行。

当这两个进程在输出的时候，它们会同时一个字节一个字节的输出，两个进程的输出交织在一起，所以你可以看到两个f，两个o等等。

**fork创建了一个新的进程。** 当我们在Shell中运行东西的时候，**Shell实际上会创建一个新的进程来运行我们输入的每一个指令**。

所以，当我输入ls时，我们需要Shell通过fork创建一个进程来运行ls，这里需要某种方式来让这个新的进程来运行ls程序中的指令，加载名为ls的文件中的指令（也就是后面的exec系统调用)。

> **Q:fork产生的子进程是不是总是与父进程是一样的？它们有可能不一样吗？**

Robert教授：**在XV6中**，除了fork的返回值，两个进程是一样的。两个进程的指令是一样的，数据是一样的，栈是一样的，同时，两个进程又有各自独立的地址空间，它们都认为自己的内存从0开始增长，但是在XV6中，父子进程除了fork的返回值，其他都是一样的。文件描述符的表单也从父进程拷贝到子进程。所以如果父进程打开了一个文件，子进程可以看到同一个文件描述符，尽管子进程看到的是一个文件描述符的表单的拷贝。除了拷贝内存以外，fork还会拷贝文件描述符表单这一点还挺重要的，我们接下来会看到。

在一个更加复杂的操作系统，有一些细节我们现在并不关心，这些细节偶尔会导致父子进程不一致。

### 1.4.5 exec、wait系统调用

#### 1.4.5.1 exec系统调用

> **exec代码**
echo是一个非常简单的命令，它接收任何你传递给它的输入，并将输入写到输出。

```c
// exec.c: replace a process with a executable file

# include "kernel/types.h"
# include "user/user.h"

int main(){
    char *argv[] = {"echo","this","is","echo",0};

    exec("echo",argv);

    printf("exec failed!\n");

    exit(0);
}
```

**上述代码会执行exec系统调用**，这个系统调用**会从指定的文件中读取并加载指令**，**并替代当前调用进程的指令**。从某种程度上来说，这样*相当于丢弃了调用进程的内存，并开始执行新加载的指令*

`exec("echo",argv);`:该行会有如下效果

- 操作系统从名为`echo`的文件中**加载指令到当前的进程中**，并替换了当前进程的内存
- **之后开始执行这些新加载的指令**。
- **传入命令行参数**:exec允许你传入一个命令行参数的数组，这里就是一个C语言中的指针数组，在上面代码的第10行设置好了一个字符指针的数组，这里的字符指针本质就是一个字符串（string）。

综上所述此处等价于运行`echo`命令，并携带"this is echo"这三个参数。所以当我们运行exec文件时:

```zsh
$ exec
this is echo
```

可以看到“this is echo”的输出。即此处运行了exec程序，但exec程序实际上调用了exec系统调用，并用echo指令来代替自己，所以这里是**echo命令在产生输出。**

> **exec注意事项**

- **exec系统调用会保留当前的文件描述符表单**。所以任何在exec系统调用之前的文件描述符，例如0，1，2等。它们在新的程序中表示相同的东西。
- **一般而言exec系统调用不会返回**，因为exec会完全替换当前进程的内存，相当于当前进程不复存在了，所以exec系统调用已经没有地方能返回了。
- **exec系统调用只会当出错时才会返回**，因为某些错误会阻止操作系统为你运行文件中的指令，例如程序文件根本不存在，因为exec系统调用不能找到文件，exec会返回-1来表示：出错了，我找不到文件。

> **总结**

以上代码就是实现：一个程序利用另外一个程序代替自己。但实际应用中，我们不希望调用一个程序之后丢失控制权，对于这种还希望能拿回控制权的场景，可以先执行fork系统调用，然后在子进程中调用exec。

#### 1.4.5.2 fork/exec系统调用

> **fork/exec成功调用子进程代码**

```c
// forkexec.c:fork then exec

# include "kernel/types.h"
# include "user/user.h"

int main(){
    int pid,status;

    pid = fork();

    if(pid == 0){
        char *argv[] = {"echo","THIS","IS","ECHO",0};
        exec("echo",argv);
        printf("exec failed!\n");
        exit(1);
    }else{
        printf("parent waiting\n");
        wait(&status);
        printf("the child exited with status %d\n",status);
    }
    exit(0);
}
```

- 在上述代码中，首先调用了`fork`
- 子进程会利用`echo`命令代替自己，echo执行完成后就退出。
- 父进程会重新获得控制权，fork在父进程中返回大于0的值，父进程会继续在19行执行

运行输出:

```zsh
$ forkexec
parent waiting
THIS IS ECHO
the child exited with status 0
```

> **wait系统调用**

Unix提供了一个wait系统调用，**wait会等待之前创建的子进程退出**。

当我们在Shell命令行执行一个指令时，一般会希望Shell等待指令执行完成。所以wait系统调用，使得父进程可以等待任何一个子进程返回。

**wait参数 status**：是一种父进程与子进程之间的一种通信方式，他可以让退出的子进程以一个整数（32bit的数据）与等待的父进程通信。

所以在if语句中的最后一行`exit`的参数是1，操作系统会将1从退出的子进程传递到`wait(&status)`，即父进程的等待处。

`&status`，是将status对应的地址传递给内核，内核会向这个地址写入子进程向exit传入的参数。

> **UNIX中exit的传参风格**

- 如果一个程序成功退出，那么exit的参数即为0；
- 如果一个程序出现错误，那么exit的参数为1。

> **fork/exec调用子进程代码失败示例**

```c
// forkexec.c:fork then exec

# include "kernel/types.h"
# include "user/user.h"

int main(){
    int pid,status;

    pid = fork();

    if(pid == 0){
        char *argv[] = {"echo","THIS","IS","ECHO",0};
        // 调用了不存在的系统调用
        exec("sdfaddfaecho",argv);
        printf("exec failed!\n");
        exit(1);
    }else{
        printf("parent waiting\n");
        wait(&status);
        printf("the child exited with status %d\n",status);
    }
    exit(0);
}
```

运行输出：

```zsh
$ forkexec
parent waiting
exec failed!
the child exited with status 1
```

> **总结**

上述代码中我们使用了一个常用写法，即先调用`fork`,然后在子进程中调用`exec`。

这里需要注意的一点是，fork首先拷贝了整个父进程，之后exec将这个拷贝全部丢弃，某种程度上而言，这里的拷贝操作是浪费的。在大型程序中比较明显。

在后续课程中会针对这个问题实现优化，比如`copy-on-write fork`,这种方式会消除fork的几乎所有的明显的低效，而只拷贝执行exec所需要的内存，这里需要很多涉及到虚拟内存系统的技巧。

同时可以构建一个fork，对于内存实行lazy拷贝，通常来说fork之后立刻是exec，这样你就不用实际的拷贝，因为子进程实际上并没有使用大部分的内存。

### 1.4.6 I/O Redirect

Shell提供了方便的重定向工具，如果运行下述指令则表示: 

- Shell会将echo的输出送到文件out
- 之后运行cat指令，并将out文件作为输入

可以看到保存在out文件中的内容就是echo指令的输出。

```zsh
$ echo hello > out
$ cat < out
hello
```

> **redirect.c**

```c
// redirect.c: run a commond with output redirected

# include "kernel/types.h"
# include "user/user.h"
# include "kernel/fcntl.h"


int main(){
    int pid;

    pid = fork();

    if(pid == 0){
        close(1);
        open("output.txt",O_WRONLY|O_CREATE);

        char *argv[] = {"echo","this","is","redirected","echo",0};
        exec("echo",argv);
        prinf("exec failed!\n");
        exit(1);
    }else{
        wait((int *)0);
    }
    exit(0);
}
```

> **代码分析**

Shell之所以具备上述功能，是因为如上述代码所示:

- Shell首先会fork一个子进程，然后在子进程中Shell改变了文件描述符(在这里为"ouput.txt")，默认情况下为1，即console的输出文件符。该方法是Unix中的常见的用来重定向指令的输入输出的方法，这种方法同时又不会影响父进程的输入输出。因为我们不会想要重定向Shell的输出，我们只想重定向子进程的输出。

- 代码`close(1)`的意义是:我们希望文件描述符1指向一个其他的位置，即我们这里关闭原本指向console输出的文件描述符1

- 而因为刚关闭文件描述符1，所以代码`open("output.txt",O_WRONLY|O_CREATE);`一定返回1，因为`open`会返回当前进程未使用的最小文件描述符。而文件描述符`0`对应着console输入，`1`是我们刚刚关闭的最小文件描述符，所以open一定可以返回1，即执行完上述代码后文件描述符`1`与文件`output.txt`关联

- 之后我们执行exec(echo)，echo会输出到文件描述符1，也就是文件output.txt。但echo不清楚发生了什么。

> **运行输出**

```zsh
$ redirect
$ cat < output.txt
this is redirected echo
```
