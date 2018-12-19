# -*- coding: utf-8 -*-
class LexicalError(Exception):
    """
    词法错误
    """

    def __init__(self, line_num, msg):
        self.line_num = line_num
        self.msg = msg


class Uncertain(Exception):
    """
    出现无法识别的单词，可能是聚在一起的单词，如a=b+c
    """


def get_token(this_format, file_name):
    """
    用于获取token

    设置好文件名字后，返回迭代器，每次调用next来获取下一个token，以this_format指定的形式返回

    :param this_format: 定义token内部的排序,eg:'{1} {0}',token为（类型 单词）
    :param file_name: 源程序文件路径
    :return: str, 迭代器，一次返回一个token
    :raise: LexicalError 词法错误
    """
    key_word = ['void', 'int', 'short', 'long', 'float', 'double', 'auto', 'char', 'unsigned', 'signed', 'register',
                'volatile', 'static', 'struct', 'union', 'enum', 'typedef', 'const', 'extern', 'if', 'else',
                'switch', 'case', 'for', 'do', 'while', 'goto', 'continue', 'break', 'default', 'sizeof', 'return']
    delimiter = ['<=', '==', '=', '<', '>', '+', '-', '*', '/', '{', '}', ',', ';', '(', ')', '[', ']']

    def get_attribute(word_need_indentify):
        """
        传入一个单词，得到token的属性分类结果
        :raise: Uncertain 不确定的单词，可能是单词的组合，如a=b+c
        """
        # 关键字
        if word_need_indentify in key_word:
            token_in_ga = this_format.format(word_need_indentify, 'K')
        # 字符
        elif word_need_indentify[0] == "'":
            if word_need_indentify[-1] == "'" and word_need_indentify[-2] != "\\":
                token_in_ga = this_format.format(word_need_indentify, 'C')
            else:
                raise LexicalError(line_num, '词法错误，未找到\'')
        # 字符串
        elif word_need_indentify[0] == '"':
            if word_need_indentify[-1] == '"' and word_need_indentify[-2] != "\\":
                token_in_ga = this_format.format(word_need_indentify, 'S')
            else:
                raise LexicalError(line_num, '词法错误，未找到\"')
        # 常数
        elif word_need_indentify[0].isdigit() or (
                (word_need_indentify[0] == '+' or word_need_indentify[0] == '-') and len(word_need_indentify) > 1):
            try:
                float(word_need_indentify)
            except ValueError:
                raise LexicalError(line_num, '常数词法错误')
            token_in_ga = this_format.format(word_need_indentify, 'c')
        # 标识符
        elif word_need_indentify[0].isalpha() or word_need_indentify[0] == '_':
            for i in word_need_indentify[1:]:
                if not (i.isalpha() or i.isdigit() or i == '_'):
                    raise Uncertain
            token_in_ga = this_format.format(word_need_indentify, 'i')
        else:
            raise Uncertain
        return token_in_ga

    with open(file_name) as f:
        line_num = 1
        for line in f.readlines():
            # 按空格分割
            words = line.split()
            # 多个空格会产生''的处理
            for word in words:
                note = False
                if word == '':
                    continue

                try:
                    token = get_attribute(word)
                    yield token
                except Uncertain:
                    # 要分割的上一字符开始位置，长界符标记
                    last_pos = 0
                    long_delimiter = False
                    for i in range(len(word)):
                        # 长界符eg:==的跳过
                        if long_delimiter:
                            long_delimiter = False
                            continue

                        if word[i] in delimiter:
                            if i != last_pos:
                                try:
                                    token = get_attribute(word[last_pos:i])
                                    yield token
                                except Uncertain:
                                    raise LexicalError(line_num, '不可识别的token')
                            if word[i:i + 2] in delimiter:
                                token = this_format.format(word[i:i + 2], 'P')
                                long_delimiter = True
                                last_pos = i + 2
                            elif word[i:i + 2] == '//':
                                note = True
                                break
                            else:
                                token = this_format.format(word[i], 'P')
                                last_pos = i + 1
                            yield token

                        elif word[i] == '\n':
                            break
            if note:
                continue

            line_num += 1


if __name__ == '__main__':
    file_name = input('输入源程序文件名，不需要txt后缀\n') + '.txt'
    try:
        for i in get_token('{1} {0}', file_name):
            print(i)
    except LexicalError as e:
        print('发生错误！\n在第{}行，发生了"{}"错误'.format(e.line_num, e.msg))
