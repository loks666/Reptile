import re
from string import punctuation


def is_english(text):
    # 使用正则表达式匹配英文字母
    pattern = re.compile(r'[a-zA-Z]')
    return bool(pattern.search(text))


def is_chinese(word):
    # 使用zhon库来检查中文字符
    chinese_punctuation = set(punctuation)
    chinese_characters = set([char for char in word if char not in chinese_punctuation])
    return any(0x4e00 <= ord(char) <= 0x9fff for char in chinese_characters)


if __name__ == '__main__':
    result = is_chinese('这是CS50，哈佛大学的介绍')
    print(result)
