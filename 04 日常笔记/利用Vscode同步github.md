# 利用Vscode同步github

+ 首先需要对本地项目文件夹进行配置
    详见MAC配置git与文件同步

+ 使用Vscode打开该文件夹

+ 点击右侧功能栏——源代码管理：此处进行项目文件同步的地方，如果没有对文件进行修改或者添加删除，则不会显示需要进行同步的文件。

+ 修改后的文件，则会显示在源代码管理界面
  
  ![1](./picutre/../picture/%20利用Vscode同步github1.jpg)


+ 点击图中红框所指的加号，其作用类似于上述终端输入git add filename
  ![2](./picutre/../picture/%20利用Vscode同步github2.jpg)

+ 之后点击左边箭头所指的确认勾，就会在右边箭头所指的地方让你添加修改的注释，添加后回车
    ![3](./picutre/../picture/%20利用Vscode同步github3.jpg)

+ 这时可以看到vscode最下方状态栏有一个待上传的任务，点击确认勾右边的三点标号，选择推送即可。再次刷新项目仓库网站，就可以看到修改后的同步文件了。
    ![4](./picutre/../picture/%20利用Vscode同步github4.png)