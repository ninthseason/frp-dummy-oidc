frp-dummy-oidc 是一个**无视规范的粗糙的但是可用的**仅适用于 frp 的 oidc provider

用于为 frp 的 oidc 验证模式提供 OP 服务

本工具使用 fastapi 以极简(陋)的方式实现了 frp 验证流程所需的三个终结点
- /.well-known/openid-configuration
- /.well-known/jwks.json
- /token

同时支持配置若干用户名和密码

> 声明: 
> - 本工具并不是一个用户管理系统, 故没有实现专业的用户管理功能, 用户的添加与删除需要手动于文件中进行, 且密码以明文保存在文件中
> - 因为我在实现本工具时根本没看规范，所以本工具可能存在漏洞(OIDC未定义的行为)
> - 本工具的开发目的是给我的几个朋友分发一份独立的账号密码(而非单调无趣的token), 用于访问我的frp服务. 任何除此之外的更大规模的使用行为不保证可用性和稳定性. 

### 依赖

> pip install fastapi uvicorn cryptography PyJWT

> 我使用的版本:
> fastapi==0.110.0
> uvicorn==0.29.0
> cryptography==39.0.1
> PyJWT==2.8.0

### 配置方法

本工具*并未*做到开箱即用, 在使用前仍需进行几个简单的步骤

1. 生成 RSA256 密钥
    你可以用任何你喜欢的方式生成密钥(pem格式, 公钥命名为public_key.pem, 私钥命名为private_key.pem, 放于项目文件夹下)

    推荐使用keygen.py脚本进行生成

    > 警告(虽然是老生常谈了): 请保护好你的私钥, 不要泄露给任何人.
2. 生成 JWK
    用任何你喜欢的方式将 PEM 格式的公钥转换为 JWK 格式

    你可以使用一些在线服务: https://irrte.ch/jwt-js-decode/pem2jwk.html
3. 在 server.py 中配置 ISSUER 和 JWKS
    修改 server.py 中 5-12 行.

    ISSUER 是你 oidc provider 服务所在的根 url(应形如`http://<yourdomain>:<port>`)
    JWKS 是存放第二步生成的 JWK 的数组, **注意你的 JWK 应该放在 JWKS 里面, 而不是整个替换掉 JWKS**
4. 配置用户
    用户名和密码保存在 user.toml 文件中, 每行为一个用户, 格式为`<用户名> = <密码>`, 如果还不知道怎么写可以参考user-example.toml

    注意, user.toml 不会热重载, 所以每次修改后必须重启服务端

#### 启动服务

> `uvicorn server:app`

#### 配置frp

frps.toml:

> auth.method = "oidc"
> auth.oidc.issuer = "http://127.0.0.1:8000"  # 替换成你的 ISSUER 地址

frpc.toml:

> auth.method = "oidc"
> auth.oidc.clientID = "admin"  # 用户名
> auth.oidc.clientSecret = "IAMTHEADMIN!"  # 密码
> auth.oidc.tokenEndpointURL = "http://127.0.0.1:8000/token"  # 替换成你的 ISSUER 地址


> 无需按官方文档配置 auth.oidc.audience
> 亦无需配置 auth.oidc.scope (在使用国内鉴权平台 authing 作为 oidc provider 时需要配置该属性)

#### 常见问题

因为无人使用，暂无常见问题.
