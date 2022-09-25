# MIT 6.S081/Fall 2020 搭建risc-v与xv6开发调试环境

## 一、环境说明

电脑型号：MacBook Pro (14-inch, 2021)

系统版本：macOS Monterey 12.3.1

芯片：M1芯片，arm64架构

## 二、基础配置

### 2.1 brew

```bash
# 查看brew版本
brew -v

# 安装基本依赖环境
brew install python3 gawk gnu-sed gmp mpfr libmpc isl zlib expat gsed
brew tap discoteq/discoteq
brew install flock

# Qemu 需要依赖ninja
brew install ninja
```

- Error
  - 1. 执行```brew install python3 gawk gnu-sed gmp mpfr libmpc isl zlib expat gsed```
    - 错误信息 1
  
    ```bash
    # 报错
    fatal: not in a git directory
    Error: Command failed with exit 128: git
    ```

    - 解决方案-更新brew，报新的错误
  
    ```bash
    brew update 
    Warning: No remote 'origin' in /opt/homebrew/Library/Taps/homebrew/ homebrew-core, skipping update!
    Warning: No remote 'origin' in /opt/homebrew/Library/Taps/homebrew/homebrew-services, skipping update!
    ```

    - 解决更新brew的警告
  
    ```bash
    # 依次替换以下brew源
    # 更新Homebrew
    cd "$(brew --repo)"
    git remote set-url origin https://mirrors.ustc.edu.cn/brew.git
    # 更新Homebrew-core
    cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
    git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git

    # 报错
    fatal: unsafe repository ('/opt/homebrew/Library/Taps/homebrew/homebrew-core' is owned by someone else)
    To add an exception for this directory, call:

    # 解决方案
    git config --global --add safe.directory /opt/homebrew/Library/Taps/homebrew/homebrew-core

    # 更新Homebrew-cask（最重要的一步，很多更新完国内源依然卡就是没更新这个）
    cd "$(brew --repo)"/Library/Taps/homebrew/homebrew-cask
    git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-cask.git

    # 执行
    echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles/' >> ~/.zshrc
    source ~/.zshrc
    ```

    - 备注： 当执行下述语句出现如下问题时，可采用方法
  
    ```bash
    (base) iiixv@IIIXVdeMacBook-Air homebrew-services % git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-services.git
    fatal: unsafe repository ('/opt/homebrew/Library/Taps/homebrew/homebrew-services' is owned by someone else)
    To add an exception for this directory, call: git config --global --add safe.directory /opt/homebrew/Library/Taps/homebrew/homebrew-services
    (base) iiixv@IIIXVdeMacBook-Air homebrew-services %git config --global --add safe.directory /opt/homebrew/Library/Taps/homebrew/homebrew-services

    ```

### 2.2 关于 GCC / LLVM + CLANG（可选）

Mac 默认情况下预装的环境是 LLVM+CLANG 而不是 GCC 虽然有 GCC 的命令 但是其实是 CLANG

测试如下 执行 gcc -v:

```sh
gcc -v
Configured with: --prefix=/Library/Developer/CommandLineTools/usr --with-gxx-include-dir=/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/4.2.1
Apple clang version 13.0.0 (clang-1300.0.29.30)
Target: arm64-apple-darwin21.2.0
Thread model: posix
InstalledDir: /Library/Developer/CommandLineTools/usr/bin
```

在编译 riscv-gnu-toolchain (opens new window)工具链的时候，本机是 GCC 还是 LLVM+CLANG 都不会影响，我亲测都可以编译成功，所以这个地方可以保持默认，如果需要安装GCC 来替换 LLVM + CLANG 可以按照以下步骤操作:

