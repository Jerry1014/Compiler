import sys

sys.path.append(r'C:\Users\Jerry\PycharmProjects\Compiler\lexical analysis')

from lexical_analysis import get_token


class State:
    def __init__(self, start_state, token):
        self._state = [start_state, ]
        self._token = token + [('#','')]
        self._token_pos = -1
        self._current_char = ''

        self.trans_dict = dict()
        self.get_trans_dict(self)

    def start(self):
        if len(self.trans_dict) > 0:
            while True:
                print(self._token)
                self.read_next_token(self._token)
                if self._state[-1] == 'OK':
                    print('Right')
                    break
                elif self._state[-1] == 'Wrong':
                    print('Wrong')
                    break

    def read_next_token(self, token):
        # 当前状态 当前符号 移进规约标志 下一状态 规约符号个数（若有） 规约产生式右部（若有）
        self._token_pos += 1
        if token[self._token_pos][1] == 'i标识符' or token[self._token_pos][1] == 'c常数':
            self._current_char = 'I'
        else:
            self._current_char = token[self._token_pos][0]

        sign = 0
        for tr in self.trans_dict[self._state[-1]]:
            if self._current_char in tr[0]:
                sign = 1

                if tr[1] == 'M':
                    self._state.append(tr[2][:-1])
                else:
                    self._token_pos -= int(tr[2])
                    token = self._token[:self._token_pos] + [(tr[3][:-1],'')]
                    token += self._token[self._token_pos+int(tr[2]):]
                    self._token = token
                    self._state = self._state[:-int(tr[2])]
                    self._token_pos -= 1

        if sign == 0:
            self._state = 'Wrong'

    @staticmethod
    def get_trans_dict(self):
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


if __name__ == '__main__':
    my_token = get_token()

    auto_ma = State('0', my_token)
    auto_ma.start()
