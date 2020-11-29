# 主要用来处理密码加密
import base64
import binascii
import hashlib
import os


def __b64encode_salt(random_salt: bytes) -> str:
    return base64.b64encode(random_salt).decode()


def __b64decode_salt(random_salt_b64: str) -> bytes:
    return base64.b64decode(random_salt_b64.encode())


def make_password(raw_password: str) -> (str, str):
    """
    加密密码,返回加密的密码值和随机盐
    :param raw_password:
    :return:
    """
    random_salt = os.urandom(16)
    password = hashlib.pbkdf2_hmac(
        "sha256", raw_password.encode("utf-8"), random_salt, 16
    )  # 随机生成盐值
    return binascii.hexlify(password).decode(), __b64encode_salt(random_salt)


def verify_password(raw_password: str, password: str, random_salt_b64: str) -> bool:
    """
    验证密码是否正确
    :param raw_password:要验证的密码
    :param password:数据库存储的密码
    :param random_salt_b64:数据库存储的随机盐
    :return:
    """
    random_salt = __b64decode_salt(random_salt_b64)
    raw_password = hashlib.pbkdf2_hmac("sha256", raw_password.encode("utf-8"), random_salt, 16)
    if binascii.hexlify(raw_password).decode() == password:
        return True
    else:
        return False
