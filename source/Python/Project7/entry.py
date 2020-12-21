class RedeclarationError(Exception): pass
class UndeclaredError(Exception): pass
class TypeError450(Exception): pass
class GTFO_Outside_Of_Loop(Exception): pass


class SymbolTable:
    def __init__(self):
        self.declared_variables = {}
        self.var_count = 1
        self.gtfo_stack = []
        self.label_count = 1

    def get_label(self, name):
        label = f"{name}_{self.label_count}"
        self.label_count += 1
        return label

    def start_while_compilation(self, while_end_label):
        self.gtfo_stack.append(while_end_label)

    def end_while_compilation(self, while_end_label):
        top_stack = self.gtfo_stack[-1]
        assert top_stack == while_end_label
        self.gtfo_stack.pop()

    def top_of_while_stack(self):
        if not self.gtfo_stack:
            raise GTFO_Outside_Of_Loop("You FOOL!")
        return self.gtfo_stack[-1]

    def declare_variable(self, name, declaration_type):
        if name in self.declared_variables:
            raise RedeclarationError(f'{name} has already been declared!')
        entry = self.get_entry(declaration_type)
        self.declared_variables[name] = entry
        return entry

    def get_entry_for_variable(self, name):
        if name not in self.declared_variables:
            raise UndeclaredError(f'{name} has not been declared!')
        return self.declared_variables[name]

    def get_entry(self, expr_type):
        address = self.var_count
        self.var_count += 1
        address = f"s{address}"
        return Entry(address, expr_type)


class Entry:
    def __init__(self, address, expr_type):
        self.address = address
        self.expr_type = expr_type
        self.array_entry = None
        self.index_entry = None

    def __repr__(self):
        return self.address


if __name__ == "__main__":
    st = SymbolTable()

    # pretend assignment
    entry_left = st.get_entry("NUMBR")
    entry_right = st.get_entry("NUMBR")
    if entry_left.expr_type != entry_right.expr_type:
        raise TypeError450(f"{entry_left.expr_type} != {entry_right.expr_type}")

    entry_result = st.get_entry("NUMBR")
