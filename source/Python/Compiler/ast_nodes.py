import abc
from enum import Enum
from random import randint

class InvalidOperationError(Exception): pass
class YarnParseError(Exception): pass
class InvalidTypeError(Exception): pass
class SwitchError(Exception): pass
class InvalidArguments(Exception): pass

from . symbol_table import InvalidCastError
from . symbol_table import InvalidComparisonError
from pprint import pprint

PrimitiveType = Enum('PrimitiveType', 'NUMBR LETTR TROOF')


class ASTNode(abc.ABC):
    def __init__(self, children=None):
        self.children = children if children else []

    @abc.abstractmethod
    def compile(self, compiled_output, symbol_table):
        for child in self.children:
            child.compile(compiled_output, symbol_table)


class CodeBlock(ASTNode):
    """
    Represents a block of statements.
    For instance, the main program or part of a
    flow control statement. Its children are a list
    of statements.
    """
    def __init__(self, children):
        super().__init__(children=children)

    def __repr__(self):
        return f"CodeBlock({self.children})"

    def compile(self, compiled_output, symbol_table):
        symbol_table.increment_scope()
        super().compile(compiled_output, symbol_table)
        symbol_table.decrement_scope()


class MainProgram(CodeBlock):
    """
    Represents the entire program, has a CodeBlock as
    its only child, and a version
    """
    def __init__(self, children, version):
        super().__init__(children=children)
        assert version.value == '1.450', version

    def __repr__(self):
        return f"MainProgram({self.children})"

    def compile(self, compiled_output, symbol_table):
        self.children[0].compile(compiled_output, symbol_table)


class Literal:
    def compile(self, compiled_output, symbol_table):
        s_value = symbol_table.assign_literal(var_type=self.var_type, value=self.value)
        compiled_output.append(f"VAL_COPY {self.value} {s_value}")
        return s_value


class NumbrLiteral(Literal):
    """
    An expression that represents a Numbr (like 5).
    The string of the value is stored as its only child.
    """
    def __init__(self, value):
        self.value = value
        self.var_type = "NUMBR"

    def __repr__(self):
        return f"NumbrLiteral({self.value})"


class TroofLiteral(Literal):
    """
    An expression that represents a Troof value (Win/Fail).
    The string of the value is stored as its only child.
    """
    def __init__(self, value):
        converted_value = "1" if value == "WIN" else "0" if value == "FAIL" else ""
        self.value = converted_value
        self.var_type = "TROOF"

    def __repr__(self):
        return f"TroofLiteral({self.value})"


class LettrLiteral(Literal):
    """
    An expression that represents a Lettr value (Char).
    The string of the value is stored as its only child.
    """
    def __init__(self, value):
        self.value = value
        self.var_type = "LETTR"

    def __repr__(self):
        return f"LettrLiteral({self.value})"

    def compile(self, compiled_output, symbol_table):
        lol_to_lmao = {
            "':)'": "'\n'",
            "':>'": "'\t'",
            "':\''": "'\\''",
            "'::'": "':'"
        }
        value = lol_to_lmao[self.value] if self.value in lol_to_lmao else self.value
        s_value = symbol_table.assign_literal(var_type=self.var_type, value=value)
        compiled_output.append(f"VAL_COPY {value} {s_value}")
        return s_value


class ArrayDecl:
    def __init__(self, identifier, var_type, size):
        self.children = [identifier, var_type, size]

    def __repr__(self):
        return f"ArrayDecl({self.children[0]}, {self.children[1]}S, {self.children[2]})"

    def compile(self, compiled_output, symbol_table):
        array = symbol_table.declare(identifier=self.children[0], var_type=f"{self.children[1]}S")
        size = self.children[2].compile(compiled_output, symbol_table)
        compiled_output.append(f"AR_SET_SIZE {array} {size}")
        return array


class IndexNode(ASTNode):
    def __init__(self, identifier, index):
        self.children = [UseVar(identifier), index]

    def __repr__(self):
        return f"IndexNode({self.children[0]}, {self.children[1]})"

    def compile(self, compiled_output, symbol_table):
        array = self.children[0].compile(compiled_output, symbol_table)
        index = self.children[1].compile(compiled_output, symbol_table)
        result = symbol_table.assign_literal(var_type=array.var_type[:-1])
        compiled_output.append(f"AR_GET_IDX {array} {index} {result}")
        result.array_entry = array
        result.index_entry = index
        return result


