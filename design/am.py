from lexer import get_token, LexicalError


class Automaton:
    """
    语法制导自动机
    """

    def __init__(self, start_state, token_gen):
        """
        :param start_state: 开始状态，str
        :param token_gen: token生成器
        """
        # 状态 token生成器 当前所有字符 从规约字符前读取字符
        self.state = [start_state, ]
        self.token_gen = token_gen
        self.token = list()
        self.token_backward = 0

        # 状态转换表
        self.trans_dict = dict()
        self.get_trans_dict()

    def start(self):
        """
        用于启动自动机进行分析，最后的结果为RIGHT（符合语法）/WRONG（不符）
        并在此过程中执行相应的语义动作
        :return: None
        """
        # 状态转换表不为空
        if len(self.trans_dict) > 0:
            while True:
                # 取一个token
                try:
                    if self.token_backward > 1:
                        self.token_backward -= 1
                    else:
                        self.token.append(next(self.token_gen))
                except LexicalError as e:
                    print('发生词法错误！\n在第{}行，发生了"{}"错误'.format(e.line_num, e.msg))
                    break
                except StopIteration:
                    print('语法制导完成')
                    break

                # 用于配合产生式中I的定义
                if self.token[-self.token_backward][-1] == 'i' or self.token[-self.token_backward][-1] == 'c':
                    current_char = 'I'
                else:
                    current_char = self.token[-self.token_backward][:-2]

                sign = 0
                for tr in self.trans_dict[self.state[-1]]:
                    if current_char in tr[0]:
                        # 存在对应当前状态和当前字符的转换
                        sign = 1
                        if tr[1] == 'M':
                            # 移进
                            self.state.append(tr[2])
                        else:
                            # 规约
                            self.semantic_action_step1(tr[4], self.token[-int(tr[2]):])
                            the_next = self.token.pop()
                            self.token = self.token[:-int(tr[2])]
                            self.token.append(tr[3])
                            self.token.append(the_next)
                            self.state = self.state[:-int(tr[2])]
                            self.semantic_action_step2()
                            self.token_backward = 3

                if sign == 0:
                    print(self.token)
                    print('发生语法错误')
                    break
        else:
            print('状态转换表为空！')

    def get_trans_dict(self):
        """
        载入状态转换文件
        文件格式（空格分隔）：当前状态 当前符号（可有多个，逗号分隔eg:+，-) 移进规约标志 下一状态 规约符号个数（若有） 规约产生式右部（若有）
        :return: None
        """
        try:
            trans_file = input('输入状态转移文件，不需要后缀名，默认txt\n')
            with open(trans_file + '.txt') as f:
                for line in f.readlines():
                    cur_sta, *trans = line.split()
                    trans[0] = trans[0].split(',')
                    if cur_sta not in self.trans_dict.keys():
                        self.trans_dict[cur_sta] = [trans, ]
                    else:
                        self.trans_dict[cur_sta].append(trans)

        except FileNotFoundError:
            print('文件不存在')

    def semantic_action_step1(self, action, op):
        """
        在token串改变前，保存即将用于语义动作的相关属性
        :param action: 动作指示
        :param op: 语义动作的对象
        :return: None
        """
        pass

    def semantic_action_step2(self):
        """
        用于生成语义动作
        :param op_pos: 要操作的对象
        :return: None
        """
        pass


if __name__ == '__main__':
    my_token = get_token('{0} {1}', 'ex_e.txt')
    sm = Automaton('0', my_token)
    sm.start()
