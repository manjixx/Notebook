# Nacos 配置中心源码解析

## 三、服务端源码分析

Nacos配置中心的服务端源码主要在 nacos-config 项目的ConfigController 类中

### 3.1 处理长轮询

```java
 /**
     * The client listens for configuration changes.
     */
    @PostMapping("/listener")
    @Secured(action = ActionTypes.READ, parser = ConfigResourceParser.class)
    public void listener(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setAttribute("org.apache.catalina.ASYNC_SUPPORTED", true);
        String probeModify = request.getParameter("Listening-Configs");
        if (StringUtils.isBlank(probeModify)) {
            throw new IllegalArgumentException("invalid probeModify");
        }
        
        probeModify = URLDecoder.decode(probeModify, Constants.ENCODE);
        
        Map<String, String> clientMd5Map;
        try {
            clientMd5Map = MD5Util.getClientMd5Map(probeModify);
        } catch (Throwable e) {
            throw new IllegalArgumentException("invalid probeModify");
        }
        
        // do long-polling
        inner.doPollingConfig(request, response, clientMd5Map, probeModify.length());
    }
```

## 参考资料

[](https://blog.csdn.net/m0_73311735/article/details/129491922)