class ArrayLength(ASTNode):
    def __init__(self, identifier):
        self.children = [identifier]

    def __repr__(self):
        return f"ArrayLength({self.children[0]})"

    def compile(self, compiled_output, symbol_table):
        array = self.children[0].compile(compiled_output, symbol_table)
        result = symbol_table.assign_literal(var_type="NUMBR")
        compiled_output.append(f"AR_GET_SIZE {array} {result}")
        return result


class ArrayLiteral(Literal):
    def __init__(self, var_type=None, size=0):
        self.value = []
        self.var_type = f"{var_type}S"
        self.size = size

    def compile(self, compiled_output, symbol_table):

        size = symbol_table.assign_literal(var_type="NUMBR", value=self.size)
        array = symbol_table.get_entry(var_type=self.var_type, array=True)

        compiled_output.append(f"VAL_COPY {self.size} {size}")
        compiled_output.append(f"AR_SET_SIZE {array} {size}")

        for i in range(len(self.value)):
            char = self.value[i]
            result = char.compile(compiled_output, symbol_table)
            compiled_output.append(f"AR_SET_IDX {array} {i} {result}")

        return array


class YarnLiteral(ArrayLiteral):
    def __init__(self, value):
        # Get Content Between the Quotes
        string_contents = value[1:-1]
        values = []
        i = 0
        while i < len(string_contents):
            char = string_contents[i]
            if char == ":":
                if i + 1 < len(string_contents):
                    if string_contents[i+1] == "\"":
                        values.append(LettrLiteral(f"'{string_contents[i+1]}'"))
                    else:
                        values.append(LettrLiteral(f"'{char}{string_contents[i+1]}'"))
                    i += 2
                else:
                    raise YarnParseError(f"Unable to Parse Yarn, Unescaped ':' Character found")
            else:
                if char == "'":
                    values.append(LettrLiteral(f"'\\{char}'"))
                else:
                    values.append(LettrLiteral(f"'{char}'"))
                i += 1

        # Initialize as Array
        super().__init__(var_type="LETTR", size=len(values))

        self.value = values

    def __repr__(self):
        return f"YarnLiteral(\"{self.value}\")"


class InitNode:
    def __init__(self, decl, assign):
        self.children = [decl, assign]

    def __repr__(self):
        return f"InitNode({self.children})"

    def compile(self, compiled_output, symbol_table):
        for child in self.children:
            child.compile(compiled_output, symbol_table)


class DeclNode:
    def __init__(self, identifier, var_type):
        self.children = [identifier, var_type]

    def __repr__(self):
        return f"DeclNode({self.children[0]}, {self.children[1]})"

    def compile(self, compiled_output, symbol_table):
        loc = symbol_table.declare(identifier=self.children[0], var_type=self.children[1])
        return loc


class AssignNode:
    def __init__(self, identifier=None, value=None):
        self.children = [identifier, value]

    def __repr__(self):
        return f"AssignNode({self.children[0]}, {self.children[1]})"

    def compile(self, compiled_output, symbol_table):
        array_assign = False

        identifier = self.children[0]
        value = self.children[1].compile(compiled_output, symbol_table)
        var_type = symbol_table.get_type(value)
        if identifier is None:
            symbol = symbol_table.assign(var_type=var_type, value=value)
        else:
            symbol = identifier.compile(compiled_output, symbol_table)
            symbol_table.assign(symbol=symbol, var_type=var_type, value=value)

            if symbol.array_entry:
                array_assign = True

        # Add Output to Compiled_Output

        # Assignment of ArrayLiteral
        if value.is_array():
            compiled_output.extend(symbol_table.copy_array(src=value, dest=symbol))
            return symbol

        # Assignment Between Scalars
        elif not array_assign:
            compiled_output.append(f"VAL_COPY {value} {symbol}")
            return symbol

        # Assignment Of Array Indices
        else:
            array = symbol.array_entry
            index = symbol.index_entry
            compiled_output.append(f"AR_SET_IDX {array} {index} {value}")
            return value


