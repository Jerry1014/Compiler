from lexical_analysis import get_token

symbol = ['+', '-', '*', '/', 'I', '(', ')', '#']
priority = [['>', '>', '<', '<', '<', '<', '>', '>'], ['>', '>', '<', '<', '<', '<', '>', '>'],
            ['>', '>', '>', '>', '<', '<', '>', '>'], ['>', '>', '>', '>', '<', '<', '>', '>'],
            ['>', '>', '>', '>', '.', '.', '>', '>'], ['<', '<', '<', '<', '<', '<', '=', '<'],
            ['>', '>', '>', '>', '.', '.', '>', '>'], ['<', '<', '<', '<', '<', '<', '.', '=']]
production = {'+': 'E', '-': 'E', '*': 'T', '/': 'T', 'I': 'F', '()': 'F'}
non_terminal = ['T', 'F', 'E']
left = list()

if __name__ == '__main__':
    token = get_token()
    token.insert(0, ('<',))
    token.append(('#',))

    pos = 2
    last_left = 0
    current_symbol = token[1][0]
    current_pos = 1
    while True:
        if current_pos >= len(token):
            print('WRONG')
            break

        try:
            if token[pos][1] == 'i标识符' or token[pos][1] == 'c常数':
                token[pos] = ('I')
        except:
            pass

        if token[pos][0] in non_terminal:
            pos += 1
            continue

        insert_symbol = priority[symbol.index(current_symbol)][symbol.index(token[pos][0])]
        if insert_symbol == '<':
            token.insert(current_pos + 1, ('<'))
            last_left = current_pos + 1
            current_pos = pos + 1
            current_symbol = token[current_pos][0]
            pos += 2

        elif insert_symbol == '>':
            handle = ''
            while last_left + 1 < pos:
                if token[last_left + 1][0] not in non_terminal:
                    handle += token[last_left + 1][0]
                del token[last_left + 1]
                pos -= 1
            print(handle)
            del token[last_left]
            current_symbol = token[last_left - 1][0]

            for key, value in production.items():
                if key == handle:
                    token.insert(last_left, value)
                    break
            current_pos = last_left - 1
            pos = last_left + 1

            last_left = -1
            for i in range(current_pos, -1, -1):
                if token[i][0] == '<':
                    last_left = i
                    break

            if last_left == -1 and token[pos][0] == '#':
                print("RIGHT")
                print(token)
                break

        elif insert_symbol == '=':
            current_pos = pos
            current_symbol = token[current_pos][0]
            pos += 1
        else:
            print('WRONG')
            break
