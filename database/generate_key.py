import secrets
import string


def generate_encryption_key(length=43):
    if length != 43:
        raise ValueError("Length must be exactly 43 characters.")

    characters = string.ascii_letters + string.digits
    encryption_key = ''.join(secrets.choice(characters) for i in range(length))
    return encryption_key


# 使用函数生成一个43位长度的加密密钥
encryption_key = generate_encryption_key()
print(encryption_key)
