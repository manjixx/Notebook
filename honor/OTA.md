
# OTA 服务概述

## 常见缩略语

- OTA(Over the Air): 在线更新服务
- HOTA(Honor Over The Air): XX在线更新服务
	- TUS(Terminal  Unified Portal Server): 终端升级管理服务器
	- TQS(Terminal Query Server): 终端升级查询服务器
	- TDS(Terminal  Download Server): 终端升级下载服务器

- COTA(Customization Over The Air): 定制在线更新服务
  - CPS(Cota protal Service): Cota前端门户服务
  - CQS(Cota Query Service): Cota 业务查询服务

- POTA(Plugin Over the Air):插件在线更新服务

- ECOTA(Enterprise Customization Over the Air):企业定制在线服务 

- BQS(Baseline Version Query Service):BL泳道及版本查询服务

- BMS(Baseline Manage Server):BL泳道及版本管理服务

- CABE(Customization Asset Backend):定制资产(应用)后端服务，用于承载独立更新的应用

- CDN (Content Delivery Network): 内容分发网络
  
   CDN是构建在现有网络基础之上的智能虚拟网络，依靠部署在各地的边缘服务器，通过中心平台的负载均衡、内容分发、调度等功能模块，使用户就近获取所需内容，降低网络拥塞，提高用户访问响应速度和命中率。CDN的关键技术主要有内容存储和分发技术。

## 云计算

### 什么是云计算？

-  痛点：
	- IT三大基础设施资源：计算(CPU + 内存)、网络、存储
	- 传统IT模式下，资源利用率低、费用昂贵、业务上线时间长、维护周期长

- 早期云计算
	- 就是简单一点的分布式计算，解决任务分发，计算结果合并就好了。也曾经还有一个别名，叫网格计算。
	-  VMware、Virtual PC、GAE、SAE、云盘

- 逐渐成熟的云计算
	
	很多大企业早期可能也只是想解决自己的效率与计算问题，到后来，这些大佬发现，这个能力也可以提供给外部使用，所以，就出现了公共云（public cloud）计算 ，把计算机的计算能力直接放在网上卖出去。

	- 基于网络的提供资源共享的远端服务，共享的软硬件资源和信息按需提供给使用此类资源进行计算和其他业务部署的需求者

	- 虚拟化是云计算基础架构的核心，是云计算发展的基础 

## 云计算架构

![云计算架构](https://pic3.zhimg.com/80/v2-07b42a077d6ea92d95d0ac7513ec0d86_720w.jpg)

- IaaS (Infrastructure as a Service)，又称I层，基础设施即服务，是最底层的硬件资源，主要包括CPU（计算资源），硬盘（存储资源），还有网卡（网络资源）

- PaaS(Platform as a Service), 又称P层，平台即服务，提供类似操作系统和开发工具的功能，通过互联网为用户提供一整套开发、运行和运营应用软件的支撑平台

- SaaS(Software as a Service),又称S层，软件即服务，通过互联网提供软件服务的软件应用模式。用户不需要再花费大量投资用于硬件、软件和开发，只需要支付一定的租赁费用，就可以享受到相应的服务。

- DaaS(Data as a Service),又称D层，数据即服务，通过获取别人的数据作为自己的服务。

## 云计算管理平台

通过命令或者基于Web可视化控制面板来管理IaSS云端的资源池(服务器、存储和网络)
![云计算管理平台](https://pica.zhimg.com/v2-6fdd17f5eecc1a05605a6629210cc18a_1440w.jpg?source=172ae18b)
[九大开源云管理平台](https://cloud.tencent.com/developer/news/494035)

















