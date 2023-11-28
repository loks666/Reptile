import secrets
import string

print()


def generate_token(length=32):
    if not 3 <= length <= 32:
        raise ValueError("Length must be between 3 and 32 characters.")

    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for i in range(length))
    return token


# 使用函数生成一个指定长度的token
token = generate_token(32)  # 指定长度为10
print(token)
