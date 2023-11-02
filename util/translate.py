# 设置输入和输出文件路径
import random
import re
import string
import sys
import time
from string import punctuation

import translators as ts

input_file = r'cs50-1-Chinese.bak.srt'
output_file = r'cs50-1-Chinese.srt'


def format_file():
    # 打开输入文件和输出文件
    with open(input_file, 'r', encoding='utf-8') as input_srt, open(output_file, 'w', encoding='utf-8') as output_srt:
        # 初始化一个变量来存储当前字幕的内容
        translation_services = ['bing', 'alibaba', 'cloudTranslation', 'caiyun',
                                'youdao', 'baidu', 'deepl', 'sogou', 'tencent']
        lines = input_srt.readlines()  # 一次性读取所有行
        jump = False
        for i in range(len(lines)):
            current_line = lines[i].strip()
            pre_line = lines[i - 1].strip()
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
            if i + 1 < len(lines):
                if jump:
                    jump = False
                    continue
                b1 = pre_line == ''
                b2 = is_english(current_line) and not "-->" in current_line and not current_line == ''
                b3 = next_line == ''
                if b2 and b3:
                    # print("上一句：" + pre_line)
                    print("当前：" + current_line)
                    print("下一句：" + next_line)
                    output_srt.write(current_line + "\n")
                    translation = try_translate(current_line, translation_services)
                    output_srt.write(translation + "\n")
                    # jump = True
                else:
                    pass
                    output_srt.write(current_line + "\n")
                    # jump = False

    # 关闭文件
    input_srt.close()
    output_srt.close()


def contains_chinese(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False


def not_translate(pre_line, current_line, next_line, output):
    b1 = is_chinese(current_line)
    b2 = is_english(next_line)
    if b1 and b2:
        print("当前：" + current_line)
        print("下一句英文：" + next_line)
        output.write(next_line + "\n")
        output.write(current_line + "\n")
    else:
        output.write(current_line + "\n")


def replace_line(current_line, next_line, output):
    b1 = is_chinese(current_line)
    b2 = is_chinese(next_line)
    if b1 and b2:
        print("当前：" + current_line)
        print("下一句中文：" + next_line)
    else:
        output.write(current_line + "\n")


def add_feed(current_line, next_line, output):
    b1 = is_chinese(current_line)
    b2 = next_line.isdigit()
    if b1 and b2:
        print("当前中文：" + current_line)
        print("下一句数字：" + next_line)
        output.write(current_line + "\n")
        output.write("\n")
    else:
        output.write(current_line + "\n")


def trans(assert_line, line, next_line, output_srt, translation_services):
    # 调用 trans(assert_line, line, next_line, output_srt, translation_services) 函数来翻译字幕
    if ":" not in assert_line and not len(assert_line) < 5 and not assert_line.isdigit() or is_english(
            assert_line):
        if not is_chinese(next_line):
            print("这行需要翻译：" + assert_line)
            print("下一行：" + next_line)
            output_srt.write(line)
            translation = try_translate(line, translation_services)
            output_srt.write(translation + "\n")
            output_srt.write(next_line + "\n")
        else:
            output_srt.write(line)
            output_srt.write(next_line + "\n")
    else:
        output_srt.write(line)


# 判断字符是否为英语
def is_english(text):
    # 定义允许的英文字符和数字
    allowed_chars = string.ascii_letters + string.digits + string.punctuation + ' '  # 可能包含标点和空格

    # 检查文本中的每个字符是否都在允许的字符集中
    return all(char in allowed_chars for char in text)


# 判断字符是否为汉字
def is_chinese(word):
    # 使用zhon库来检查中文字符
    chinese_punctuation = set(punctuation)
    chinese_characters = set([char for char in word if char not in chinese_punctuation])
    return any(0x4e00 <= ord(char) <= 0x9fff for char in chinese_characters)


# 定义一个函数来尝试不同的翻译服务
def try_translate(english_text, translation_services):
    while True:
        for service in translation_services:
            try:
                translated_text = translate(english_text, service)
                return translated_text  # 如果成功翻译，返回结果
            except Exception as e:
                print(f"服务 {service} 失败辽，错误信息: {str(e)}")
                continue  # 如果出现异常，继续尝试下一个服务


def translate(english_text, translator):
    # result = ts.translate_text(english_text, translator='cloudTranslation', from_language='en', to_language='cn')
    result = ts.translate_text(english_text, translator=translator, from_language='en', to_language='cn')
    print(result)
    return result


if __name__ == '__main__':
    format_file()

    print("字幕合并完成。")
    sys.exit()
