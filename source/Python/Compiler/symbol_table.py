from collections import ChainMap
class RedeclarationError(Exception): pass
class UndeclaredError(Exception): pass
class InvalidCastError(Exception): pass
class InvalidComparisonError(Exception): pass
class InvalidBreak(Exception): pass
class InvalidDefinition(Exception): pass
class SymbolTableError(Exception): pass

DEFAULT_SYMBOL_VALUE = 0
DEFAULT_SYMBOL_TYPE = None


class SymbolTable:
    def __init__(self):
        self.entries = 1
        self.table = dict()         # Entries
        self.scope = ChainMap()     # Symbols to Locations
        self.last_declared = None   # Last uninitialized Entry

        self.labels = {"if": 0, "while": 0, "comp": 0, "print": 0, "switch": 0, "case": 0, "return": 0}

        self.break_stack = []

        self.last_function = None
        self.function_defs = dict()

    def __repr__(self):
        table = [str(k) + ": " + str(v.value) + ", " + str(v.var_type) for k, v in self.table.items()]
        return f"{table}"

    def declare(self, identifier, var_type, value=DEFAULT_SYMBOL_VALUE):

        if identifier in self.scope.maps[0]:
            raise RedeclarationError(f"Redeclaration of {identifier} in the scope")

        address = self.get_entry(var_type=var_type, array=True if var_type[-1] == 'S' else False)

        self.scope[identifier] = address

        # TODO: REMOVE LATER
        address.value = value

        self.table[address] = address
        self.last_declared = address

        print(f"Assigning id [{identifier}] to register [{address}]")

        return address

    def assign(self, symbol=None, var_type=DEFAULT_SYMBOL_TYPE, value=DEFAULT_SYMBOL_VALUE):

        print(f"Assigning value [{value}] to register [{self.last_declared if symbol is None else symbol}]")

        # Assigning to Last Declared
        if symbol is None:
            address = self.last_declared
            self.last_declared = None

        # Assigning to Scalar (s location)
        else:
            address = symbol

        if address not in self.table:
            raise UndeclaredError(f"Assignment of undefined variable {symbol}")

        if var_type == DEFAULT_SYMBOL_TYPE:
            var_type = self.table[address].var_type

        elif not self.table[address].compare_type(var_type):
            raise InvalidCastError(f"Invalid Cast from {self.table[address].var_type} to {var_type}")

        # TODO: REMOVE LATER
        address.value = value

        self.table[address] = address

        return address

    def get_var(self, identifier):
        if identifier not in self.scope:
            raise UndeclaredError(f"Use of undefined variable {identifier}")

        address = self.scope[identifier]

        return address

    # Method to Place Literal in Register
    def assign_literal(self, var_type, value=DEFAULT_SYMBOL_VALUE, location=None):
        if location is None:
            address = self.get_entry(var_type)

        # TODO: REMOVE LATER
        address.value = value

        self.table[address] = address
        return address

    # Retrieve Next Register/S Value
    def get_entry(self, var_type, array=False):
        address = f"{'a' if array else 's'}{self.entries}"
        self.entries += 1
        entry = Entry(address, var_type)
        self.table[entry] = entry
        return entry

    def get_int(self):
        return self.assign_literal(var_type="NUMBR")

    def increment_scope(self):
        self.scope = self.scope.new_child()

    def decrement_scope(self):
        allowed = len(self.scope.maps) > 1
        if allowed:
            self.scope = self.scope.parents

    def get_type(self, symbol):
        if symbol in self.table:
            return self.table[symbol].var_type
        else:
            return None

    def compare_type(self, symbol1, symbol2, error=True):
        type1, type2 = self.get_type(symbol1), self.get_type(symbol2)
        if type1 != type2:
            if error:
                raise InvalidComparisonError(f"Cannot Compare Type [{type1}] to Type [{type2}]")
            else:
                return False
        elif symbol1.is_array() != symbol2.is_array():
            if symbol1.is_array():
                raise InvalidComparisonError(f"Cannot Compare Array Type [{type1}] to Array Type [{type2}]")
            else:
                raise InvalidComparisonError(f"Cannot Compare Array Type [{type1}] to Non-Array Type [{type2}]")
        elif not error:
            return True

    def get_new_label(self, label_type, end=True):
        label_type = label_type.lower()
        if label_type in self.labels:
            value = self.labels[label_type]
            if end:
                value += 1
                self.labels[label_type] = value
                if label_type == "while":
                    self.break_stack.append(f"while_{value}")
                elif label_type == "switch":
                    self.break_stack.append(f"switch_{value}")
            return f"{'end' if end else 'start'}_{label_type}_{value}"
        else:
            raise SymbolTableError(f"Get Label Failed on LabelType {label_type}")

    def break_loop(self):
        if not self.break_stack:
            pass
            # raise InvalidBreak(f"Cannot Break Outside of a Loop")
        else:
            if "switch" in self.break_stack[-1]:  # TODO: Switch Never Removed?
                return self.break_stack[-1]
            return self.break_stack.pop()

    def break_switch(self):
        if not self.break_stack:
            pass
            # raise InvalidBreak(f"Cannot Break Outside of a Switch Statement")
        else:
            self.break_stack.pop()

    def declare_function(self, symbol, param_locs, rtn_type):  # TODO: FUNCTION REDEFINITION ERROR
        if len(self.scope.maps) > 3:
            raise InvalidDefinition(f"Attempting to define function '{symbol}' outside of global scope!")

        rtn_loc = self.get_entry(var_type=rtn_type, array=(rtn_type[-1] == 'S'))
        rtn_label = self.get_int()

        function_def = FuncDef(symbol=symbol, rtn_loc=rtn_loc, rtn_label=rtn_label, param_locs=param_locs)
        self.function_defs[symbol] = function_def
        self.last_function = function_def
        return function_def

    def return_function(self, compiled_output, value):
        func_def = self.last_function

        # Check Return Type
        self.compare_type(value, func_def.rtn_loc)

        if func_def.rtn_loc.is_array():
            compiled_output.extend(self.copy_array(value, func_def.rtn_loc))
        else:
            compiled_output.append(f"VAL_COPY {value} {func_def.rtn_loc}")

        compiled_output.append(f"JUMP {func_def.rtn_jump}")

    def lookup_function(self, symbol):
        if symbol in self.function_defs:
            return self.function_defs[symbol]
        else:
            raise UndeclaredError(f"Unknown Function {symbol}")

    def copy_array(self, src, dest):
        output = []

        end = self.get_new_label(label_type="COMP")
        start = self.get_new_label(label_type="COMP", end=False)

        size = self.get_int()
        temp = self.assign_literal(var_type=src.var_type[:-1])
        comp = self.get_int()
        i = self.get_int()

        output.append(f"VAL_COPY 0 {i}")
        output.append(f"AR_GET_SIZE {src} {size}")
        output.append(f"AR_SET_SIZE {dest} {size}")
        output.append(f"{start}:")
        output.append(f"TEST_LESS {i} {size} {comp}")
        output.append(f"JUMP_IF_0 {comp} {end}")
        output.append(f"AR_GET_IDX {src} {i} {temp}")
        output.append(f"AR_SET_IDX {dest} {i} {temp}")
        output.append(f"ADD 1 {i} {i}")
        output.append(f"JUMP {start}")
        output.append(f"{end}:")

        return output

    def compare_arrays(self, array1, array2, result):
        output = []

        end_comp = self.get_new_label(label_type="COMP")
        start_comp = self.get_new_label(label_type="COMP", end=False)

        length1 = self.get_int()
        length2 = self.get_int()

        value1 = self.assign_literal(var_type=array1.var_type[:-1])
        value2 = self.assign_literal(var_type=array2.var_type[:-1])

        i = self.get_int()

        output.append(f"### BEGIN ARRAY COMP ###")

        output.append(f"AR_GET_SIZE {array1} {length1}")
        output.append(f"AR_GET_SIZE {array2} {length2}")
        output.append(f"TEST_EQU {length1} {length2} {result}")
        output.append(f"JUMP_IF_0 {result} {end_comp}")

        output.append(f"VAL_COPY 0 {i}")

        output.append(f"{start_comp}:")

        output.append(f"TEST_EQU {i} {length1} {result}")
        output.append(f"JUMP_IF_N0 {result} {end_comp}")

        output.append(f"AR_GET_IDX {array1} {i} {value1}")
        output.append(f"AR_GET_IDX {array2} {i} {value2}")
        output.append(f"TEST_EQU {value1} {value2} {result}")
        output.append(f"JUMP_IF_0 {result} {end_comp}")

        output.append(f"ADD 1 {i} {i}")
        output.append(f"JUMP {start_comp}")

        output.append(f"{end_comp}:")

        output.append(f"### END ARRAY COMP ###")

        return output


class Entry:
    def __init__(self, address, var_type):
        self.address = address
        self.var_type = var_type
        self.array_entry = None
        self.index_entry = None

        # TODO: Remove Later (debugging)
        self.value = DEFAULT_SYMBOL_VALUE

    def __repr__(self):
        return self.address

    def compare_type(self, var_type):
        if var_type in self.var_type:
            return True
        return False

    def is_array(self):
        return self.address[0] == 'a'

    def is_scalar(self):
        return self.address[0] == 's'


class FuncDef:
    def __init__(self, symbol, rtn_loc, rtn_label, param_locs):
        self.symbol = symbol
        self.rtn_loc = rtn_loc
        self.rtn_label = rtn_label
        self.param_locs = param_locs

        self.start_label = "_func_" + symbol
        self.end_label = "_func_end_" + symbol
        self.rtn_jump = "_func_rtn_" + symbol

    def __repr__(self):
        return f"func_{self.symbol}"
