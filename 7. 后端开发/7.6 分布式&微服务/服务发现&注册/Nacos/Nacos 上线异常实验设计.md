# 实验设计

1. 将ewp模块中，Nacos相关参数从Configure-Env中移除，配置到`boostrap.yml`文件中，注意此处配置的为开发环境的nacos_ip。
2. debug模式启动本地ewp服务，登录nacos服务列表平台，下线开发服务器中的ewp节点
3. 在相应的位置处添加断点
4. 更改`bootstrap.yml`文件中nacos_ip为字母`${NACOS_IP}`
5. 修改nacos配置中心的remote-ewp.yml配置文件，并使之生效
6. 进入断点观察


https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=spring%20boot%20%E5%88%B7%E6%96%B0bootstrap.yml%20%E4%B8%ADNacosIP&oq=spring%2520boot%2520%25E5%2588%25B7%25E6%2596%25B0bootstrap.yml&rsv_pq=bf407aa80001447f&rsv_t=6711zvWI5Tr4HRCuFPxLfXZm%2Fs%2FBbCBvSuPIZ%2FdZLtnakAN1ibwUeOTOXWo&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t&inputT=14334&rsv_sug3=226&rsv_sug1=187&rsv_sug7=100&rsv_sug2=0&rsv_sug4=18471 | spring boot 刷新bootstrap.yml 中NacosIP_百度搜索
http://www.javashuo.com/article/p-njqeekmm-ge.html | SpringBoot项目中的配置文件如何动态刷新 - JavaShuo
https://blog.csdn.net/Mr_Liu946/article/details/118898901 | 【精选】Springboot配置文件加载原理及流程【源码分析】_springboot加载配置文件源码_Mr_Liu946的博客-CSDN博客
https://blog.csdn.net/qq_49619863/article/details/129458433 | Nacos配置拉取及配置动态刷新原理【源码阅读】_配置中心动态刷新原理-CSDN博客
https://blog.csdn.net/Chenhui98/article/details/126299298?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-126299298-blog-129458433.235%5Ev38%5Epc_relevant_sort_base1&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-126299298-blog-129458433.235%5Ev38%5Epc_relevant_sort_base1&utm_relevant_index=1 | Nacos配置中心是如何实现动态刷新原理_nacos配置中心动态刷新-CSDN博客
https://blog.csdn.net/Apandam/article/details/130781918 | Nacos-04-@RefreshScope自动刷新原理_nacos自动刷新原理_Polarisy丶的博客-CSDN博客
https://blog.csdn.net/qq_39017153/article/details/132402409 | 如何实现Nacos配置文件动态刷新【四种方式】_nacos配置中心动态刷新_孟德爱吃香菜的博客-CSDN博客
https://blog.csdn.net/run65536/article/details/131477092 | 实现Nacos属性值自动刷新的三种方式_nacos配置中心动态刷新_琴剑飘零西复东的博客-CSDN博客
https://blog.csdn.net/hguisu/article/details/48788367 | Spring学习笔记(4)一SpringMVC启动原理和WebApplicationContext、ApplicationContextInitializer、ApplicationRunner机制_applicationrunner springmvc-CSDN博客
https://coding.m.imooc.com/questiondetail?cid=358&qid=282187 | nacos配置的生效时间
https://www.bilibili.com/ | 哔哩哔哩 (゜-゜)つロ 干杯~-bilibili
https://www.google.com.hk/search?q=nacos+%E9%85%8D%E7%BD%AE%E4%B8%AD%E5%BF%83%E6%9B%B4%E6%96%B0%E5%AF%BC%E8%87%B4%E6%9C%8D%E5%8A%A1%E4%B8%8B%E7%BA%BF&sca_esv=582627702&hl=zh-TW&biw=1920&bih=993&ei=kd9UZdntNrmF2roPpI284Ak&ved=0ahUKEwiZ-p-DpcaCAxW5glYBHaQGD5wQ4dUDCBA&uact=5&oq=nacos+%E9%85%8D%E7%BD%AE%E4%B8%AD%E5%BF%83%E6%9B%B4%E6%96%B0%E5%AF%BC%E8%87%B4%E6%9C%8D%E5%8A%A1%E4%B8%8B%E7%BA%BF&gs_lp=Egxnd3Mtd2l6LXNlcnAiKm5hY29zIOmFjee9ruS4reW_g-abtOaWsOWvvOiHtOacjeWKoeS4i-e6vzIFEAAYogRImUlQ2whY-0ZwAXgAkAEBmAHVBaAB5mOqAQY1LTE4LjK4AQPIAQD4AQHCAggQABiiBBiwA8ICBxAAGIoFGEPCAgUQABiABMICBBAAGB7CAgYQABgEGB7CAgUQIRigAeIDBBgBIEGIBgGQBgE&sclient=gws-wiz-serp#ip=1 | nacos 配置中心更新导致服务下线 - Google 搜尋
https://github.com/alibaba/spring-cloud-alibaba/issues/1297 | 只使用nacos配置中心的话 ,修改配置后eureka重新注册服务 需要3次以上才能注册成功 · Issue #1297 · alibaba/spring-cloud-alibaba · GitHub
https://github.com/alibaba/nacos/issues/8464 | Nacos 2.1.0 修改配置后服务掉线 · Issue #8464 · alibaba/nacos · GitHub
https://github.com/alibaba/nacos/issues/9959 | client心跳恢复正常后无法重新自动注册到server · Issue #9959 · alibaba/nacos · GitHub
https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=28114124_2_dg&wd=%40Order&oq=bootstrap.yml%25E5%258A%25A0%25E8%25BD%25BD%2520%25E5%25AE%25B9%25E5%2599%25A8%25E4%25BA%2586%25E5%2590%2597&rsv_pq=c7c8237d00a2ce86&rsv_t=5a95JcmrdXmubb0Xkh2e1CHbMK5QAdBe3zCt3W49iedQZ8RmHpSR5Lfp5OwSF7lysnWRBw&rqlang=cn&rsv_enter=0&rsv_dl=tb&sug=springbootbootstrap&rsv_btype=t&inputT=2837&rsv_sug3=583&rsv_sug1=352&rsv_sug7=100&rsv_sug2=0&rsv_sug4=4058 | @Order_百度搜索
https://www.cnblogs.com/wt20/p/17181602.html | 聊聊bootstrap.yml - wastonl - 博客园
https://blog.csdn.net/huang007guo/article/details/118939128 | 使用refreshScope.refresh导致Eureka服务下线_eureka 1.6的bug-CSDN博客
https://blog.csdn.net/qq_43141726/article/details/130791705 | [Nacos] Nacos Client获取所有服务和定时更新Client端的注册表 (三)_nacos 获取服务列表_959y的博客-CSDN博客
https://www.cnblogs.com/kurl88/p/15227288.html | nacos上的注册过的服务实例掉线分析 - kurl88 - 博客园
https://www.zhihu.com/question/554976827/answer/2685299010?utm_id=0 | (3 封私信) nacos是怎么处理刚修改配置,然后客户端掉线的这种情况的? - 知乎
https://blog.csdn.net/hlzdbk/article/details/129421842 | 28个案例问题分析---023---部分服务总是出现频繁掉线的情况--nacos，springCloud_nacos元数据丢失_郝老三的博客-CSDN博客
https://blog.csdn.net/qq_36628536/article/details/113753581 | 【精选】Spring学习之ContextRefreshr_contextrefresher_你的boy_Z的博客-CSDN博客
https://www.baidu.com/s?tn=28114124_2_dg&wd=nacos%20%E9%85%8D%E7%BD%AE%E4%B8%AD%E5%BF%83%E6%9B%B4%E6%96%B0%E5%AF%BC%E8%87%B4%E6%9C%8D%E5%8A%A1%E4%B8%8B%E7%BA%BF | nacos 配置中心更新导致服务下线_百度搜索
https://developer.aliyun.com/ask/555742 | 怎么Nacos1.4.6版本refreshScope.refresh配置更新导致注册的服务下线？-问答-阿里云开发者社区-阿里云