# Returns the Variables Register
class UseVar:
    def __init__(self, symbol):
        self.children = [symbol]

    def __repr__(self):
        return f"UseVar({self.children[0]})"

    def compile(self, compiled_output, symbol_table):
        return symbol_table.get_var(self.children[0])


class PrintNode:
    def __init__(self, children, newline=True):
        self.children = children
        self.newline = newline

    def __repr__(self):
        return f"PrintNode({self.children})"

    def compile(self, compiled_output, symbol_table):
        for child in self.children:
            result_loc = child.compile(compiled_output, symbol_table)
            if result_loc.is_array():
                end = symbol_table.get_new_label("PRINT")
                start = symbol_table.get_new_label("PRINT", end=False)

                size = symbol_table.assign_literal(var_type="NUMBR")
                i = symbol_table.assign_literal(var_type="NUMBR")
                comp = symbol_table.assign_literal(var_type="NUMBR")

                if result_loc.compare_type("LETTR"):
                    value = symbol_table.assign_literal(var_type="LETTR")
                else:
                    value = symbol_table.assign_literal(var_type="NUMBR")

                compiled_output.append(f"AR_GET_SIZE {result_loc} {size}")
                compiled_output.append(f"VAL_COPY 0 {i}")

                compiled_output.append(f"{start}:")

                compiled_output.append(f"TEST_EQU {i} {size} {comp}")
                compiled_output.append(f"JUMP_IF_N0 {comp} {end}")
                compiled_output.append(f"AR_GET_IDX {result_loc} {i} {value}")

                if result_loc.compare_type("LETTR"):
                    compiled_output.append(f"OUT_CHAR {value}")
                else:
                    compiled_output.append(f"OUT_NUM {value}")

                compiled_output.append(f"ADD 1 {i} {i}")
                compiled_output.append(f"JUMP {start}")

                compiled_output.append(f"{end}:")

            elif result_loc.compare_type("LETTR"):
                compiled_output.append(f"OUT_CHAR {result_loc}")

            else:
                compiled_output.append(f"OUT_NUM {result_loc}")

        if self.newline:
            compiled_output.append(f"OUT_CHAR '\\n'")


class BinaryOpNode:
    def __init__(self, op, lhs, rhs):
        self.children = [op, lhs, rhs]

    def __repr__(self):
        return f"BinaryOpNode({self.children})"

    def compile(self, compiled_output, symbol_table):

        print(f"Performing Binary Operation: {self.children[0]}")

        symbol_to_command = {
            'SUM': 'ADD',
            'DIFF': 'SUB',
            'PRODUKT': 'MULT',
            'QUOSHUNT': 'DIV',
            'SAEM': 'TEST_EQU',
            'DIFFRINT': 'TEST_NEQU',
            'FURSTSMALLR': 'TEST_LESS',
            'FURSTBIGGR': 'TEST_GTR'
        }
        op_command = symbol_to_command[self.children[0]]

        lhs_compiled = self.children[1].compile(compiled_output, symbol_table)
        rhs_compiled = self.children[2].compile(compiled_output, symbol_table)

        if op_command in ['ADD', 'SUB', 'MULT', 'DIV']:
            symbol_table.compare_type(lhs_compiled, rhs_compiled)
            if symbol_table.get_type(lhs_compiled) == "LETTR" or symbol_table.get_type(rhs_compiled) == "LETTR":
                raise InvalidOperationError(f"Cannot Perform Math Operations on Type LETTR")
            s_value = symbol_table.assign_literal(var_type=symbol_table.get_type(lhs_compiled))

        elif not symbol_table.compare_type(lhs_compiled, rhs_compiled, error=False):
            s_value = symbol_table.assign_literal(var_type="TROOF")
            compiled_output.append(f"TEST_EQU 0 1 {s_value}")
            return s_value

        else:
            print(f"Compare: {op_command} {lhs_compiled} {rhs_compiled}")
            s_value = symbol_table.assign_literal(var_type="TROOF")

        result = f"{op_command} {lhs_compiled} {rhs_compiled} {s_value}"
        compiled_output.append(result)

        return s_value


