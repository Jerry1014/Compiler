# Compiler
编译原理实验与课设

design 课程设计
---
- lexer 词法分析器
    -       用于获取token
            设置好文件名字后，返回迭代器，每次调用next来获取下一个token，以this_format指定的形式返回


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