# all_production dict key为str，产生式左部 value为list,产生式右部，list为产生式集，每一产生式为list of str，最后一个为语义代表符号
all_production = dict()
am_file_name = ''
# 当前可分配的状态
state_count = 1


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
    with open(am_file_name, 'a') as f:
        # 生成规约状态
        if pos >= len(right) - 1:
            next_str = ''
            for i in next:
                next_str += i + ','
            # 3 +,-,*,/,# G 1 T =
            f.writelines(str(state) + ' ' + next_str[:-1] + ' G ' + str(len(right)) + ' ' + left + ' ' + right[-1])

        # 生成移进状态
        # 当前读取字符和状态的映射，用于合并读取同一字符的不同状态  非终结符（key，str）及它的follow（value，list）
        cur_char_state = dict()
        non_terminal_next = dict()

        # 当前产生式继续往下读
        cur_char_state[right[pos]] = state_count
        get_am(left, right, pos + 1, next, state_count)
        # 2 * M 10
        f.writelines(str(state) + ' ' + right[pos] + ' M ' + str(state_count))
        state_count += 1

        # 规约当前产生式中的非终结符
        # 当前产生式读取的字符，用于判断是否继续加入产生式
        cur_read_char = list()

        # 如果当前产生式当前读取符号为非终结符
        if right[pos] in all_production.keys():
            cur_read_char.append(right[pos])
            if pos != len(right)-2:
                non_terminal_next[right[pos]] = [right[pos+1]]
            else:
                non_terminal_next[right[pos]] = next

        # 添加所有的产生式
        while len(cur_read_char) != 0:
            # 添加该非终结符的所有产生式，并计算follow集，并加入可能的新的产生式
            for production in all_production[cur_read_char[0]]:
                if production[0] in all_production.keys():
                    if production[0] == cur_read_char[0]:
                        if cur_read_char[0] in non_terminal_next.keys():
                            if len(production) > 2:
                                non_terminal_next[cur_read_char[0]].append(production[1])
                            else:
                                non_terminal_next[cur_read_char[0]].append(non_terminal_next[cur_read_char[0]])
                        else:
                            if len(production) > 2:
                                non_terminal_next[cur_read_char[0]] = [production[1]]
                            else:
                                non_terminal_next[cur_read_char[0]] = non_terminal_next[cur_read_char[0]]
                    else:
                        cur_read_char.append(production[0])

            # 生成该非终结符的移进状态
            for production in all_production[cur_read_char[0]]:
                get_am(cur_read_char[0], production, 1, non_terminal_next[cur_read_char[0]], state_count)
                # 2 * M 10
                f.writelines(str(state) + ' ' + production[0] + ' M ' + str(state_count))
                state_count += 1