class UnaryOpNode:
    def __init__(self, op, val):
        self.children = [op, val]

    def __repr__(self):
        return f"UnaryOpNode({self.children})"

    def compile(self, compiled_output, symbol_table):

        print(f"Unary Op: {self.children[0]}")

        symbol_to_command = {
            'FLIP': 'DIV',
            'SQUAR': 'MULT'
        }
        op_command = symbol_to_command[self.children[0]]

        val_compiled = self.children[1].compile(compiled_output, symbol_table)

        output_var = symbol_table.assign_literal(var_type="TROOF")

        if op_command == 'DIV':
            lhs, rhs = 1, val_compiled
        elif op_command == 'MULT':
            lhs, rhs = val_compiled, val_compiled

        result = f"{op_command} {lhs} {rhs} {output_var}"
        compiled_output.append(result)

        return output_var


class LogicalBiOpNode:
    def __init__(self, op, lhs, rhs, label=""):
        self.children = [op, lhs, rhs]

    def __repr__(self):
        return f"LogicalBiOpNode({self.children})"

    def compile(self, compiled_output, symbol_table):

        print(f"Logical Binary Op: {self.children[0]}")

        symbol_to_command = {
            'BOTH': 'MULT',
            'EITHER': 'ADD',
            'WON': 'XOR'
        }
        op_command = symbol_to_command[self.children[0]]

        if op_command == 'XOR':

            lhs = self.children[1]
            rhs = self.children[2]

            # Ensure Both Are Same Type
            symbol_table.compare_type(lhs, rhs)

            xor = LogicalBiOpNode('BOTH', 
                LogicalBiOpNode('EITHER', lhs, rhs), 
                LogicalUnOpNode('NOT', LogicalBiOpNode('BOTH', lhs, rhs))
            ).compile(compiled_output, symbol_table)

            return xor

        lhs_compiled = self.children[1].compile(compiled_output, symbol_table)

        # Short Circuiting!
        sc_var = symbol_table.assign_literal(var_type="TROOF")
        sc = f"MULT {lhs_compiled} 1 {sc_var}"
        compiled_output.append(sc)

        end_label = symbol_table.get_new_label(label_type="COMP")

        skip_label = symbol_table.get_new_label(label_type="COMP")

        comp_var = symbol_table.assign_literal(var_type="TROOF")
        output_var = symbol_table.assign_literal(var_type="TROOF")

        if self.children[0] == 'BOTH':
            compiled_output.append(f"JUMP_IF_N0 {sc_var} {skip_label}")
            compiled_output.append(f"VAL_COPY 0 {output_var}")

            compiled_output.append(f"JUMP_IF_0 {sc_var} {end_label}")

        else:
            compiled_output.append(f"JUMP_IF_0 {sc_var} {skip_label}")
            compiled_output.append(f"VAL_COPY 1 {output_var}")

            compiled_output.append(f"JUMP_IF_N0 {sc_var} {end_label}")

        compiled_output.append(f"{skip_label}:")

        rhs_compiled = self.children[2].compile(compiled_output, symbol_table)

        # Ensure Both Are Same Type
        symbol_table.compare_type(lhs_compiled, rhs_compiled)

        # Body
        comp = f"{op_command} {lhs_compiled} {rhs_compiled} {comp_var}"
        compiled_output.append(comp)

        result = f"TEST_GTR {comp_var} 0 {output_var}"
        compiled_output.append(result)

        # End Short Circuit
        compiled_output.append(f"{end_label}:")

        return output_var


class LogicalUnOpNode:
    def __init__(self, op, value):
        self.children = [op, value]

    def __repr__(self):
        return f"LogicalUnOpNode({self.children})"

    def compile(self, compiled_output, symbol_table):

        print(f"Logical Unary Op: {self.children[0]}")

        symbol_to_command = {
            'NOT': 'SUB'
        }
        op_command = symbol_to_command[self.children[0]]

        value_compiled = self.children[1].compile(compiled_output, symbol_table)

        comp_var = symbol_table.assign_literal(var_type="TROOF")
        comp = f"{op_command} 1 {value_compiled} {comp_var}"
        compiled_output.append(comp)

        output_var = symbol_table.assign_literal(var_type="TROOF")
        result = f"TEST_GTR {comp_var} {0} {output_var}"
        compiled_output.append(result)

        return output_var


