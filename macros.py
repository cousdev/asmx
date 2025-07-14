import parser

TEMP_REGISTER = "a1"
TEMP_MIN = "a1"
TEMP_MAX = "a2"

def dispatch_macros(instruction_list):
    #print(instruction_list)
    i = 0
    while i < len(instruction_list):
        instruction = instruction_list[i]

        # Skip labels or other non-instruction entries
        if instruction.get("type") != "instruction":
            i += 1
            continue

        opcode = instruction["opcode"]

        # Try find a suitable opcode specific expander
        expander = macro_expanders.get(opcode)
        expansion = expander(instruction) if expander else None

        
        if expansion:
            print("Expanded with the result:")
            print(expansion)

            # Convert expanded lines to parsed instruction dicts
            parsed_instructions = []
            for line in expansion:
                if isinstance(line, dict):
                    # Already parsed code, no need to check it.
                    parsed_instructions.append(line)
                elif isinstance(line, str):
                    tokens = line.split()
                    parsed = parser.parse_line(tokens, instruction["line_num"])
                    parsed_instructions.append(parsed)
                else:
                    raise TypeError(f"Invalid macro expansion item: {line}")

            instruction_list[i:i+1] = parsed_instructions
            i += len(parsed_instructions)
        else:
            print("Wasn't expanded.")
            i += 1
                
    return instruction_list

def expand_immediates(instruction):
    args = instruction.get("args", [])

    # Expand instructions where the second argument is an immediate value.
    if len(args) > 1 and isinstance(instruction["args"][1], int):
        value = instruction["args"][1]
        opcode = instruction["opcode"]
        dest = instruction["args"][0]

        return [
            f"set {TEMP_REGISTER} #{value}",
            f"{opcode} {dest} {TEMP_REGISTER}"
        ]
    
    return None

def expand_cmp(instruction):
    left, right = instruction["args"]

    return [
        f"mov {TEMP_REGISTER} {left}",
        f"sub {TEMP_REGISTER} {right}",
        f"cmp {TEMP_REGISTER} {TEMP_REGISTER}"
    ]


def expand_jmp(instruction):
    register = None
    label = None
    line_number = instruction["line_num"]
    mode = None

    if instruction["opcode"] == "jmp":
        mode = 0
        label = instruction["args"][0]
    elif instruction["opcode"] == "jgt":
        mode = 1
        label = instruction["args"][1]
        register = instruction["args"][0]
    elif instruction["opcode"] == "jeq":
        mode = 2
        label = instruction["args"][1]
        register = instruction["args"][0]
    elif instruction["opcode"] == "jlt":
        mode = 3
        label = instruction["args"][1]
        register = instruction["args"][0]

    if mode != 0:
        return [
            f"cmp {register} {register}",
            {
                "type": "instruction",
                "opcode": "jmp",
                "args": [mode, label],
                "line_num": line_number
            }
        ]
    
    else:
        return [
            {
                "type": "instruction",
                "opcode": "jmp",
                "args": [mode, label],
                "line_num": line_number
            }
        ]

    
def expand_rand(instruction):
    expanded_lines = []
    dest, min_val, max_val = instruction["args"]

    if isinstance(min_val, int):
        expanded_lines.append(f"set {TEMP_MIN} #{min_val}"),
        min_operand = TEMP_MIN
    else:
        min_operand = min_val

    if isinstance(max_val, int):
        expanded_lines.append(f"set {TEMP_MAX} #{max_val}"),
        max_operand = TEMP_MAX
    else:
        max_operand = max_val

    expanded_lines.append(f"rand {dest} {min_operand} {max_operand}")
    return expanded_lines

macro_expanders = {
    "add": expand_immediates,
    "sub": expand_immediates,
    "mul": expand_immediates,
    "div": expand_immediates,
    "cmp": expand_cmp,
    "jmp": expand_jmp,
    "jlt": expand_jmp,
    "jeq": expand_jmp,
    "jgt": expand_jmp,
    "rand": expand_rand
}
