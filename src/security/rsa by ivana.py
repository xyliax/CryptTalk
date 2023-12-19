def run():
    return "hello from python"


from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5

def CreateKeys():
    # ramdom creator
    random_generator = Random.new().read

    rsa = RSA.generate(1024, random_generator)
    # creating securate key
    private_pem = rsa.exportKey()
    with open("private.pem", "wb") as f:
        f.write(private_pem)
    # creating public key
    public_pem = rsa.publickey().exportKey()
    with open("public.pem", "wb") as f:
        f.write(public_pem)

def encrypt(plain_text):
    rsakey = RSA.importKey(open("public.pem").read())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 创建用于执行pkcs1_v1_5加密或解密的密码
    cipher_text = base64.b64encode(cipher.encrypt(plain_text.encode('utf-8')))
    return cipher_text

def decrypt(cipher_text):
    encrypt_text = cipher_text.encode('utf-8')
    rsakey = RSA.importKey(open("private.pem").read())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 创建用于执行pkcs1_v1_5加密或解密的密码
    text = cipher.decrypt(base64.b64decode(encrypt_text), "解密失败")
    return text.decode('utf-8')

def sign(message):
    rsakey = RSA.importKey(open("private.pem").read())
    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode("utf-8"))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    return signature.decode('utf-8')

def verify(message, signature):
    rsakey = RSA.importKey(open("public.pem").read())
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    hsmsg = SHA.new()
    hsmsg.update(message.encode("utf-8"))
    is_verify = verifier.verify(hsmsg, base64.b64decode(signature))
    return is_verify

# reference https://www.cnblogs.com/deliaries/p/13445277.html