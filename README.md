# Compiler
编译原理实验与课设

design 课程设计
---
- lexer 词法分析器
    - 用于获取token
    - 设置好文件名字后，返回迭代器，每次调用next来获取下一个token，以this_format指定的形式返回

- gammar_to_ll1 文法->LL(1)分析
    - 将文法按要求以文件输入后，得到每个产生式的first，用于以后的LL（1）分析表的构造
    - 不支持文法检测，不支持空产生式

- gammar_to_lr1 文法->LR(1)分析
    - 将文法按要求以文件输入后，得到状态转换表，用于以后的LR（1）分析表的构造
    - 不支持空产生式
    - 输入输出格式
-     文法文件
      Left Right1 Right2 ... SEM （以空格分割）
      Left：产生式左部 Right*：产生式的一个右部 SEM：语义动作
      eg：E E + T +（空格分割），代表E->E+T 语义动作代表符号为+
      * 第一个左部将被视为开始符号
      * 语义动作代表符号'0'被视为''，既，无动作
-     输出状态转换文件 
      - 移进状态 State Char 'M' Next_state（空格分割）
        State：当前状态 Char：当前读取符号 'M'：字符，代表移进 Next_state：下一状态
        eg：0 E M 1，代表0状态读取符号’E'后，移进到1状态
      - 规约状态 State Char0，Char1...（逗号分割） 'G' Num Left SEM（空格分割）
        State:当前状态 Char*：Next符号集（逗号分割） 'G'：代表规约 Num：规约符号个数 Left：归约成的左部符号 SEM：语义动作 （空格分割）
        eg：3 -,+,# G 3 E +，代表3状态读到符号-/+/#时，将从当前往前的三个符号，规约城’E‘，并执行语义动作’+‘
        
- 杂项
    - ex_p 算术表达式的产生式
    - lr1_ex 使用gammar_to_lr1生成的算术表达式的lr1状态转换表

experiment 实验
---
- lexical analysis 词法分析
    - 1 返回token串（tuple）组成的列表
    - 2 返回token串（str，空格分割）组成的列表，可定义串内排列顺序
- syntax analysis 语法分析
    - 1 递归下降子程序
    - 2 简单符号优先
    - 3 LR（1）
- semantic analysis 语义分析
    - 1 LR（1）
    - 2 递归下降子程序