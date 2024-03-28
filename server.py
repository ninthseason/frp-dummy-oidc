from fastapi import FastAPI, Form
import tomllib
from sign import get_jwt

ISSUER = "http://127.0.0.1:8000"
JWKS = {
    "keys": [{
        "kty": "RSA",
        "e": "AQAB",
        "n": "ydF6lw_ldxcYwGOlswGAopDbM1TG-1QUIwYZ3Cwvt5ItkE9gxZceJqZwdoSTuR4lYQLTyP8m_O6Ymf9GzCDxT96dOkMwSp8GZa9cVo2fpb0VYTf2xEj7MrajsBlAvgtNxT3N3ufSQ439r2LMEs904MShSeAVdh9C-3CBvPbh1Pdt1JKTkwp025_5p4BFH4PUEBIDvjkCWSGYkwdQx-PGql6B76HtRrZUKtbQuVoXK_aWdAo2sHCS9vkb1Jc-uBIa0nlneLTpDKByTLNKj880vIaruEHAFpA2DXGE6D4DTbVnnr2pRN6FOkxwqjWlY8bdIdOG4Ksa-6CJuvUY11sL9Q","alg":"RS256","use":"sig"
    }]
}

# 读取/创建用户列表
# user.toml 每行格式应为:
#   username = "password"
# 具体样例见 user-example.toml
try:
    with open("user.toml", "rb") as f:
        user_table = tomllib.load(f)
except FileNotFoundError:
    with open("user.toml", "w") as _:
        user_table = {}

print(user_table)
app = FastAPI()

# frps启动时从这获取openid基本信息
@app.get("/.well-known/openid-configuration")
async def meta():
    return {"issuer": ISSUER, "token_endpoint": ISSUER + "/token", "jwks_uri": ISSUER + "/.well-known/jwks.json"}

# frps在验证签名时需要从这获取公钥
@app.get("/.well-known/jwks.json")
async def jwks():
    return JWKS

# frpc启动时从这获取token
@app.post("/token")
async def token(client_id: str = Form(), client_secret: str = Form()):
    print("login attampt:", client_id, client_secret)
    if (password := user_table.get(client_id)) is not None:
        if password == client_secret:
            return {
                "access_token": get_jwt(ISSUER),
                "token_type": "Bearer",
            }
        else:
            print(f"密码错误: {client_id}:{client_secret}")
            return { "err": "密码错误" }
    else:
        print(f"账号不存在: {client_id}")
        return { "err": "账号不存在" }

