# 配置文件详解

```yaml
spring:
    cloud:
        gateway:
            httpclient:
                ssl:
                    trusted-x509-certificates:   # 网关配置信任证书
                        - classpath: ca.crt
                    key-store: classpath:remote-keystore.jks  # 密钥管理器，可以存储密钥对和证书，但不能用于存储密钥
                    key-store-password:
                    key-password:
                    key-store-type: JKS


server:
    ssl:
        keystore:               # 密钥库
        key-password:           #  指定别名条目的密码(私钥的密码)
        key-store-password:     # 指定密钥库的密码(获取keystore信息所需的密码)
        key-alias:              # 别名
        enabled: true           # 开启 SSL
        ciphers:                # 支持的SSL密码
        protocol: TLS           # 使用的协议
        enabled-protocols: TLSv1.2  #  启用 SSL 协议
        key-store-type: JKS     # 
        # whether client authentication is wanted ( "want" ) orneeded ( "need " ) . Requires a trust store.
        client-auth: none       # 是否需要客户端身份验证
        trust-store:            # 存放 sSL 证书的信任存储。truststore是放信任的证书的一个store。truststore和keystore的性质是一样的，都是存放key的一个仓库，区别在于，truststore里存放的是只包含公钥的数字证书，代表了可以信任的证书，而keystore是包含私钥的。
        turst-store-password:   # 用于访问信任存储的密码。
        turst-store-type:       # 信任存储的类型。
        expire-alert-days:      # 过期期限

client:
    ssl:
        trust-store:
        trust-store-password:
        trust-store-type:
        key-store-enable:
        key-store:
        key-store-password:
        key-password:
        key-alias:
        key-store-type:
```

## SAML 扩展

Spring Security SAML 身份认证和授权翻译。

SAML 扩展需要配置安全设置，其中包括用于数字签名和加密的加密材料、用于配置远程实体提供的可信加密材料的安全配置文件以及 HTTPS 连接的验证。

Spring Security SAML 扩展了 Spring Security 核心库，支持 SAML 标准，允许应用与任何SAML兼容的身份提供者（Identity Provider, IdP）进行交互。这使得企业可以方便地将内部或外部服务统一管理，无需每个系统都独立处理认证和授权问题。

技术名词：

- SAML协议：SAML 是一种 XML-based 的标准，用于在 Web 应用之间传输安全信息，如用户身份、权限等。Spring Security SAML通过实现SAML协议的各种角色（如Service Provider和服务提供者IdP），确保数据的安全交换。

- SSO集成：该项目简化了SSO的配置和实施过程。只需几个步骤，即可让Spring Boot应用支持SAML SSO，减轻开发负担。

- 灵活性：Spring Security SAML提供了丰富的API和配置选项，以适应不同企业的复杂需求。无论是自定义认证流程，还是对接不同的IdP，都能灵活应对。

- 安全性：利用Spring Security的强大安全机制，Spring Security SAML可防止常见的网络攻击，如XSS、CSRF等，并支持SSL/TLS加密通信，保护用户信息不被窃取。

- 易于集成：由于其与Spring生态系统的紧密关系，Spring Security SAML能轻松与其他Spring组件（如Spring MVC、Spring Boot）集成，无须大量修改现有代码。

```yaml

# auth 里的 saml 扩展
saml:
    keystore: remote_ca.jks     # key store file
    keyalias:                   # 别名
    certificatepath:            #
    digestAlgorithm:
    signatureAlgorithm:
    loginurl:
    diagest:
        sha256:
        rsaSha256:
    validServiceUrl:
    source:
    storepassword:
    keypassword:

server:
    ssl:
        key-store:
        key-password:
        key-alias:
        enabled:
        ciphers:
        protocol: TLS
        enabled-protocols: TLSv1.2
        key-store-type: JKS
        client-auth: need
        trust-store: 
        turst-store-password:
        turst-store-type:
        expire-alert-days:

client:
    ssl:
        trust-store:
        trust-store-password:
        trust-store-type:
        key-store-enable:
        key-store:          # 密钥管理器
        key-store-password:
        key-password:
        key-alias:
        key-store-type:
```

### 2.1 密钥管理

SAML 交换涉及使用加密技术对数据进行签名和加密。所有与加密密钥的交互都是通过接口`org.springframework.security.saml.key.KeyManager`完成的。默认实现 `org.springframework.security.saml.key.JKSKeyManager` 依赖于包含所有私钥和公钥的单个 `JKS` 密钥存储。

`KeyManager` 应至少包含一个私钥，应通过使用私钥的别名作为`JKSKeyManager`构造函数的一部分将其标记为默认值。

如果您的应用程序不需要创建数字签名和/或解密传入消息，则可以使用不需要任何 JKS 文件的密钥库的空实现 - `org.springframework.security.saml.key.EmptyKeyManager`。例如，仅使用 IDP 初始化的单点登录时可能会出现这种情况。请注意，使用 EmptyKeyManager 时，某些 Spring SAML 功能将不可用。这至少包括 SP 初始化的单点登录、单点注销、扩展元数据中附加密钥的使用以及元数据签名的验证。

```txt
javax.net.ssl.SSLHandshakeException:no subject alternative names present
```