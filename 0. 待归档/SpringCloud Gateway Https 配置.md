# Spring Cloud Gateway HTTPS 配置

application.yml中配置SSL如下所示：

```yml
server:
  ssl:
    enabled: true
    key-alias: scg
    key-store-password: scg1234
    key-store: classpath:scg-keystore.p12
    key-store-type: PKCS12
```

Spring Cloud Gateway可以路由请求到 http 或 https 的服务，如果是将请求路由到https服务，可以通过下面的配置，让网关信任所有的后面服务的证书：

```yml
spring:
  cloud:
    gateway:
      httpclient:
        ssl:
          useInsecureTrustManager: true
```

这种配置方式不适合用于生产环境，在生产环境中，可以在网关这里配置一些信任的证书，如下面配置所示：

```yml
spring:
  cloud:
    gateway:
      httpclient:
        ssl:
          trustedX509Certificates:
          - cert1.pem
          - cert2.pem
```

如果没有给网关配置可以信任的证书，那么这些默认的证书将被使用，不过，这些配置可以被系统属性设置（javax.net.ssl.trustStore）覆盖。