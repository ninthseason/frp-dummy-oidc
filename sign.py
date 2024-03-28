from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.backends import default_backend  
from jwt import encode, decode, PyJWTError
import time


with open("private_key.pem", "rb") as key_file:  
    private_key = serialization.load_pem_private_key(  
        key_file.read(),  
        password=None,  
        backend=default_backend()  
    )  
  
header = {
    "typ": "JWT",
    "alg": "RS256",
}

def payload(issuer: str, valid_duration=10):
    return {
        "aud": "may be useful, but not now",
        "iat": int(time.time()),
        "exp": int(time.time()) + valid_duration,
        "iss": issuer
    }

# 根据issuer和有效时间创建jwt, 没什么好说的
def get_jwt(issuer: str, valid_duration=10):
    return encode(headers=header, payload=payload(issuer, valid_duration), key=private_key, algorithm='RS256')


if __name__ == "__main__":
    # 以下是测试代码
    # 使用私钥对JWT进行签名  
    encoded_jwt = get_jwt("http://127.0.0.1:8000") 
    print("Encoded JWT:", encoded_jwt)  

    with open("public_key.pem", "rb") as key_file:  
        public_key = serialization.load_pem_public_key(  
            key_file.read(),  
            backend=default_backend()  
        )  

    # 使用公钥验证JWT  
    try:  
        decoded_jwt = decode(encoded_jwt, public_key, algorithms=['RS256'], audience="may be useful, but not now")  
        print("Decoded JWT:", decoded_jwt)  
    except PyJWTError as e:  
        print("JWT verification failed:", e)