```bash
# 安装
brew install gcc
# 版本为gcc 11.2.0_3
# 设置环境变量: 
# 把以下内容添加到 ~/.zshrc 或者 ~/.bash_profile  或者 /etc/profile
# 因为我使用的是zsh 所以配置到 ~/.zshrc 里
vim ~/.zshrc
# 增加以下内容 
export GCCPATH=/opt/homebrew/Cellar/gcc/11.2.0_3/
export PATH=$PATH:${GCCPATH//://bin:}/bin
alias gcc='gcc-11'
alias cc='gcc-11'
alias g++='g++-11'
alias c++='c++-11'
# 使环境生效
source ~/.zshrc
# 测试
gcc -v
Using built-in specs.
COLLECT_GCC=gcc-11
COLLECT_LTO_WRAPPER=/opt/homebrew/Cellar/gcc/11.2.0_3/bin/../libexec/gcc/aarch64-apple-darwin21/11/lto-wrapper
Target: aarch64-apple-darwin21
....省略
Thread model: posix
Supported LTO compression algorithms: zlib zstd
gcc version 11.2.0 (Homebrew GCC 11.2.0_3)

```

### 2.3 安装 riscv-gnu-toolchain

原文档提供两种安装方式

#### 2.3.1 使用 brew 进行安装（可选）

我用了这个步骤安装 会出现一些问题 所以此处需要看运气了。

```sh
brew tap riscv-software-src/riscv
brew install riscv-tools
```

#### 2.3.2 源码编译安装（可选）

##### 2.3.2.1 克隆源码

```sh
git clone --recursive https://github.com/riscv/riscv-gnu-toolchain
```

源码很大 6.5G左右 所以克隆的时候会很慢 可以先克隆主仓库 分开克隆子仓库

```sh
git clone https://github.com/riscv/riscv-gnu-toolchain
cd riscv-gnu-toolchain
git submodule update --init --recursive
```

百度云中下载我这边上传好的 可以直接下载解压

