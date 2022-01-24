Name: Tony Froman
Hours to complete project: 5
Feedback:


External Sources (Attributions):
1. Guide to Regular Expressions: https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285
2. Regular Expression Examples: https://www.regular-expressions.info/examplesprogrammer.html
3. Floating Point RegEx: https://stackoverflow.com/questions/12643009/regular-expression-for-floating-point-numbers
4. Ignoring Warnings: https://stackoverflow.com/questions/879173/how-to-ignore-deprecation-warnings-in-python
5. Negative Lookahead RegEx: https://stackoverflow.com/questions/2706745/how-to-match-the-character-not-followed-by-a-or-em-or-strong
6. Dr. Josh Nahum


AST = MainProgram([
    CodeBlock([
        PrintNode([RandomValue]),
        CodeBlock([
            ConditionalNode([
                TroofLiteral(1),
                CodeBlock([
                    CodeBlock([
                        FuncDef(['numbr_function', [DeclNode(arg, NUMBR), DeclNode(arg2, LETTR)],
                            CodeBlock([PrintNode([UseVar(arg2)]),
                                ReturnNode([
                                    BinaryOpNode(['SUM', NumbrLiteral(8), UseVar(arg)])
                                ])
                            ]), 'NUMBR'
                        ])
                    ]),
                    InitNode([
                        DeclNode(x, NUMBR),
                        AssignNode(None, FuncCall(['numbr_function', [NumbrLiteral(4), InputNode]]))
                    ]),
                    PrintNode([UseVar(x)])
                ]),
                []
            ])
        ]),
        PrintNode([RandomValue])
    ])
])
