from .lolcode_parser import build_parser, parse_LOLcode
from .symbol_table import SymbolTable
from .interpreter import interpret
from .roflcode_generator import generate_ROFLcode_from_LMAOcode

from pprint import pprint


def generate_LMAOcode_from_LOLcode(lolcode_str):
    ast = parse_LOLcode(lolcode_str)

    compiled_output = []
    symbol_table = SymbolTable()
    print(f"\nAST = {ast}")

    print(f"\nCOMPILER OUTPUT")
    ast.compile(compiled_output, symbol_table)

    #print(f"\nST = {symbol_table}")

    #print(f"\nCompiled Output = {compiled_output}")
    lmao_code = "\n".join(compiled_output) + "\n"
    print(lmao_code)

    standard_input = "aabb \n\t .,'! fasdf"
    output = interpret(lmao_code, language="LMAOcode", seed=0, standard_input=standard_input, debug_mode=True)
    #print(f"\nOutput = {output}")
    return lmao_code


def generate_ROFLcode_from_LOLcode(lolcode_str):
    lmao_code = generate_LMAOcode_from_LOLcode(lolcode_str)
    return generate_ROFLcode_from_LMAOcode(lmao_code)


if __name__ == "__main__":
    lmaocode = generate_LMAOcode_from_LOLcode(r"""
HAI 1.450
VISIBLE WHATEVR
HOW IZ I fib YR arg ITZ A NUMBR  MKAY
    O RLY? FURSTBIGGR 2 AN arg
    YA RLY
        FOUND YR 1	
    NO WAI
        I HAS A sub_a ITZ A NUMBR AN ITZ DIFF OF arg AN 2
        I HAS A sub_b ITZ A NUMBR AN ITZ DIFF OF arg AN 1

        I HAS A fib_a ITZ A NUMBR AN ITZ I IZ fib YR sub_a MKAY
        I HAS A fib_b ITZ A NUMBR AN ITZ I IZ fib YR sub_b MKAY

        FOUND YR SUM OF fib_a AN fib_b
    OIC
IF U SAY SO ITZ A NUMBR 
VISIBLE I IZ fib YR 4 MKAY
VISIBLE WHATEVR
KTHXBYE
""")

    SEED = 0
    STANDARD_INPUT = "adf asgkgkjhgyfa  dasfasdfasdffdaaaaa fdsafdasfadfafdaaaafdsadfasdfaaafdasfdafaafdaaafadfsafsfaaaaa"

    output = interpret(input_=lmaocode, language='LMAOcode', debug_mode=True, standard_input=STANDARD_INPUT, seed=SEED)

    # roflcode = generate_ROFLcode_from_LMAOcode(lmaocode)
    # output = interpret(input_=roflcode, language='ROFLcode', debug_mode=True, standard_input="abdc", seed=0)

    print(output)
