from . rply import ParserGenerator
from . lolcode_lexer import build_lexer
from . ast_nodes import *

class ParseError(Exception): pass
class LexError(Exception): pass


def build_parser(possible_tokens):
    # Initialize Parser Generator with Possible Tokens
    pg = ParserGenerator(possible_tokens)

    # BNF Production Rules Go Here
    @pg.production("program : opt_newlines header block footer opt_newlines")
    def program(p):
        return MainProgram(children=[p[2]], version=p[1])

    # region Formatting

    # Header
    @pg.production("header : HAI NUMBAR_LITERAL newlines")
    def header(p):
        return p[1]

    # Footer
    @pg.production("footer : KTHXBYE")
    def footer(p):
        pass

    # Newlines
    @pg.production('opt_newlines : newlines')
    @pg.production('opt_newlines : ')
    @pg.production('newlines : NEWLINE')
    @pg.production('newlines : NEWLINE newlines')
    def optional_newlines(p):
        pass

    # Identifiers
    @pg.production("identifier : IDENTIFIER")
    def identifier(p):
        return p[0].value

    # Code Block -> Statements
    @pg.production("block : statements")
    def block(p):
        return CodeBlock(children=p[0])

    # Statement Expansion
    @pg.production("statements : statement newlines statements")
    def state_exp(p):
        return [p[0]] + p[2]

    # Epsilon
    @pg.production("statements : ")
    def epsilon(p):
        return []

    # endregion

    # region Declaration / Assignment

    # Declaration (no init)
    @pg.production("statement : decl")
    def decl(p):
        return p[0]

    @pg.production("decl : I HAS A identifier ITZ A PRIMITIVE_TYPE")
    def var_dec(p):
        return DeclNode(identifier=p[3], var_type=p[6].value)

    @pg.production("decl : I HAS A identifier ITZ array_type array_size")
    def type_primitive(p):
        return ArrayDecl(identifier=p[3], var_type=p[5], size=p[6])

    @pg.production("array_type : A YARN")
    def type_yarn(p):
        return "LETTR"

    @pg.production("array_type : LOTZ A PRIMITIVE_TYPE S")
    def type_array(p):
        return p[2].value

    @pg.production("array_size : THAR IZ amount")
    def var_assign_array(p):
        return p[2]

    @pg.production("amount : IN identifier 'Z amount PUT amount")
    def array_index_placement(p):
        return AssignNode(identifier=IndexNode(identifier=p[1], index=p[3]), value=p[5])

    # Initialization
    @pg.production("statement : init")
    def initialization(p):
        return p[0]

    @pg.production("init : decl assign")
    def dec_init(p):
        return InitNode(decl=p[0], assign=p[1])

    @pg.production("assign : ITZ amount")
    def var_assign_expr(p):
        return AssignNode(value=p[1])

    # Assignment
    @pg.production("expr : assign")
    def assignment(p):
        return p[0]

    @pg.production("assign : identifier R amount")
    def assign_from_expr(p):
        return AssignNode(identifier=UseVar(p[0]), value=p[2])

    # endregion

    # region Printing
    @pg.production("statement : print")
    def expr_print(p):
        return p[0]

    @pg.production("print : VISIBLE multiple")
    def print_amount(p):
        return PrintNode(children=p[1])

    @pg.production("print : VISIBLE multiple BANG")
    def print_bang(p):
        return PrintNode(children=p[1], newline=False)

    # endregion

    # region Math Operations
    @pg.production("expr : operation")
    def operation(p):
        return p[0]

    @pg.production('optional_by_clause :')
    @pg.production('optional_by_clause : BY amount')
    def optional_by_clause(p):
        if p:
            return p[1]
        return None

    @pg.production("operation : assignment_operation")
    def operation_as(p):
        return p[0]

    @pg.production("assignment_operation : ASSIGNMENT_OPERATOR identifier optional_by_clause")
    def assignment_operation(p):
        operator = p[0].getstr()
        identifier = p[1]
        by_clause = p[2]

        delta = by_clause if by_clause else NumbrLiteral('1')
        math_operator = 'SUM' if operator == 'UPPIN' else 'DIFF'

        expression = BinaryOpNode(op=math_operator, lhs=UseVar(symbol=identifier), rhs=delta)
        return AssignNode(identifier=UseVar(symbol=identifier), value=expression)

    @pg.production("operation : MATH_BINARY_OPERATOR OF amount amount")
    def bi_op(p):
        return BinaryOpNode(op=p[0].value, lhs=p[2], rhs=p[3])

    @pg.production("operation : MATH_UNARY_OPERATOR OF amount")
    def un_op(p):
        return UnaryOpNode(op=p[0].value, val=p[2])

    @pg.production("operation : COMPARISON_BINARY_OPERATOR amount amount")
    def comp_bi(p):
        return BinaryOpNode(op=p[0].value, lhs=p[1], rhs=p[2])

    @pg.production("operation : LOGICAL_BINARY_OPERATOR OF amount amount")
    def log_bi(p):
        return LogicalBiOpNode(op=p[0].value, lhs=p[2], rhs=p[3])

    @pg.production("operation : LOGICAL_UNARY_OPERATOR amount")
    def log_un(p):
        return LogicalUnOpNode(op=p[0].value, value=p[1])

    @pg.production("operation : LOGICAL_VARIABLE_OPERATOR OF multiple MKAY")
    def log_var(p):
        return LogicalVarOpNode(op=p[0].value, value=p[2])

    @pg.production("multiple : amount multiple")
    def multiple(p):
        return [p[0]] + p[1]

    @pg.production("multiple : ")
    def multiples_eps(p):
        return []

    # endregion

    # region Amounts
    @pg.production("statement : amount")
    def state_amount(p):
        return p[0]

    @pg.production("amount : literal")
    def state_amount(p):
        return p[0]

    @pg.production("amount : identifier")
    def amount_id(p):
        return UseVar(symbol=p[0])

    @pg.production("amount : expr")
    def amount_expr(p):
        return p[0]

    # Literals
    @pg.production("literal : NUMBR_LITERAL")
    @pg.production("literal : TROOF_LITERAL")
    @pg.production("literal : LETTR_LITERAL")
    @pg.production("literal : YARN_LITERAL")
    def literal(p):
        token_type = p[0].gettokentype()
        if "NUMBR" in token_type:
            return NumbrLiteral(value=p[0].value)
        elif "TROOF" in token_type:
            return TroofLiteral(value=p[0].value)
        elif "LETTR" in token_type:
            return LettrLiteral(value=p[0].value)
        elif "YARN" in token_type:
            return YarnLiteral(value=p[0].value)

    # Arrays
    @pg.production("amount : identifier 'Z amount")
    def amount_index(p):
        return IndexNode(identifier=p[0], index=p[2])

    @pg.production("amount : LENGTHZ OF identifier")
    def amount_array_size(p):
        return ArrayLength(identifier=UseVar(symbol=p[2]))

    @pg.production("amount : LENGTHZ OF YARN_LITERAL")
    def amount_array_size(p):
        return ArrayLength(identifier=YarnLiteral(value=p[2].value))

    # Random Values
    @pg.production("amount : WHATEVR")
    def random(p):
        return RandomNode()

    # Input Values
    @pg.production("amount : GIMMEH")
    def get_input(p):
        return InputNode()

    # endregion

    # region Flow Control

    # While Loop
    @pg.production("statement : while")
    def while_loop(p):
        return p[0]

    @pg.production("while : IM IN YR LOOP opt_change opt_til newlines block NOW IM OUTTA YR LOOP")
    def while_body(p):
        return WhileNode(change=p[4], cond=p[5], body=p[7])

    @pg.production("opt_change : ")
    @pg.production("opt_change : assignment_operation")
    def while_til(p):
        if p:
            return p[0]
        return None

    @pg.production("opt_til : ")
    @pg.production("opt_til : TIL amount")
    def while_til(p):
        if p:
            return p[1]
        return None

    # Conditional Statement
    @pg.production("statement : conditional")
    def cond_statement(p):
        return p[0]

    @pg.production("conditional : O RLY ? amount opt_newlines conditionals OIC")
    def cond_body(p):
        return ConditionalNode(statement=p[3], if_child=p[5][0], else_child=p[5][1])

    # If/Else Statement
    @pg.production("conditionals : if else")
    def ifelse_statement(p):
        return p[0] + p[1]

    # If Statement
    @pg.production("if : YA RLY opt_newlines block")
    def if_body(p):
        return [p[3]]

    @pg.production("if : ")
    def if_empty(p):
        return [[]]

    # Else Statement
    @pg.production("else : NO WAI opt_newlines block")
    def else_body(p):
        return [p[3]]

    @pg.production("else : ")
    def else_empty(p):
        return [[]]

    # Switch Statement
    @pg.production("statement : switch")
    def switch_statement(p):
        return p[0]

    @pg.production("switch : WTF ? amount NEWLINE switch_cases OIC")
    def switch_body(p):
        return SwitchNode(switch=p[2], body=p[4])

    @pg.production("switch_cases : switch_case switch_cases")
    @pg.production("switch_cases : ")
    def switch_cases(p):
        if p:
            return [p[0]] + p[1]
        return []

    @pg.production("switch_case : OMG literal NEWLINE block")
    @pg.production("switch_case : OMGWTF NEWLINE block")
    def switch_case(p):
        if p[0].value == "OMG":
            return CaseNode(case=p[1], body=p[3])
        return CaseNode(body=p[2])

    # Break Statement
    @pg.production("statement : break")
    def break_statement(p):
        return p[0]

    # TODO: CHANGE Return
    @pg.production("break : GTFO")
    def break_body(p):
        return BreakNode()

    # endregion

    # region Function Definitions
    @pg.production("statement : function_def")
    def expr_fn(p):
        return p[0]

    @pg.production("function_def : func_header func_parameters MKAY NEWLINE func_body func_footer")
    def fn_def(p):
        return CodeBlock([FunctionDefinition(symbol=p[0], params=p[1], body=p[4], return_type=p[5])])

    @pg.production("func_header : HOW IZ I IDENTIFIER")
    def fn_header(p):
        return p[3].value

    @pg.production("func_body : opt_newlines block")
    def fn_body(p):
        return p[1]

    @pg.production("func_parameters : func_parameter func_parameters")
    @pg.production("func_parameters : ")
    def fn_parameters(p):
        if p:
            return [p[0]] + p[1]
        return []

    @pg.production("func_parameter : YR IDENTIFIER ITZ A PRIMITIVE_TYPE")
    def fn_parameter(p):
        return DeclNode(identifier=p[1].value, var_type=p[4].value)

    @pg.production("func_parameter : YR IDENTIFIER ITZ array_type")
    def fn_parameter_array(p):
        return ArrayDecl(identifier=p[1].value, var_type=p[3], size=NumbrLiteral(value=20))

    @pg.production("func_footer : IF U SAY SO ITZ A PRIMITIVE_TYPE")
    def fn_return_type(p):
        return p[6].value

    @pg.production("func_footer : IF U SAY SO ITZ array_type")
    def fn_return_type_array(p):
        return p[5] + 'S'

    @pg.production("statement : FOUND YR amount")
    def fn_return(p):
        return ReturnNode(value=p[2])

    @pg.production("amount : function_call")
    def fn_call(p):
        return p[0]

    @pg.production("function_call : I IZ IDENTIFIER func_arguments MKAY")
    def fn_call_(p):
        return FunctionCall(symbol=p[2].value, args=p[3])

    @pg.production("func_arguments : func_argument func_arguments")
    @pg.production("func_arguments : ")
    def fn_arguments(p):
        if p:
            return [p[0]] + p[1]
        return []

    @pg.production("func_argument : YR amount")
    def fn_argument(p):
        return p[1]

    # endregion

    # region Error Handling
    @pg.error
    def error_handler(token):
        raise ParseError(f"No production rule covers {token}")

    # endregion

    # Build Parser from Rules
    parser = pg.build()

    return parser


# Professor Nahum's Code
def check_for_lexing_errors(tokens):
    for token in tokens:
        if token.name == 'ERROR':
            raise LexError(f'Lexing error on token ({token.value}) at position {token.source_pos}.')


def parse_LOLcode(lolcode_str):
    lexer = build_lexer()

    token_list = list(lexer.lex(lolcode_str))
    #pprint(token_list)
    #pprint([(token, token.source_pos) for token in token_list])

    # CHECK FOR LEXING ERRORS
    check_for_lexing_errors(token_list)

    rules_to_ignore = {'ERROR'}
    possible_tokens = [rule.name for rule in lexer.rules if rule.name not in rules_to_ignore]
    # pprint(possible_tokens)

    parser = build_parser(possible_tokens)

    if parser.lr_table.sr_conflicts:
        raise ParseError(f'Shift-reduce conflicts {parser.lr_table.sr_conflicts}')
    if parser.lr_table.rr_conflicts:
        raise ParseError(f'Reduce-reduce conflicts {parser.lr_table.rr_conflicts}')

    ast = parser.parse(iter(token_list))
    # print(f"Ast: {ast}")

    return ast