地址：[源码包](https://pan.baidu.com/s/1iDNpV2_UTWk4OwZx0Bv2YA#list/path=%2F) 提取码：nmvw 包名： riscv-gnu-toolchain-src-2022-01-17.tar.gz

##### 2.3.2.2 编译安装

注: 如果你的 Mac 是 arm 架构 M1 系列的芯片 需要改个配置

```bash
# 进入目录
cd riscv-gnu-toolchain
# 注销配置
# 编辑文件 
vim riscv-gcc/gcc/config.host
# 注销96行 97行
96     #out_host_hook_obj=host-darwin.o
97     #host_xmake_file="${host_xmake_file} x-darwin"
```

编译

```bash
cd riscv-gnu-toolchain

./configure --prefix=/opt/riscv-gnu-toolchain --with-cmodel=medany --enable-multilib

# 因为安到opt目录下所以加了sudo 如果不安装在这个目录下 可以不使用sudo
sudo make
```

配置环境变量

```bash
# 把以下内容添加到 ~/.zshrc 或者 ~/.bash_profile  或者 /etc/profile
# 因为我使用的是zsh 所以配置到 ~/.zshrc 里
export RISCV_HOME=/opt/riscv-gnu-toolchain
export PATH=${PATH}:${RISCV_HOME}/bin
# 用 source 命令 让环境变量重新加载
source ~/.zshrc 
```

### 2.4 安装 Qemu

Qemu 是强大的虚拟机操作系统模拟器，在此课程中，我们使用 qemu 来模拟硬件 ，使 xv6 运行在该模拟器之上。

我安装的 qemu 版本为 6.2.0

以下安装选一个即可 你怎么开心怎么选 我用的是 1.使用 brew 安装

#### 2.4.1 使用brew安装

```bash
brew install qemu
```

#### 2.4.2 使用源码安装（可选）

下载源码并进行编译

```bash
wget https://download.qemu.org/qemu-6.2.0.tar.xz

tar xf qemu-6.2.0.tar.xz

cd qemu-6.2.0

./configure --prefix=/opt/qemu

make 

make install
```

配置环境变量

```bash
# 把以下内容添加到 ~/.zshrc 或者 ~/.bash_profile  或者 /etc/profile
# 因为我使用的是zsh 所以配置到 ~/.zshrc 里
export QEMU_HOME=/opt/qemu
export PATH=${PATH}:${QEMU_HOME}/bin
# 用 source 命令 让环境变量重新加载
source ~/.zshrc 
```

#### 2.4.3.验证是否安装成功

```bash
// 执行 如果打印以下内容代表安装成功
qemu-system-riscv64 --version
QEMU emulator version 6.1.0
Copyright (c) 2003-2021 Fabrice Bellard and the QEMU Project developers
```

### 2.5 编译及运行 xv6

#### 2.5.1 克隆

```bash
git clone https://github.com/mit-pdos/xv6-riscv.git
```

#### 2.5.2 编译

```bash
cd xv6-riscv
make
```

#### 2.5.3 使用 qemu 运行

```bash
make qemu
```

### 2.6 使用 qemu-gdb 对 xv6进行调试

需要2个终端窗口

#### 2.6.1 窗口1

```bash
cd xv6-riscvbash
make CPUS=1 qemu-gdb
```

运行成功后显示如下内容

```bash
sed "s/:1234/:25501/" < .gdbinit.tmpl-riscv > .gdbinit
*** Now run 'gdb' in another window.
qemu-system-riscv64 -machine virt -bios none -kernel kernel/kernel -m 128M -smp 1 -nographic -drive file=fs.img,if=none,format=raw,id=x0 -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 -S -gdb tcp::25501
```

#### 2.6.2 窗口2

```bash
cd xv6-riscv
riscv64-unknown-elf-gdb
```

显示如下内容表示并未成功加载

```bash
GNU gdb (GDB) 10.1
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "--host=arm-apple-darwin21.4.0 --target=riscv64-unknown-elf".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word".
warning: File "/Users/iiixv/xv6-riscv/.gdbinit" auto-loading has been declined by your `auto-load safe-path' set to "$debugdir:$datadir/auto-load".
To enable execution of this file add
	add-auto-load-safe-path /Users/iiixv/xv6-riscv/.gdbinit
line to your configuration file "/Users/iiixv/.gdbinit".
To completely disable this security protection add
	set auto-load safe-path /
line to your configuration file "/Users/iiixv/.gdbinit".
For more information about this security protection see the
--Type <RET> for more, q to quit, c to continue without paging--

```

解决方案：

xv6-riscv 目录下有 .gdbinit 配置 有的情况下 riscv64-unknown-elf-gdb 会自动加载，如果没有.gdbinit则需要你手动 source .gdbinit 当打印 0x0000000000001000 in ?? () 代表可以调试。

> ## 参考

[MIT 6.S081/Fall 2020 搭建risc-v与xv6开发调试环境](https://yaoyao.io/views/post/MIT6S081-install-riscv-qemu-xv6.html#%E6%88%91%E7%9A%84%E7%8E%AF%E5%A2%83)

---

# 版本控制

## 一、分支切换

1. 查看是否有.git目录

```zsh
ls -a         //输出.    ..   .git
```

2. 查看其他分支

```zsh
git branch -r  //输出你的分支名称
```

3. 切换目标分支

```zsh
git checkout 分支名
```

4. 拉取代码

```zsh

```

## 二、将实验代码提交到github

1. 首先将mit的实验代码克隆到本地

```zsh
git clone git://g.csail.mit.edu/xv6-labs-2020
```

2. 在github创建一个新的仓库

3. 添加git仓库地址

```zsh
git remote add github 你的仓库地址
cat .git/config
```

4. 将实验代码推送到git仓库

例如将实验1的util分支线推送到github

```zsh
git checkout util
git push github util:util
```

5. xv6实验git分支建议

建议是每个实验创建一个测试分支，例如对于util来说

```zsh
git checkout util         # 切换到util分支
git checkout -b util_test # 建立并切换到util的测试分支
```

当你在util_test分支中每测试通过一个作业，请提交（git commit）你的代码，并将所做的修改合并（git merge）到util中，然后提交（git push）到github

```zsh
git add .
git commit -m "完成了第一个作业"
git checkout util
git merge util_test
git push github util:util
```