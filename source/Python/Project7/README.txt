Name: Tony Froman
Hours to complete project: 20
Feedback:


External Sources (Attributions):
1. Guide to Regular Expressions: https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285
2. Regular Expression Examples: https://www.regular-expressions.info/examplesprogrammer.html
3. Floating Point RegEx: https://stackoverflow.com/questions/12643009/regular-expression-for-floating-point-numbers
4. Ignoring Warnings: https://stackoverflow.com/questions/879173/how-to-ignore-deprecation-warnings-in-python
5. Negative Lookahead RegEx: https://stackoverflow.com/questions/2706745/how-to-match-the-character-not-followed-by-a-or-em-or-strong
6. Professor Nahum's Code (it is basically Frankenstein at the moment)


AST = MainProgram([
    CodeBlock([
        PrintNode([RandomValue]),
        CodeBlock([
            FuncDef(['fib', [DeclNode(arg, NUMBR)],
                CodeBlock([
                    ConditionalNode([
                        BinaryOpNode(['FURSTBIGGR', NumbrLiteral(2), UseVar(arg)]),
                        CodeBlock([
                            ReturnNode([NumbrLiteral(1)])
                        ]),
                        CodeBlock([
                            ReturnNode([
                                BinaryOpNode(['SUM',
                                    FuncCall(['fib', [BinaryOpNode(['DIFF', UseVar(arg), NumbrLiteral(2)])]]),
                                    FuncCall(['fib', [BinaryOpNode(['DIFF', UseVar(arg), NumbrLiteral(1)])]])
                                ])
                            ])
                        ])
                    ])
                ]), 'NUMBR'
            ])
        ]),
        PrintNode([FuncCall(['fib', [NumbrLiteral(8)]])]),
        PrintNode([RandomValue])
    ])
])