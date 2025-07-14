import parser

TEMP_REGISTER = "a1"

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
                tokens = line.split()
                parsed = parser.parse_line(tokens, instruction["line_num"])
                parsed_instructions.append(parsed)

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


macro_expanders = {
    "add": expand_immediates,
    "sub": expand_immediates,
    "mul": expand_immediates,
    "div": expand_immediates,
    "cmp": expand_cmp,
}
