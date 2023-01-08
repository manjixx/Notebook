# 软件安装与卸载

## JDK 安装与卸载

### MAC系统 JDK 卸载及彻底删除

- 1. 删除运行路径和运行环境等

```bash
sudo rm -fr /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin
sudo rm -fr /Library/PreferencesPanes/JavaControlPanel.prefPane
sudo rm -fr ~/Library/Application\ Support/Java
```

- 2. 删除当前版本的jdk

```bash
sudo rm -rf /Library/Java/JavaVirtualMachines/jdk-9.0.1.jdk   
```

注：不确定版本号先查看当前版本 

```bash
ls /Library/Java/JavaVirtualMachines/
```

- 3. 检查是否卸载成功

```bash
java -version
```

- 4. 参考链接

[Java官方](https://www.java.com/zh-CN/download/help/mac_uninstall_java.html)

### Mac 系统安装 Java

#### 安装步骤

- 下载安装包
  安装的jdk是Zulu维护的支持m1芯片，即arm架构的版本，[安装包下载地址](https://www.azul.com/downloads/)，下载.dmg格式安装包

- 点击安装
  
- 配置路径

```bash
# 查看安装路径
ls /Library/Java/JavaVirtualMachines/
jdk1.8.0_352.jdk

# 使用bash，编辑如下文件
vim .bash_profile 

# 使用zsh，编辑如下文件
vim  ~/.zshrc

# 再配置文件中输入如下内容，注意文件路径应该与自己电脑的匹配

JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_352.jdk/Contents/Home
PATH=$JAVA_HOME/bin:$PATH:.
CLASSPATH=$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar:.
export JAVA_HOME
export PATH
export CLASSPATH
```

- 使配置文件生效果

```bash
source .bash_profile 
```

- 查看是否安装成功
  
```bash
java -version
```

#### 参考资料

[M1 macOS安装java8/java11并动态切换](https://blog.csdn.net/q863672107/article/details/125453718)

[Mac M1 安装 JDK 1.8](https://www.jianshu.com/p/348da7c0df22)

## Nodejs 安装与卸载

### node 卸载

- 依次卸载如下内容
  
```bash
sudo npm uninstall npm -g

sudo rm -rf /usr/local/lib/node /usr/local/lib/node_modules /var/db/receipts/org.nodejs.*

sudo rm -rf /usr/local/include/node /Users/$USER/.npm

sudo rm /usr/local/bin/node

sudo rm /usr/local/share/man/man1/node.1

sudo rm /usr/local/lib/dtrace/node.d
```

- 执行如下命令验证是否删除成功

```bash
node -v
// -bash: /usr/local/bin/node: No such file or directory
npm -v

// -bash: /usr/local/bin/npm: No such file or directory
```

### 使用 Homebrew 安装 node

- 安装nvm

```bash
brew install nvm
```

- 编辑 .zshrc 文件

```bash
vim .zshrc

# 按i进入编辑模式

export NVM_DIR="$HOME/.nvm"
# This loads nvm
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  
# This loads nvm bash_completion
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" 

# 然后按 esc 退出编辑模式
# 按 :wq 保存并退出

# 更新配置环境变量
source .zshrc
```

- 查看nvm版本

```bash
nvm -v
```

- 安装node

```bash
nvm install 16.15.0
```

- nvm 常用语法

```bash
# 安装node指定版本
$ nvm install 版本号

# 查看本地node的所有版本
$ nvm list

# 切换到指定的node版本
$ nvm use 10.19

# 卸载指定的node版本
$ nvm uninstall 版本号

# 安装最新的node稳定版本
$ nvm install --lts

# 查看node的所有的版本
$ nvm ls-remote

# 使用node指定版本执行指定文件
$ nvm exec 版本号 node 要执行的文件路径

# 例如：nvm exec 4.8.3 node app.js  表示使用4.8.3 版本的node，执行app.js文件

# 设置默认版本的Node，每次启动终端都使用该版本的node
nvm alias default 版本号
```