class LogicalVarOpNode:
    def __init__(self, op, value):
        self.children = [op, value]

    def __repr__(self):
        return f"LogicalVarOpNode({self.children})"

    def compile(self, compiled_output, symbol_table):

        print(f"Variable Op: {self.children[0]}")

        end_label = symbol_table.get_new_label(label_type="COMP")

        operator = self.children[0]
        result_entry = symbol_table.assign_literal(var_type="TROOF")
        compiled_output.append(f"VAL_COPY 0 {result_entry}")

        # Short Circuit
        sc_var = symbol_table.assign_literal(var_type="TROOF")

        for expr in self.children[1]:
            entry = expr.compile(compiled_output, symbol_table)
            compiled_output.append(f"### CHECKING ENTRY {entry} ###")
            compiled_output.append(f"ADD {entry} {result_entry} {result_entry}")

            skip_label = symbol_table.get_new_label(label_type="COMP")

            if operator == 'ALL':
                print(f"Entry [{entry}]: {symbol_table.table[entry]}")
                compiled_output.append(f"MULT {entry} 1 {sc_var}")
                compiled_output.append(f"JUMP_IF_N0 {sc_var} {skip_label}")

                compiled_output.append(f"VAL_COPY 0 {result_entry}")
                compiled_output.append(f"JUMP_IF_0 {sc_var} {end_label}")

            else:  # operator == 'ANY'
                print(f"Entry [{entry}]: {symbol_table.table[entry]}")
                compiled_output.append(f"MULT {result_entry} 1 {sc_var}")
                compiled_output.append(f"JUMP_IF_0 {sc_var} {skip_label}")

                compiled_output.append(f"VAL_COPY 1 {result_entry}")
                compiled_output.append(f"JUMP_IF_N0 {sc_var} {end_label}")

            compiled_output.append(f"{skip_label}:")

        if operator == 'ALL':
            compiled_output.append(f"TEST_EQU {len(self.children[1])} {result_entry} {result_entry}")

        else:  # operator == 'ANY'
            compiled_output.append(f"TEST_GTE {result_entry} 1 {result_entry}")

        compiled_output.append(f"{end_label}:")

        return result_entry


class RandomNode:
    def __repr__(self):
        return f"RandomValue"

    def compile(self, compiled_output, symbol_table):
        s_value = symbol_table.assign_literal(var_type="NUMBR")

        result = f"RANDOM {s_value}"
        compiled_output.append(result)

        return s_value


class InputNode:
    def __repr__(self):
        return f"InputNode"

    def compile(self, compiled_output, symbol_table):
        s_value = symbol_table.assign_literal(var_type="LETTR")

        result = f"IN_CHAR {s_value}"
        compiled_output.append(result)

        return s_value


class ConditionalNode:
    def __init__(self, statement, if_child, else_child):
        self.children = [statement, if_child, else_child]

    def __repr__(self):
        return f"ConditionalNode({self.children})"

    def compile(self, compiled_output, symbol_table):
        result = self.children[0].compile(compiled_output, symbol_table)
        if symbol_table.get_type(result) != "TROOF":
            raise InvalidOperationError(f"Input of O RLY statement must be of type TROOF")
        end_label = symbol_table.get_new_label(label_type="IF")
        skip_label = symbol_table.get_new_label(label_type="IF")
        compiled_output.append(f"JUMP_IF_0 {result} {skip_label}")
        if self.children[1]:
            if_block = self.children[1].compile(compiled_output, symbol_table)
            compiled_output.append(f"JUMP_IF_N0 {result} {end_label}")
        compiled_output.append(f"{skip_label}:")
        if self.children[2]:
            else_block = self.children[2].compile(compiled_output, symbol_table)
        compiled_output.append(f"{end_label}:")


