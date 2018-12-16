def get_first(a_non_terminal_char):
    pass


def get_am(left, right, pos, next, state):
    """
    按照产生式迭代产生状态转换图

    eg:  S -> *    E  , # 'sem_sign'
       left  pos right next
    需要有all_production外部变量，记录了全部的产生式
    am_file_name外部变量，用于保存状态转换表文件
    state_count外部变量，用于记录当前的状态序号
    初始传入开始符号的产生式，如S->E，#
    :param left:str 产生式左部
    :param right:list of str 产生式右部
    :param pos:int 产生式当前读取位置，从0开始
    :param next:list of str 产生式的follow集合
    :param state:int 当前子程序代表的状态
    :return:None
    """
    global state_count
    # 生成规约状态
    if pos >= len(right) - 1:
        next_str = ''
        for i in next:
            next_str += i + ','
        with open(am_file_name, 'a') as f:
            # 3 +,-,*,/,# G 1 T =
            f.writelines(
                str(state) + ' ' + next_str[:-1] + ' G ' + str(len(right) - 1) + ' ' + left + ' ' + right[-1] + '\n')

    else:
        # 生成移进状态
        # 当前读取字符和状态的映射，用于合并读取同一字符的不同状态  非终结符（key，str）及它的follow（value，list）
        cur_char_state = dict()
        non_terminal_next = dict()

        # 当前产生式继续往下读
        cur_char_state[right[pos]] = state_count

        with open(am_file_name, 'a') as f:
            # 2 * M 10
            f.writelines(str(state) + ' ' + right[pos] + ' M ' + str(state_count) + '\n')

        state_count += 1
        get_am(left, right, pos + 1, next, state_count - 1)

        # 规约当前产生式中的非终结符
        # 当前产生式读取的字符，用于判断是否继续加入产生式
        cur_read_char = list()

        # 如果当前产生式当前读取符号为非终结符
        if right[pos] in all_production.keys():
            cur_read_char.append(right[pos])
            if pos != len(right) - 2:
                if right[pos + 1] not in all_production.keys():
                    non_terminal_next[right[pos]] = [right[pos + 1]]
                else:
                    non_terminal_next[right[pos]] = get_first(right[pos + 1])
            else:
                non_terminal_next[right[pos]] = next

        # 添加所有的产生式
        while len(cur_read_char) != 0:
            # 添加该非终结符的所有产生式，并计算follow集，并加入可能的新的产生式
            handling_char = cur_read_char[0]
            for production in all_production[handling_char]:
                # 对cur_read_char第一个非终结符的产生式逐条进行处理，如果产生式第一个还是非终结符
                if production[0] in all_production.keys():
                    # 若此非终结符和要处理的非终结符相同，eg：E->E+F
                    if production[0] == handling_char:
                        if len(production) > 2:
                            tem_next = list()
                            if production[1] in all_production.keys():
                                tem_next = get_first(production[1])
                            else:
                                tem_next = [production[1]]
                            if handling_char in non_terminal_next.keys():
                                non_terminal_next[handling_char] += tem_next
                            else:
                                non_terminal_next[handling_char] = tem_next
                    else:
                        cur_read_char.append(production[0])
                        if len(production) > 2:
                            tem_next = list()
                            if production[1] in all_production.keys():
                                tem_next = get_first(production[1])
                            else:
                                tem_next = [production[1]]
                            if production[0] in non_terminal_next.keys():
                                non_terminal_next[production[0]] += tem_next
                            else:
                                non_terminal_next[production[0]] = tem_next
                        else:
                            non_terminal_next[production[0]] = non_terminal_next[handling_char]

            # 生成该非终结符的移进状态
            for production in all_production[handling_char]:
                if production[0] in cur_char_state.keys():
                    get_am(handling_char, production, 1, non_terminal_next[handling_char],
                           cur_char_state[handling_char])
                else:
                    with open(am_file_name, 'a') as f:
                        # 2 * M 10
                        f.writelines(str(state) + ' ' + production[0] + ' M ' + str(state_count) + '\n')

                    state_count += 1
                    get_am(handling_char, production, 1, non_terminal_next[handling_char], state_count - 1)
                    cur_char_state[production[0]] = state_count
            cur_read_char = cur_read_char[1:]


if __name__ == '__main__':
    # all_production dict key为str，产生式左部 value为list,产生式右部，list为产生式集，每一产生式为list of str，最后一个为语义代表符号
    all_production = {
        'S': [['E', '']],
        'E': [['E', '+', 'T', '+'], ['E', '-', 'T', '-'], ['T', '=']],
        'T': [['*', '=']]
    }
    am_file_name = 'tem.txt'
    # 当前可分配的状态
    state_count = 1
    with open(am_file_name, 'w'):
        pass

    get_am('S', all_production['S'][0], 0, ['#'], 0)
