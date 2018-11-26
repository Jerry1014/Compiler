import sys
sys.path.append(r'C:\Users\Jerry\PycharmProjects\Compiler\lexical analysis')

from lexical_analysis import get_token


def subroutine_s():
    global state, pos
    subroutine_e()
    if token[pos][0] == '#' and state == 1:
        print('RIGHT')
    else:
        print(pos)
        print(state)
        print('WRONG')


def subroutine_f():
    global state, pos
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
        pos += 1


def subroutine_t1():
    global state, pos
    if not (token[pos][0] == '*' or token[pos][0] == '/'):
        return
    pos += 1
    subroutine_f()
    subroutine_t1()


def subroutine_t():
    global state, pos
    subroutine_f()
    subroutine_t1()


def subroutine_e1():
    global state, pos
    if not (token[pos][0] == '+' or token[pos][0] == '-'):
        return
    pos += 1
    subroutine_t()
    subroutine_e1()


def subroutine_e():
    global state, pos
    subroutine_t()
    subroutine_e1()


if __name__ == '__main__':
    token = get_token()
    token.append(('#', '结束标记', 0))
    pos = 0
    state = 1

    subroutine_s()
