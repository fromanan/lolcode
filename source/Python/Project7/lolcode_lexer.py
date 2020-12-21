import re
from . rply import LexerGenerator

def build_lexer():
    lg = LexerGenerator()

    # Ignore Whitespace
    lg.ignore(r'[\t ]')

    # New Line
    lg.add('NEWLINE', r'\n')

    # Comments, Used for both: ".*?" from [ATTRIBUTION 2]
    lg.ignore(r'BTW.*?(?=\n)')  # Used (?=\n) to end with but ignore \n [ATTRIBUTION 1]
    lg.ignore(r'OBTW.*?TLDR', re.DOTALL)  # (?=\n)

    # Literals
    lg.add('LETTR_LITERAL', r"(':'')|('[^']')|(':\)')|(':>')|('::')")
    lg.add('NUMBAR_LITERAL', r'[+-]?([0-9]*)?[.][0-9]+')  # RegEx from [ATTRIBUTION 3]
    lg.add('NUMBR_LITERAL', r'[+-]?\d+')
    lg.add('YARN_LITERAL', r'\"[^\n]*\"')

    lg.add('PRIMITIVE_TYPE', r'NUMBR|NUMBAR|LETTR|TROOF')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]{11,}')

    lg.add('COMPARISON_BINARY_OPERATOR', r'FURSTSMALLR')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]{10}')

    lg.add('COMPARISON_BINARY_OPERATOR', r'FURSTBIGGR')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]{8,9}')

    lg.add('COMPARISON_BINARY_OPERATOR', r'DIFFRINT')
    lg.add('MATH_BINARY_OPERATOR', r'QUOSHUNT')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]{7}')

    lg.add('MATH_BINARY_OPERATOR', r'PRODUKT')
    lg.add('LENGTHZ', r'LENGTHZ')
    lg.add('KTHXBYE', r'KTHXBYE')
    lg.add('VISIBLE', r'VISIBLE')
    lg.add('WHATEVR', r'WHATEVR')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]{6}')

    lg.add('MATH_BINARY_OPERATOR', r'SMALLR')
    lg.add('LOGICAL_BINARY_OPERATOR', r'EITHER')
    lg.add('ASSIGNMENT_OPERATOR', r'NERFIN')
    lg.add('GIMMEH', r'GIMMEH')
    lg.add('OMGWTF', r'OMGWTF')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]{5}')

    lg.add('MATH_BINARY_OPERATOR', r'BIGGR')
    lg.add('MATH_UNARY_OPERATOR', r'SQUAR')
    lg.add('ASSIGNMENT_OPERATOR', r'UPPIN')
    lg.add('OUTTA', r'OUTTA')
    lg.add('FOUND', r'FOUND')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]{4}')

    lg.add('COMPARISON_BINARY_OPERATOR', r'SAEM')
    lg.add('MATH_BINARY_OPERATOR', r'DIFF')
    lg.add('MATH_UNARY_OPERATOR', r'FLIP')
    lg.add('LOGICAL_BINARY_OPERATOR', r'BOTH')
    lg.add('TROOF_LITERAL', r'FAIL')
    lg.add('YARN', r'YARN')
    lg.add('GTFO', r'GTFO')
    lg.add('MKAY', r'MKAY')
    lg.add('THAR', r'THAR')
    lg.add('LOTZ', r'LOTZ')
    lg.add('LOOP', r'LOOP')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]{3}')

    lg.add('MATH_BINARY_OPERATOR', r'SUM')
    lg.add('LOGICAL_UNARY_OPERATOR', r'NOT')
    lg.add('LOGICAL_VARIABLE_OPERATOR', r'ALL|ANY')
    lg.add('LOGICAL_BINARY_OPERATOR', r'WON')
    lg.add('TROOF_LITERAL', r'WIN')
    lg.add('WAI', r'WAI')
    lg.add('WTF', r'WTF')
    lg.add('OMG', r'OMG')
    lg.add('OIC', r'OIC')
    lg.add('RLY', r'RLY')
    lg.add('HAI', r'HAI')
    lg.add('ITZ', r'ITZ')
    lg.add('HAS', r'HAS')
    lg.add('HOW', r'HOW')
    lg.add('PUT', r'PUT')
    lg.add('NOW', r'NOW')
    lg.add('TIL', r'TIL')
    lg.add('SAY', r'SAY')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]{2}')

    lg.add('IM', r'IM')
    lg.add('IZ', r'IZ')
    lg.add('IF', r'IF')
    lg.add('YA', r'YA')
    lg.add('NO', r'NO')
    lg.add('OF', r'OF')
    lg.ignore(r'AN(?!Y)')  # Replaced: lg.add('AN', r'AN'), NEGATIVE LOOKAHEAD FROM [ATTRIBUTION 5]
    lg.add('BY', r'BY')
    lg.add("'Z", r"'Z")
    lg.add('IN', r'IN')
    lg.add('YR', r'YR')
    lg.add('SO', r'SO')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]+')

    lg.add('?', r'\?')
    lg.add('BANG', r'!')
    lg.add('I', r'I')
    lg.add('A', r'A')
    lg.add('R', r'R')
    lg.add('O', r'O')
    lg.add('S', r'S')
    lg.add('U', r'U')

    lg.add('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]*')

    # Errors
    lg.add('ERROR', r'.', re.DOTALL)

    lexer = lg.build()

    return lexer