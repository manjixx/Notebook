# Kafak常见面试题

## 一、基础知识

### 1.1 Kfaka是什么，主要应用场景有哪些？

Kfaka是一个分布式流处理平台，流平台有三个关键功能:

1. 消息队列:发布和订阅消息流，这个功能类似于消息队列，这也是 Kafka 也被归类为消息队列的原因。
2. 容错的持久方式存储消息流:Kafka 会把消息持久化到磁盘，有效避免了消息丢失的风险。
3. 流式处理平台:在消息发布时处理，Kfaka提供了一个完整的流式处理库

应用场景：

1. 消息队列：建立实时流数据管道，以可靠地在系统或应用程序之间获取数据。
2. 数据处理：Kafka 会把消息持久化到磁盘，有效避免了消息丢失的风险。

### 1.2 队列模型

早期的消息模型，使用队列（Queue）作为消息通信载体，满足生产者与消费者模式，一条消息只能被一个消费者使用，未被消费的消息在队列中保留直到被消费或超时。

### 1.3 Kfaka的消息模型:发布和订阅模型

![](https://guide-blog-images.oss-cn-shenzhen.aliyuncs.com/java-guide-blog/%E5%8F%91%E5%B8%83%E8%AE%A2%E9%98%85%E6%A8%A1%E5%9E%8B.png)

- 使用主题（Topic） 作为消息通信载体，类似于广播模式；
- 发布者发布一条消息，该消息**通过主题**传递给所有的订阅者，在一条消息广播之后才订阅的用户则是收不到该条消息的。

### 1.4 什么是Producer、Consumer、Broker、Topic、Partition

![](https://guide-blog-images.oss-cn-shenzhen.aliyuncs.com/github/javaguide/high-performance/message-queue20210507200944439.png)

- **Producer（生产者）** : 产生消息的一方。
- **Consumer（消费者）** : 消费消息的一方。
- **Broker（代理）** : 可以看作是一个独立的 Kafka 实例。多个 Kafka Broker 组成一个 Kafka Cluster。
- **Topic（主题）** : Producer 将消息发送到特定的主题，Consumer 通过订阅特定的 Topic(主题) 来消费消息。
- **Partition（分区）** : **Partition 属于 Topic 的一部分。** 一个 Topic 可以有多个 Partition ，并且同一 Topic 下的 Partition 可以分布在不同的 Broker 上，这也就表明一个 Topic 可以横跨多个 Broker 。这正如我上面所画的图一样。

### 1.5 Kfka多副本机制

Kafka会为Partition引入多个副本。副本中有一个叫leader的副本，多个follower副，发送的消息会被发送到leader副本，然后follower从leader副本拉取消息进行同步。

生产者与消费者只与leader副本交互，follower副本可以理解为leader副本的拷贝，存在只是为了消息存储的安全性。

### 1.6 Kafka分区与多副本机制的优点

1. Kafka通过给特定的Topic指定多个Partition，而各个Partition可以分布到不同Broker上，这样可以提供较好的并发能力
2. 多副本机制则提高了消息存储的安全性，提高了容灾能力。

### 1.7 Zookeeper在Kafka中的作用

1. Broker注册管理
2. Topic注册管理
3. 负载均衡

### 1.8 Kafka如何保证消息发送顺序

1. 一个消息只对应一个Topic
2. 发送消息时指定key/Partition,保证同一个key的消息只发送到同一个Partition

### 1.9 Kafka 如何保证消息不丢失

- 生产者丢失：重发机制、注意重发次数与重发间隔
- 消费者丢失:关闭自动提交offset，改为每次消费结束后手动提交offset。
- Kafka丢失: 
  - 配置 acks = all 代表则**所有副本都要接收到该消息之后该消息才算真正成功被发送。**
  - 设置 replication.factor >= 3:保证每个 分区(partition) 至少有 3 个副本。
  - 设置 min.insync.replicas> 1 ，这样配置代表消息至少要被写入到 2 个副本才算是被成功发送。

### 1.10 Kfka如何保证消息不重复消费

- 消费消息服务做幂等校验
- 自动关闭提交设置为false。