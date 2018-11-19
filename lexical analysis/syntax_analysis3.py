from lexical_analysis import get_token


class State:
    def __init__(self, start_state, token):
        self._state = start_state
        self._token = token
        self._token_pos = -1
        self._current_char = ''
        self._next_char = ''

        self.trans_dict = dict()
        self.get_trans_dict()

    def start(self):
        if len(self.trans_dict) > 0:
            while True:
                self.read_next_token(self._token)
                if self._state == 'OK':
                    print('Right')
                elif self._next_char == '#' or self._state == 'Wrong':
                    print('Wrong')
                    break

    def read_next_token(self, token):
        self._token_pos += 1
        self._current_char = token[self._token_pos][0]
        self._next_char = token[self._token_pos + 1][0]

        sign = 0
        for tr in self.trans_dict[self._state]:
            if self._current_char == tr[0]:
                if self._next_char == tr[1]:
                    sign = 1
                    self._state = tr[2]

                    if tr[3] != 'M':
                        self._token = self._token[:-(int(tr[4]))]
                        self._token.append(tr[5])
        if sign == 0:
            self._state = 'Wrong'

    @staticmethod
    def get_trans_dict(self):
        try:
            trans_file = input('输入状态转移文件')
            trans_dict = dict()
            with open(trans_file) as f:
                for line in f.readlines():
                    cur_sta, *trans = line.split(',')
                    if cur_sta not in trans_dict.keys():
                        trans_dict[cur_sta] = [trans, ]
                    else:
                        trans_dict[cur_sta].append(trans)
        except FileNotFoundError:
            print('文件不存在')


if __name__ == '__main__':
    my_token = get_token()

    auto_ma = State('E', my_token)
