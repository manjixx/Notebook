# 前言


# 一、Ajax简介

## 1.1 什么是AJAX?

**AJAX = Asynchronous JavaScript + XML（异步 JavaScript 和 XML）**

AJAX 是一种用于创建快速动态网页的技术。 其本身不是一种新技术，而是一个在 2005 年被 Jesse James Garrett 提出的新术语，用来描述一种使用现有技术集合的‘新’方法，包括：HTML 或 XHTML, CSS, JavaScript, DOM, XML, XSLT, 以及最重要的 XMLHttpRequest。

简单点说，就是使用 `XMLHttpRequest` 对象与服务器通信。

它可以使用 JSON，XML，HTML 和 text 文本等格式发送和接收数据。AJAX 最吸引人的就是它的“异步”特性，也就是说**它可以在不重新刷新页面的情况下与服务器通信，交换数据，或更新页面。**

传统的网页（不使用 AJAX）如果需要更新内容，必需重载整个网页面。

**使用Ajax最主要的两个特性做如下事情**
- 在不重新加载页面的情况下发送请求给服务器。
- 接受并使用从服务器发来的数据。
