# left right 空格分割 其中，原来的‘{’不变，{改为\{,[同
file_name = input('文件名，无需txt后缀')


def get_first(left, num):
    """
    对单个的产生式的处理
    :param left:str，产生式左部
    :param num:str，对应的那一条产生式（在all_productions[left]中的位置）
    :return: None

    """

    def get_first_once():
        """
        求first
        :return: None
        """
        cur_char = all_productions[left][num][pos]
        if cur_char in all_productions.keys():
            # 将新的命名序号压栈
            count.append(1)
            # 遍历当前非终结符的产生式
            if cur_char not in production_with_first.keys():
                production_with_first[cur_char] = dict()
                for num_of_cur_char_production in range(len(all_productions[cur_char])):
                    get_first(cur_char, num_of_cur_char_production)

            # 将当前非终结符的first添加进当前产生式的first集
            count.pop()
            if count[-1] not in production_with_first[left].keys():
                production_with_first[left][count[-1]] = set()
            for i in production_with_first[cur_char].values():
                production_with_first[left][count[-1]] |= i
        else:
            production_with_first[left][count[-1]] = set([cur_char])
        count[-1] += 1

    # 用于记录开始时，可能出现的{/[ 当前读取到的位置
    s = list()
    pos = 0

    # 产生式开始时，将在开头出现的{、[压栈
    while all_productions[left][num][pos] == '{' or all_productions[left][num][pos] == '[':
        s.append(all_productions[left][num][pos])
        pos += 1

    # 如果产生式第一位为非终结符，先求该非终结符的first，再计算当前的产生式的next
    get_first_once()
    # 对符号开头压栈的{、[弹栈
    while len(s) > 0:
        # 如果产生式第一位为非终结符，先求该非终结符的first，再计算当前的产生式的next
        if all_productions[left][num][pos] == ']' or all_productions[left][num][pos] == '}':
            pos += 1
            # 如果产生式第一位为非终结符，先求该非终结符的first，再计算当前的产生式的next
            get_first_once()
            s.pop()

        pos += 1


# 记录所有的产生式
all_productions = dict()
with open(file_name + '.txt') as f:
    for line in f.readlines():
        left, *right = line.split()

        if left not in all_productions.keys():
            all_productions[left] = []
        all_productions[left].append(right)

# 生成所有的first集
production_with_first = dict()
for key in all_productions.keys():
    if key not in production_with_first.keys():
        production_with_first[key] = dict()
        count = [1]
        for i in range(len(all_productions[key])):
            get_first(key, i)

with open('ll1LR1_expression.txt', 'w') as f:
    for left in production_with_first.keys():
        for num_production in production_with_first[left].keys():
            f.write(left + ' ')
            f.write(str(num_production) + ':')
            f.write(production_with_first[left][num_production].pop())
            for i in production_with_first[left][num_production]:
                f.write('`')
                f.write(i)
            f.write('\n')

print(production_with_first)
