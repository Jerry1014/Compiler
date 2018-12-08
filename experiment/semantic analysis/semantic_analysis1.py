# 导入语法分析
import sys
import os

sys.path.append(os.path.abspath(r'../syntax analysis'))
from syntax_analysis3 import Automaton, get_token


class SemanticAutomaton(Automaton):
    def __init__(self, start_state, token):
        super().__init__(start_state, token)
        # 属性文法映射 当前临时变量命名计数 临时变量全名 四元式
        self.action_dict = {'=': '=', '=3': '=', '+': '+', '-': '-', '*': '*', '/': '/'}
        self.temporary_num = 0
        self.semantic_sym = ''
        self.quaternion = list()

    def semantic_action_step1(self, action, op):
        """
        在token串改变前，保存即将用于语义动作的相关属性
        :param action: 动作指示
        :param op: 语义动作的对象
        :return: None
        """
        if action in self.action_dict.keys():
            if action == '=':
                self.semantic_sym = op[0][-1]
            elif action == '=3':
                self.semantic_sym = op[1][-1]
            else:
                self.semantic_sym = 't' + str(self.temporary_num)
                self.quaternion.append \
                    (self.action_dict[action] + ',' + op[0][-1] + ',' + op[-1][-1] + ',' + self.semantic_sym)
                self.temporary_num += 1

    def semantic_action_step2(self, op_pos):
        """
        用于生成语义动作
        :param op_pos: 要操作的对象
        :return: None
        """
        self.token[op_pos][-1] = self.semantic_sym

    def print_quaternion(self):
        print(self.quaternion)


if __name__ == '__main__':
    my_token = get_token('{0} {1} {2}')

    sm = SemanticAutomaton('0', my_token)
    sm.start()
    sm.print_quaternion()
