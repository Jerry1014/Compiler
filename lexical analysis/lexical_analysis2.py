# -*- coding: utf-8 -*-
class LexicalError(Exception):
    def __init__(self, line_num, msg):
        self.line_num = line_num
        self.msg = msg


def get_token(this_format):
    file_name = input("默认为txt文件，不需要后缀名，非工作目录需带路径\n")

    token = list()
    # 类型
    identifier = list()
    char = list()
    string = list()
    constant = list()
    key_word = ['int', 'main', 'void', 'if', 'else', 'char']
    delimiter = ['<=', '==', '=', '<', '>', '+', '-', '*', '/', '{', '}', ',', ';', '(', ')', '[', ']']

    def get_attribute(word_need_indentify):
        """传入一个单词，得到token的属性分类结果"""
        # 关键字
        if word_need_indentify in key_word:
            need_to_add = this_format.format(word_need_indentify, 'K关键字', key_word.index(word_need_indentify))

        # 字符
        elif word_need_indentify[0] == "'":
            if word_need_indentify[-1] == "'":
                if word_need_indentify not in char:
                    char.append(word_need_indentify)
                need_to_add = this_format.format(word_need_indentify, 'C字符', char.index(word_need_indentify))
            else:
                raise LexicalError(line_num, '词法错误，未找到\'')

        # 字符串
        elif word_need_indentify[0] == '"':
            if word_need_indentify[-1] == '"':
                if word_need_indentify not in string:
                    string.append(word_need_indentify)
                need_to_add = this_format.format(word_need_indentify, 'S字符串', string.index(word_need_indentify))
            else:
                raise LexicalError(line_num, '词法错误，未找到\"')

        # 常数
        elif word_need_indentify[0].isdigit():
            sign = 1
            for i in word_need_indentify[1:]:
                if not (i.isdigit() or i == '.' or i == 'e'):
                    sign = 0
                    break
            if sign == 1:
                if word_need_indentify not in constant:
                    constant.append(word_need_indentify)
                need_to_add = this_format.format(word_need_indentify, 'c常数', constant.index(word_need_indentify))
            else:
                raise LexicalError(line_num, '常数词法错误')

        # 标识符
        elif word_need_indentify[0].isalpha() or word_need_indentify[0] == '_':
            sign = 1  # 0.出错 1.正确
            for i in word_need_indentify[1:]:
                if not (i.isalpha() or i.isdigit() or i == '_'):
                    sign = 0
                    break
            if sign == 1:
                if word_need_indentify not in identifier:
                    identifier.append(word_need_indentify)
                need_to_add = this_format.format \
                    (word_need_indentify, 'i标识符', identifier.index(word_need_indentify))
            else:
                raise LexicalError(line_num, '标志符词法错误')

        else:
            raise LexicalError(line_num, '无法识别')
        token.append(need_to_add)

    try:
        with open(file_name + '.txt') as f:
            # 按行分割
            line_num = 1
            for line in f.readlines():
                words = line.split(' ')
                # 按空格分割
                for word in words:
                    # 多个空格会产生''的处理
                    if word == '':
                        continue

                    # 关键字
                    if word in key_word:
                        token.append(this_format.format(word, 'K关键字', key_word.index(word)))

                    else:
                        last_pos = -1
                        long_delimiter = 0
                        for i in range(len(word)):
                            if long_delimiter == 1:
                                long_delimiter = 0
                                continue

                            if word[i] in delimiter:
                                if i - last_pos > 1:
                                    get_attribute(word[last_pos + 1:i])
                                if word[i:i + 2] in delimiter:
                                    need_to_add = this_format.format\
                                        (word[i:i + 2], 'P界符', delimiter.index(word[i:i + 2]))
                                    long_delimiter = 1
                                    last_pos = i + 1
                                else:
                                    need_to_add = this_format.format(word[i], 'P界符', delimiter.index(word[i]))
                                    last_pos = i
                                token.append(need_to_add)
                            elif word[i] == '\n':
                                break
            line_num += 1

        print(token)
    except FileNotFoundError:
        print("无此文件")

    return token


if __name__ == '__main__':
    my_format = '{1} {0} {2}'
    get_token(my_format)