class WhileNode:
    def __init__(self, cond, body, change):
        self.children = [cond, body, change]

    def __repr__(self):
        return f"WhileNode({self.children}"

    def compile(self, compiled_output, symbol_table):
        end_label = symbol_table.get_new_label(label_type="WHILE")
        start_label = symbol_table.get_new_label(label_type="WHILE", end=False)

        compiled_output.append(f"{start_label}:")

        if self.children[0]:
            cond = self.children[0].compile(compiled_output, symbol_table)
            if cond.var_type != "TROOF":
                raise InvalidTypeError(f"Cannot Perform Troof Comparison on Type {cond.var_type}")
            comp = symbol_table.assign_literal(var_type="NUMBR")
            compiled_output.append(f"VAL_COPY {cond} {comp}")
            compiled_output.append(f"JUMP_IF_N0 {comp} {end_label}")

        body = self.children[1].compile(compiled_output, symbol_table)

        if self.children[2]:
            change = self.children[2].compile(compiled_output, symbol_table)

        compiled_output.append(f"JUMP {start_label}")

        compiled_output.append(f"{end_label}:")


class SwitchNode:
    def __init__(self, switch, body):
        self.children = [switch, body]

    def __repr__(self):
        return f"SwitchNode({self.children}"

    def compile(self, compiled_output, symbol_table):
        end_label = symbol_table.get_new_label(label_type="SWITCH")

        passover = symbol_table.assign_literal(var_type="TROOF")
        compiled_output.append(f"VAL_COPY 0 {passover}")

        default_cases = 0

        compiled_output.append(f"### BEGIN SWITCH STATEMENT ###")

        switch = self.children[0].compile(compiled_output, symbol_table)
        for case in self.children[1]:
            case.compile(compiled_output, symbol_table, switch, passover)
            if case.is_default():
                default_cases += 1

        if default_cases > 1:
            raise SwitchError(f"Too Many Default Cases, Only 1 Allowed")

        compiled_output.append(f"{end_label}:")
        symbol_table.break_switch()

        compiled_output.append(f"### END SWITCH STATEMENT ###")


class CaseNode:
    def __init__(self, case=None, body=[]):
        self.children = [case, body]

    def __repr__(self):
        return f"CaseNode({self.children}"

    def compile(self, compiled_output, symbol_table, switch, passover):
        compiled_output.append(f"### BEGIN {'DEFAULT ' if self.is_default() else ''}CASE ###")

        end_label = symbol_table.get_new_label(label_type="CASE")
        start_label = symbol_table.get_new_label(label_type="CASE", end=False)

        # Skip Header if this is a Case Fallthrough/Passover
        compiled_output.append(f"JUMP_IF_N0 {passover} {start_label}")

        # Non-default Case Header (check if case is a hit)
        if self.children[0] is not None:
            result = symbol_table.assign_literal(var_type="TROOF")
            case = self.children[0].compile(compiled_output, symbol_table)
            symbol_table.compare_type(case, switch)
            if not switch.is_array():
                compiled_output.append(f"TEST_EQU {switch} {case} {result}")
            else:
                compiled_output.extend(symbol_table.compare_arrays(switch, case, result))
            compiled_output.append(f"VAL_COPY {result} {passover}")     # Update if the case is a hit
            compiled_output.append(f"JUMP_IF_0 {result} {end_label}")

        compiled_output.append(f"{start_label}:")

        body = self.children[1].compile(compiled_output, symbol_table)

        compiled_output.append(f"{end_label}:")

        compiled_output.append(f"### END {'DEFAULT ' if self.is_default() else ''}CASE ###")

    def is_default(self):
        return self.children[0] is None


class BreakNode:
    def __repr__(self):
        return f"BreakNode"

    def compile(self, compiled_output, symbol_table):
        loop_tag = symbol_table.break_loop()
        compiled_output.append(f"JUMP end_{loop_tag}")


