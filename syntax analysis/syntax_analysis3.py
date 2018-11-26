# 导入词法分析
import sys

sys.path.append(r'C:\Users\Jerry\PycharmProjects\Compiler\lexical analysis')
from lexical_analysis import get_token


class Automaton:
    """
    自动机
    """

    def __init__(self, start_state, token):
        """
        :param start_state: 开始状态，str
        :param token: 要进行语法分析的token序列， [('A','类型','符号表索引'),]
        """
        # 状态 token串 当前读取位置 当前字符
        self._state = [start_state, ]
        self._token = token + [('#', '')]
        self._token_pos = -1
        self._current_char = ''

        # 状态转换表
        self.trans_dict = dict()
        self.get_trans_dict()

    def start(self):
        """
        用于启动自动机进行分析，最后的结果为RIGHT（符合语法）/WRONG（不符）
        :return: None
        """
        # 状态转换表不为空
        if len(self.trans_dict) > 0:
            while True:
                self.read_next_token()
                if self._state[-1] == 'OK':
                    print('Right')
                    break
                elif self._state[-1] == 'Wrong':
                    print('Wrong')
                    break

    def read_next_token(self):
        """
        在self._token读取下一符号，进行状态转换/规约
        :return: None
        """
        # 当前状态 当前符号 移进规约标志 下一状态 规约符号个数（若有） 规约产生式右部（若有）
        self._token_pos += 1
        try:
            # 用于配合产生式中I的定义
            if self._token[self._token_pos][1] == 'i标识符' or self._token[self._token_pos][1] == 'c常数':
                self._current_char = 'I'
            else:
                self._current_char = self._token[self._token_pos][0]

            sign = 0
            for tr in self.trans_dict[self._state[-1]]:
                if self._current_char in tr[0]:
                    # 存在对应当前状态和当前字符的转换
                    sign = 1

                    if tr[1] == 'M':
                        # 移进
                        self._state.append(tr[2][:-1])
                    else:
                        # 规约
                        self._token_pos -= int(tr[2])
                        token = self._token[:self._token_pos] + [(tr[3], '')]
                        token += self._token[self._token_pos + int(tr[2]):]

                        self.semantic_action_step1(tr[4][:-1], self._token[self._token_pos-int(tr[2]):self._token_pos+1])

                        self._token = token
                        self._state = self._state[:-int(tr[2])]

                        self.semantic_action_step1(self._token_pos)

                        self._token_pos -= 1
                        print(self._token)

            if sign == 0:
                self._state = ['Wrong']

        except Exception as e:
            print(e)
            self._state = ['Wrong']
            return

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
                    cur_sta, *trans = line.split(' ')
                    trans[0] = trans[0].split(',')
                    if cur_sta not in self.trans_dict.keys():
                        self.trans_dict[cur_sta] = [trans, ]
                    else:
                        self.trans_dict[cur_sta].append(trans)

        except FileNotFoundError:
            print('文件不存在')

    def semantic_action_step1(self, action, *op):
        """
        在token串改变前，保存即将用于语义动作的相关属性
        :param action: 动作指示
        :param op: 语义动作的对象
        :return: None
        """
        pass

    def semantic_action_step2(self, op_pos):
        """
        用于生成语义动作
        :param op_pos: 要操作的对象
        :return: None
        """
        pass


if __name__ == '__main__':
    my_token = get_token()

    auto_ma = Automaton('0', my_token)
    auto_ma.start()
