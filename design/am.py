from lexer import get_token, LexicalError


class Automaton:
    """
    语法制导自动机
    """

    def __init__(self, start_state, token_gen, quaternion_save_file='quaternion.txt'):
        """
        :param start_state: 开始状态，str
        :param token_gen: token生成器
        :param quaternion_save_file:四元式保存文件名
        """
        # 状态 token生成器 当前所有字符 从规约字符前读取字符
        self.state = [start_state, ]
        self.token_gen = token_gen
        self.token = list()  # list of list [char kind value] 当前符 类型 属性（产生式左部可能有）
        self.token_backward = 1

        # 属性文法映射 当前临时变量命名计数 规约的左部的属性 四元式
        self.action_dict = dict()
        self.temporary_num = 0
        self.semantic_sym = ''
        self.quaternion_save_file = quaternion_save_file

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
                if self.state[-1] == 'OK':
                    print('语法制导完成')
                    break

                # 取一个token
                try:
                    if self.token_backward > 1:
                        self.token_backward -= 1
                    else:
                        self.token.append(next(self.token_gen).split())
                except LexicalError as e:
                    print('发生词法错误！\n在第{}行，发生了"{}"错误'.format(e.line_num, e.msg))
                    break
                except StopIteration:
                    print('语法制导失败，token已读完')
                    print('当前状态栈',self.state)
                    print('\n请注意，是否没有诸如S->E,#的开始产生式')
                    print('以及，0 状态的规约成开始符号，需改为移进到OK状态\n')
                    break


                if len(self.token[-self.token_backward]) < 3:
                    # 用于配合产生式中I的定义
                    if self.token[-self.token_backward][1] == 'c':
                        self.token[-self.token_backward] = ['CO', self.token[-self.token_backward][1],
                                                            {'value': self.token[-self.token_backward][0]}]

                    if self.token[-self.token_backward][1] == 'i':
                        self.token[-self.token_backward] = ['ID', self.token[-self.token_backward][1],
                                                            {'value': self.token[-self.token_backward][0]}]

                sign = 0
                for tr in self.trans_dict[self.state[-1]]:
                    if self.token[-self.token_backward][0] in tr[0]:
                        # 存在对应当前状态和当前字符的转换
                        sign = 1
                        if tr[1] == 'M':
                            # 移进
                            self.state.append(tr[2])
                            break
                        else:
                            # 规约
                            # 语义动作执行前的准备 保存最后一个符号（next） 从token里删除要规约的部分 将规约成的左部加到token
                            # 执行语义动作 将next加回token集 状态栈弹栈 设置标记，使下一读取符号变为规约的左部，然后是next
                            self.semantic_action_step1(tr[4], self.token[-int(tr[2]) - 1:-1])
                            the_next = self.token.pop()
                            self.token = self.token[:-int(tr[2])]
                            self.token.append([tr[3], '', dict()])
                            self.semantic_action_step2()
                            self.token.append(the_next)
                            self.state = self.state[:-int(tr[2])]
                            self.token_backward = 3
                            break

                if sign == 0:
                    print(self.token)
                    print('发生语法错误，无对应的移进规约状态')
                    print('当前状态栈', self.state)
                    print('\n请注意，是否没有诸如S->E,#的开始产生式')
                    print('以及，0 状态的规约成开始符号，需改为移进到OK状态\n')
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
            state_char = dict()
            with open(trans_file + '.txt') as f:
                for line in f.readlines():
                    cur_sta, *trans = line.split()
                    trans[0] = trans[0].split(',')

                    if cur_sta not in state_char.keys():
                        state_char[cur_sta] = set(trans[0])
                    else:
                        if len(state_char[cur_sta] & set(trans[0])) == 0:
                            state_char[cur_sta] |= set(trans[0])
                        else:
                            print('状态转换表有冲突！')
                            print('冲突状态', cur_sta)
                            self.trans_dict = dict()
                            return
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
        self.semantic_sym = ''
        if action == '0':
            pass
        elif action == '=':
            # 简单将值向上传递,从value到value
            self.semantic_sym = op[0][-1]['value']
        elif action == '=3':
            # 形如(E)时，值的向上传递
            self.semantic_sym = op[1][-1]['value']
        elif action == '=I':
            # 将值赋予变量,输出四元式
            with open(self.quaternion_save_file, 'a') as f:
                f.write('=' + ',' + op[-2][-1]['value'] + ',' + '_' + ',' + op[0][-1]['value'])
                f.write('\n')
        elif action == 'IF':
            # 当碰到IF语句时，产生if的四元式
            with open(self.quaternion_save_file, 'a') as f:
                f.write('if' + ',_,_,_')
                f.write('\n')
        elif action == 'I_J':
            # 判断if的跳转
            with open(self.quaternion_save_file, 'a') as f:
                f.write('i_j' + ',' + op[1][-1]['value'] + ',_,_')
                f.write('\n')
        elif action == 'IEJ':
            # 跳转到else的情况
            with open(self.quaternion_save_file, 'a') as f:
                f.write('iej' + ',_,_,_')
                f.write('\n')
        elif action == 'IE':
            # if结束
            with open(self.quaternion_save_file, 'a') as f:
                f.write('ie' + ',_,_,_')
                f.write('\n')
        elif action == 'PE':
            # 程序段规约结束
            with open(self.quaternion_save_file, 'a') as f:
                f.write('pe' + ',_,_,' + op[0][-1]['value'])
                f.write('\n')
        elif action == 'PS':
            # 程序段入口
            self.semantic_sym = op[1][-1]['value']
            with open(self.quaternion_save_file, 'a') as f:
                f.write('ps' + ',_,_,' + op[1][-1]['value'])
                f.write('\n')
        elif action == 'WH':
            # while入口
            with open(self.quaternion_save_file, 'a') as f:
                f.write('wh' + ',_,_,_')
                f.write('\n')
        elif action == 'WJ':
            # while判断
            with open(self.quaternion_save_file, 'a') as f:
                f.write('wj' + ',' + op[1][-1]['value'] + ',_,_')
                f.write('\n')
        elif action == 'WE':
            # while结束
            with open(self.quaternion_save_file, 'a') as f:
                f.write('we' + ',_,_,_')
                f.write('\n')
        elif action == '+' or action == '-' or action == '*' or action == '/' or action == '<<' or action == '>>' or \
                action == '&' or action == '|' or action == '||' or action == '&&' or action == '!=' or action == '==' \
                or action == '<=' or action == '>=' or action == '<' or action == '>':
            # 目前只考虑+—*/的处理
            self.semantic_sym = 't' + str(self.temporary_num)
            with open(self.quaternion_save_file, 'a') as f:
                f.write(action + ',' + op[0][-1]['value'] + ',' + op[-1][-1]['value'] + ',' + self.semantic_sym)
                f.write('\n')
            self.temporary_num += 1

    def semantic_action_step2(self):
        """
        用于生成语义动作
        :return: None
        """
        if len(self.semantic_sym) > 0:
            self.token[-1][-1]['value'] = self.semantic_sym


if __name__ == '__main__':
    file_name = input('输入源程序文件名，无需txt后缀\n') + '.txt'
    my_token = get_token('{0} {1}', file_name)
    sm = Automaton('0', my_token)
    sm.start()