class FunctionDefinition:
    def __init__(self, symbol, params, body, return_type):
        self.children = [symbol, params, body, return_type]

    def __repr__(self):
        return f"FuncDef({self.children})"

    def compile(self, compiled_output, symbol_table):
        # Get all required locations for parameters
        param_locs = [param.compile(compiled_output, symbol_table) for param in self.children[1]]

        # Initialize Parameter Locations
        for param in param_locs:
            if param.is_array():
                compiled_output.append(f"AR_SET_SIZE {param} 1")
            else:
                compiled_output.append(f"VAL_COPY 0 {param}")

        # Define function in function table
        func_def = symbol_table.declare_function(symbol=self.children[0], param_locs=param_locs, rtn_type=self.children[3])

        # Initialize Return Location & Label
        if func_def.rtn_loc.is_array():
            compiled_output.append(f"AR_SET_SIZE {func_def.rtn_loc} 1")
        else:
            compiled_output.append(f"VAL_COPY 0 {func_def.rtn_loc}")
        compiled_output.append(f"VAL_COPY 0 {func_def.rtn_label}")

        # Function Details (Non-essential)
        compiled_output.append(f"# Function {self.children[0]} ({'None' if not param_locs else repr(param_locs)[1:-1]})")
        compiled_output.append(f"# return {func_def.rtn_loc}, return label {func_def.rtn_label}")

        # Header Guard
        compiled_output.append(f"JUMP {func_def.end_label}")
        compiled_output.append(f"{func_def.start_label}:")

        # Function Contents
        self.children[2].compile(compiled_output, symbol_table)

        # Return, Jump & End Label
        compiled_output.append(f"{func_def.rtn_jump}:")
        compiled_output.append(f"JUMP {func_def.rtn_label}")
        compiled_output.append(f"{func_def.end_label}:")


class FunctionCall:
    def __init__(self, symbol, args):
        self.children = [symbol, args]

    def __repr__(self):
        return f"FuncCall({self.children})"

    def compile(self, compiled_output, symbol_table):
        func_def = symbol_table.lookup_function(self.children[0])
        params = func_def.param_locs
        args = self.children[1]

        # Check number of Args!
        if len(params) != len(args):
            raise Exception  # TODO: Add Error

        compiled_output.append(f"PUSH {func_def.rtn_loc}")
        compiled_output.append(f"PUSH {func_def.rtn_label}")
        for param in params:
            compiled_output.append(f"PUSH {param}")

        compiled_output.append(f"### FUNCTION CALL ###")

        # Copy Parameters to Arguments
        for i in range(len(params)):
            param = params[i]
            arg = args[i].compile(compiled_output, symbol_table)
            symbol_table.compare_type(param, arg)  # Typecheck Arguments
            compiled_output.append(f"# Parameter {param}, Argument {arg}")
            if param.is_array():
                compiled_output.extend(symbol_table.copy_array(src=arg, dest=param))
            else:
                compiled_output.append(f"VAL_COPY {arg} {param}")

        rtn_label = symbol_table.get_new_label(label_type="RETURN")

        compiled_output.append(f"VAL_COPY {rtn_label} {func_def.rtn_label}")
        compiled_output.append(f"JUMP {func_def.start_label}")
        compiled_output.append(f"{rtn_label}:")

        rtn_type = func_def.rtn_loc.var_type
        is_array = func_def.rtn_loc.is_array()
        rtn_value = symbol_table.get_entry(var_type=rtn_type, array=is_array)
        if is_array:
            compiled_output.extend(symbol_table.copy_array(src=func_def.rtn_loc, dest=rtn_value))
        else:
            compiled_output.append(f"VAL_COPY {func_def.rtn_loc} {rtn_value}")

        compiled_output.append(f"### END FUNCTION CALL ###")

        if params:
            params.reverse()
        for param in params:
            compiled_output.append(f"POP {param}")
        compiled_output.append(f"POP {func_def.rtn_label}")
        compiled_output.append(f"POP {func_def.rtn_loc}")

        if params:
            params.reverse()

        return rtn_value


class ReturnNode:
    def __init__(self, value):
        self.children = [value]

    def __repr__(self):
        return f"ReturnNode({self.children})"

    def compile(self, compiled_output, symbol_table):
        value = self.children[0].compile(compiled_output, symbol_table)
        symbol_table.return_function(compiled_output, value)