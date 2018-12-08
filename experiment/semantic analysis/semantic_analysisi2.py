import sys
import os

sys.path.append(os.path.abspath(r'../lexical analysis'))

from lexical_analysis import get_token


def subroutine_s():
    """开始符号"""
    global state, pos
    subroutine_e()
    if token[pos][0] == '#' and state == 1:
        print('RIGHT')
    else:
        print(pos)
        print(state)
        print('WRONG')


def subroutine_f():
    """F->I|(E)"""
    global state, pos, sem
    if token[pos][0] == '(':
        pos += 1
        subroutine_e()
        if not token[pos][0] == ')':
            state = 0
        pos += 1
    else:
        if not (token[pos][1] == 'i标识符' or token[pos][1] == 'c常数'):
            state = 0
            return
        sem.append(token[pos][0])
        pos += 1


def subroutine_t1():
    """T1->*FT1|/FT1|空"""
    global state, pos, sem, temporary_num
    if not (token[pos][0] == '*' or token[pos][0] == '/'):
        return
    else:
        tem_sign = token[pos][0]
    pos += 1
    subroutine_f()
    temporary_num += 1
    print('(', tem_sign, ',', sem.pop(), ',', sem.pop(), ',t', temporary_num, ')')
    sem.append('t' + str(temporary_num))
    subroutine_t1()


def subroutine_t():
    """T->FT1"""
    global state, pos
    subroutine_f()
    subroutine_t1()


def subroutine_e1():
    """E1->+TE1|-TE1|空"""
    global state, pos, temporary_num
    if not (token[pos][0] == '+' or token[pos][0] == '-'):
        return
    else:
        tem_sign = token[pos][0]
    pos += 1
    subroutine_t()
    temporary_num += 1
    print('(', tem_sign, ',', sem.pop(), ',', sem.pop(), ',t', temporary_num, ')')
    sem.append('t' + str(temporary_num))
    subroutine_e1()


def subroutine_e():
    """E->ET1"""
    global state, pos
    subroutine_t()
    subroutine_e1()


if __name__ == '__main__':
    token = get_token()
    token.append(('#', '结束标记', 0))
    # 位置记录 状态 临时变量命名 语义栈
    pos = 0
    state = 1
    temporary_num = -1
    sem = list()

    subroutine_s()
