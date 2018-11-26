# 导入语法分析
import sys

sys.path.append(r'C:\Users\Jerry\PycharmProjects\Compiler\syntax analysis')
from syntax_analysis3 import Automaton, get_token


class SemanticAutomaton(Automaton):
    def __init__(self, start_state, token):
        super().__init__(start_state, token)
        self._action_dict = {'=': '=','=3':'=', '+': '+', '-': '-', '*': '*', '/': '/'}
        self._temporary_num = 0
        self._semantic_sym = ''
        self._quaternion = list()

    def semantic_action_step1(self, action, op):
        """
        在token串改变前，保存即将用于语义动作的相关属性
        :param action: 动作指示
        :param op: 语义动作的对象
        :return: None
        """
        if action in self._action_dict.keys():
            if action == '=':
                self._semantic_sym = op[0][-1]
            elif action == '=3':
                self._semantic_sym = op[1][-1]
            else:
                self._semantic_sym = 't'+str(self._temporary_num)
                self._quaternion.append\
                    (self._action_dict[action]+','+op[0][-1]+','+op[-1][-1]+','+self._semantic_sym)
                self._temporary_num += 1

    def semantic_action_step2(self, op_pos):
        """
        用于生成语义动作
        :param op_pos: 要操作的对象
        :return: None
        """
        self._token[op_pos][-1] = self._semantic_sym

    def print(self):
        print(self._quaternion)


if __name__ == '__main__':
    my_token = get_token('{0} {1} {2}')

    sm = SemanticAutomaton('0', my_token)
    sm.start()
    sm.print()
