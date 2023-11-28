# 十六进制字符串
hex_string = "0642FAF7516555E64F4631613B3D8D43"

# 将十六进制字符串转换为字节
bytes_object = bytes.fromhex(hex_string)

# 尝试将字节对象解码为ASCII字符
try:
    ascii_string = bytes_object.decode('ascii')
    print(ascii_string)
except UnicodeDecodeError:
    print("无法解码为ASCII字符。数据可能不是文本数据，或者使用了非ASCII编码。")
