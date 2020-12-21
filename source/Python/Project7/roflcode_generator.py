def generate_ROFLcode_from_LMAOcode(lmao_code):
    rofl_code = [f"STORE 10000 0", f"VAL_COPY 20000 regH"]  # Free Memory Starts at 10K; Stack at 20K

    lines_str = lmao_code.split("\n")
    lines_new = []
    for i in range(len(lines_str)):
        line = lines_str[i]

        if "VAL_COPY" in line and line[-1] == "'":
            lines_new.append(line + "\\n" + lines_str[i + 1])
        elif line and line[0] == "'":
            pass
        else:
            lines_new.append(line)

    lines = [line.split(" ") for line in lines_new]
    lines.pop()

    for line in lines:
        # print(f"Line: {line}")
        rofl_code.append(f"### CONVERTING {line[0]} ###")

        if not line:
            continue

        command = line[0]
        if command == "VAL_COPY":
            value = line[1]
            if value == "'":
                value = "' '"
            elif value[0] == "s" or value[0] == "a":
                rofl_code.append(f"LOAD {value[1:]} regB")
                value = "regB"
            dest = line[-1][1:]
            rofl_code.append(f"VAL_COPY {value} regA")
            rofl_code.append(f"STORE regA {dest}")
        elif command == "OUT_NUM":
            if line[1][0] == 's':
                src = line[1][1:]
                rofl_code.append(f"LOAD {src} regA")
            else:
                src = line[1]
                rofl_code.append(f"VAL_COPY {src} regA")
            rofl_code.append(f"OUT_NUM regA")
        elif command == "OUT_CHAR":
            if line[1][0] == 's':
                src = line[1][1:]
                rofl_code.append(f"LOAD {src} regA")
            else:
                src = line[1]
                rofl_code.append(f"VAL_COPY {src} regA")
            rofl_code.append(f"OUT_CHAR regA")
        elif command == "RANDOM":
            dest = line[-1][1:]
            rofl_code.append(f"RANDOM regA")
            rofl_code.append(f"STORE regA {dest}")
        elif command == "IN_CHAR":
            dest = line[-1][1:]
            rofl_code.append(f"IN_CHAR regA")
            rofl_code.append(f"STORE regA {dest}")
        elif command in ["ADD", "SUB", "DIV", "MULT", "TEST_NEQU", "TEST_EQU", "TEST_GTR", "TEST_LESS"]:
            flags = [0, 0]  # First Argument is Literal, Second Argument is Literal
            if line[1][0] != 's':
                flags[0] = 1
                src1 = line[1]
            else:
                src1 = line[1][1:]
            if line[2][0] != 's':
                flags[1] = 1
                src2 = line[2]
            else:
                src2 = line[2][1:]
            dest = line[3][1:]
            if flags[0]:
                rofl_code.append(f"VAL_COPY {src1} regA")
            else:
                rofl_code.append(f"LOAD {src1} regA")
            if flags[1]:
                rofl_code.append(f"VAL_COPY {src2} regB")
            else:
                rofl_code.append(f"LOAD {src2} regB")
            rofl_code.append(f"{command} regA regB regC")
            rofl_code.append(f"STORE regC {dest}")
        elif command in ["JUMP_IF_0", "JUMP_IF_N0"]:
            src = line[1][1:]
            label = line[2]
            rofl_code.append(f"LOAD {src} regA")
            rofl_code.append(f"{command} regA {label}")
        elif command == "JUMP":
            label = line[1]
            if label[0] == 's' and label[1:].isdigit():
                rofl_code.append(f"LOAD {label[1:]} regE")
                rofl_code.append(f"{command} regE")
            else:
                rofl_code.append(f"{command} {label}")
        elif command == "AR_GET_SIZE":
            array = line[1][1:]
            size = line[2][1:]
            rofl_code.append(f"LOAD {array} regA")
            rofl_code.append(f"MEM_COPY regA {size}")
        elif command == "AR_SET_SIZE":
            array = line[1][1:]
            if line[2][0] == 's':
                size = line[2][1:]
            else:
                size = line[2]
            rofl_code.append(f"LOAD {size} regA")
            rofl_code.append(f"LOAD 0 regB")
            rofl_code.append(f"STORE regB {array}")
            rofl_code.append(f"STORE regA regB")
            rofl_code.append(f"ADD regA regB regC")
            rofl_code.append(f"ADD 1 regC regC")
            rofl_code.append(f"STORE regC 0")
        elif command == "AR_GET_IDX":
            array = line[1][1:]
            size = line[2][1:]
            result = line[3][1:]
            rofl_code.append(f"LOAD {array} regA")
            rofl_code.append(f"LOAD {size} regB")
            rofl_code.append(f"ADD regA 1 regA")
            rofl_code.append(f"ADD regA regB regA")
            rofl_code.append(f"MEM_COPY regA {result}")
        elif command == "AR_SET_IDX":
            array = line[1][1:]
            index = line[2][1:]
            value = line[3][1:]
            rofl_code.append(f"LOAD {array} regA")
            if line[2][0] != 's':
                rofl_code.append(f"VAL_COPY {line[2]} regB")
            else:
                rofl_code.append(f"LOAD {index} regB")
            rofl_code.append(f"ADD regA 1 regA")
            rofl_code.append(f"ADD regA regB regA")
            if line[3][0] != 's':
                rofl_code.append(f"STORE {line[3]} regA")
            else:
                rofl_code.append(f"MEM_COPY {value} regA")
        elif line[-1] and line[-1][-1] == ":":
            rofl_code.append(" ".join(line))
        elif command and command[0] == "#":
            continue
        elif command in ["PUSH", "POP"]:
            value = line[1]
            location = value[1:]

            if command == "PUSH":
                rofl_code.append(f"LOAD {location} regA")
                rofl_code.append(f"STORE regA regH")
                rofl_code.append(f"ADD 1 regH regH")

            else:  # command == "POP"
                rofl_code.append(f"SUB regH 1 regH")
                rofl_code.append(f"LOAD regH regA")
                rofl_code.append(f"STORE regA {location}")

        else:
            print(f"ERROR COMMAND <{command}> NOT HANDLED!")

    return '\n'.join(rofl_code) + '\n'
