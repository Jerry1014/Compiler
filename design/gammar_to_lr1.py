# 当前可分配的状态
state_count = 1
# 记录已存在的状态，key:str 左部，value:list of list [[pro_num（产生式序号）,pos,next(set),state,[string,]],]
has_state = dict()
# 记录各个非终结符的first key:str 左部，value:set first集
left_first = dict()


def get_first(a_non_terminal_char, layer_count):
    """
    当出现两个非终结符相邻时，前一个非终结符求follow，即为后一个求first，此函数用于求非终结符的first
    :param a_non_terminal_char: str 非终结符
    :return: set first集
    """
    if layer_count > 500:
        print('在求first集时，遇到循环。当前要求first集的符号为', a_non_terminal_char)
        return set()
    if a_non_terminal_char not in left_first.keys():
        tem_first = set()
        for i in all_production[a_non_terminal_char]:
            if i[0] not in all_production.keys():
                tem_first.add(i[0])
            elif i[0] in left_first.keys():
                tem_first |= left_first[i[0]]
            elif i[0] != a_non_terminal_char:
                tem_first |= get_first(i[0], layer_count + 1)
        left_first[a_non_terminal_char] = tem_first
    return left_first[a_non_terminal_char]


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
    :param next:set of str 产生式的follow集合
    :param state:int 当前子程序代表的状态
    :return:None
    """
    global state_count, has_state, left_state, need_copy

    # 测试用断点
    if state % 10 == 0:
        print('当前状态',state)

    # 生成规约状态
    if pos == len(right) - 1:
        set_of_next = set(next)
        next_str = ''
        for i in set_of_next:
            next_str += i + ','
        with open(am_file_name, 'a') as f:
            # 3 +,-,*,/,# G 1 T =
            f.writelines(
                str(state) + ' ' + next_str[:-1] +
                ' G ' + str(len(right) - 1) + ' ' + left + ' ' + right[-1] + '\n')

    else:
        # 生成移进状态

        # 保存这个状态的子节点
        string_saver = set()
        # 记录has_state信息，在后续对重复状态的判断中，就是对产生式读取第一个字符后进行判断
        if left in has_state.keys():
            has_state[left].append([all_production[left].index(right), pos, next, state, string_saver])
        else:
            has_state[left] = [[all_production[left].index(right), pos, next, state, string_saver]]

        if right[pos] not in all_production.keys():
            with open(am_file_name, 'a') as f:
                f.writelines(str(state) + ' ' + right[pos] + ' M ' + str(state_count) + '\n')
                string_saver.add(right[pos] + ' M ' + str(state_count))
            state_count += 1
            get_am(left, right, pos + 1, next, state_count - 1)

        # 当前字符为非终结符
        else:
            # 记录展开后所有的产生式，key:str 下一个读取的字符 value:list of list 每一个list为一个产生式，[left，pro_num（产生式序号）,pos]
            production_this = {right[pos]: [[left, all_production[left].index(right), pos]]}
            # 非终结符（key，str）及它的follow（value，set）
            left_next = dict()
            # 当前产生式读取的字符，用于判断是否继续加入产生式
            cur_read_char = [right[pos]]

            # 添加当前这个非终结符的部分next
            if pos != len(right) - 2:
                if right[pos] not in left_next.keys():
                    left_next[right[pos]] = set()
                if right[pos + 1] not in all_production.keys():
                    left_next[right[pos]].add(right[pos + 1])
                else:
                    left_next[right[pos]] = left_next[right[pos]] | get_first(right[pos + 1], 0)
            else:
                left_next[right[pos]] = next

            # 添加所有的产生式和它们的next
            while len(cur_read_char) != 0:
                # 添加该非终结符的所有产生式，并计算follow集，并加入可能的新的产生式
                handling_char = cur_read_char[0]
                for index_of_production in range(len(all_production[handling_char])):
                    # 将产生式添加进项目集
                    production = all_production[handling_char][index_of_production]
                    if production[0] in production_this.keys():
                        if not (handling_char == left and index_of_production != all_production[left].index(
                                right) and pos != 0):
                            production_this[production[0]].append([handling_char, index_of_production, 0])
                    else:
                        production_this[production[0]] = [[handling_char, index_of_production, 0]]

                    # 如果产生式第一个还是非终结符
                    if production[0] in all_production.keys():
                        tem = set()
                        if production[1] in all_production.keys():
                            tem = get_first(production[1], 0)
                        elif len(production) > 2:
                            tem.add(production[1])
                        else:
                            tem |= left_next[handling_char]
                        if production[0] not in left_next.keys():
                            # cur_read_char写在这里，是为了避免循环，如，A->B,B->A，它们读取的位置都是第一位
                            cur_read_char.append(production[0])
                            left_next[production[0]] = tem
                        else:
                            left_next[production[0]] = left_next[production[0]] | tem

                cur_read_char = cur_read_char[1:]

            # 将当前left加在这的原因是，下一步对当前产生式的移进需要用到当前的left和对应的next，以及避免当前left无法加入prodution的情况
            # 如,F->(*E),E->*F,F->I
            if left not in left_next.keys():
                left_next[left] = next
            else:
                left_next[left] = left_next[left] | next
            # 递归产生式
            for cur in production_this.keys():
                # 先判断是否是存在相同的状态，因为list是有序的，比较第一个添加进去的产生式的左部就ok
                cmp_pro = production_this[cur][0]

                # 判断左部相等且不是已经移进过的
                continue_sign = False
                if cmp_pro[2] == 0:
                    if cmp_pro[0] in has_state.keys():
                        # 判断产生式 next相等
                        for i in has_state[cmp_pro[0]]:
                            if cmp_pro[1] == i[0]:
                                if left_next[cmp_pro[0]] == i[2]:
                                    if cmp_pro[2] == i[1] - 1:
                                        with open(am_file_name, 'a') as f:
                                            # 2 * M 10
                                            f.writelines(str(state) + ' ' + cur + ' M ' + str(i[3]) + '\n')
                                            string_saver.add(cur + ' M ' + str(i[3]))
                                        continue_sign = True
                                        break
                if continue_sign:
                    continue

                # 当前读取字符相同时，它们是同一状态
                same_state = state_count
                state_count += 1
                with open(am_file_name, 'a') as f:
                    # 2 * M 10
                    f.writelines(str(state) + ' ' + cur + ' M ' + str(same_state) + '\n')
                    string_saver.add(cur + ' M ' + str(same_state))

                for i in production_this[cur]:
                    # 每个小产生式读完当前字符后，判断是否为已存在的状态
                    continue_sign = False
                    # 跳过本状态的产生式，因为它已经在程序开头记录在has_state
                    if not (i[0] == left and all_production[i[0]][i[1]] == right and i[2] == pos):
                        if i[0] in has_state.keys():
                            # 判断产生式 next相等
                            for j in has_state[i[0]]:
                                if i[1] == j[0]:
                                    if left_next[i[0]] == j[2]:
                                        if i[2] + 1 == j[1]:
                                            for k in j[4]:
                                                with open(am_file_name, 'a') as f:
                                                    # 2 * M 10
                                                    f.writelines(str(same_state) + ' ' + k + '\n')
                                                continue_sign = True
                                                break
                    if continue_sign:
                        continue

                    get_am(i[0], all_production[i[0]][i[1]], i[2] + 1, left_next[i[0]], same_state)


if __name__ == '__main__':
    # all_production dict key为str，产生式左部 value为list,产生式右部，list为产生式集，每一产生式为list of str，最后一个为语义代表符号

    # # 这一段测试用
    # all_production = {
    #     'S': [['E', '0']],
    #     'E': [['E', '+', 'T', '0'], ['E', '-', 'T', '0'], ['T', '0']],
    #     'T': [['T', '*', 'F', '0'], ['T', '/', 'F', '0'], ['F', '0']],
    #     'F': [['I', '0'], ['(', 'E', ')', '0']],
    # }
    # am_file_name = 'tem.txt'
    # start_char = 'S'

    production_file_name = input('产生式文件名，无需txt后缀\n') + '.txt'
    am_file_name = input('状态转换表保存文件名，无需txt后缀\n') + '.txt'
    all_production = dict()

    with open(production_file_name) as f:
        line = f.readline().split()
        start_char = line[0]
        all_production[start_char] = [line[1:]]
        for line in f.readlines():
            line = line.split()
            if len(line) > 0:
                if line[0] in all_production.keys():
                    all_production[line[0]].append(line[1:])
                else:
                    all_production[line[0]] = [line[1:]]

    with open(am_file_name, 'w'):
        pass

    get_am(start_char, all_production[start_char][0], 0, {'#'}, 0)
