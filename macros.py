import parser
import packages

TEMP_REGISTER = "a1"
TEMP_MIN = "a1"
TEMP_MAX = "a2"

def dispatch_macros(instruction_list, max_passes=10):
    #print(instruction_list)
    i = 0
    passes = 0

    while i < len(instruction_list):
        instruction = instruction_list[i]
        if passes > max_passes:
            raise RuntimeError("Macro expansion exceeded max passes. Possible infinite recursion.")

        if instruction.get("type") == "label":
            i += 1
            continue

        if instruction.get("type") == "macro":
            print("Processing macro")
            namespace = instruction["namespace"]
            subcommand = instruction["subcommand"].lower()
            
            registry = packages.get_all_macro_registries().get(namespace)
            if not registry:
                raise ValueError(f"No macro package registered for namespace '{namespace}'")
            
            macro_fn = registry["macros"].get(subcommand)
            if not macro_fn:
                raise ValueError(f"No macro expansion function found for '{namespace} {subcommand}'")

            expansion = macro_fn(instruction)

        elif instruction.get("type") == "instruction":
            opcode = instruction["opcode"]

            # Try find a suitable opcode specific expander
            expander = macro_expanders.get(opcode)
            if expander:
                expansion = expander(instruction)
            else:
                expansion = None

        else:
            expansion = None

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
            
            passes += 1
            # Recheck the newly inserted instructions for further expansions
            # so do not increment i here.
            
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
