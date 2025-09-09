from . import parser
from . import packages

TEMP_REGISTER = "a1"
TEMP_MIN = "a1"
TEMP_MAX = "a2"

from colorama import init, Fore, Style
RESET = Style.RESET_ALL
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW

def dispatch_macros(instruction_list, max_passes=500):
    i = 0
    passes = 0

    while i < len(instruction_list):
        instruction = instruction_list[i]
        if passes > max_passes:
            print(f"{RED}[Macro Recursion] Macro expansion exceeded max passes. Possible infinite recursion.{RESET}")
            exit(1)

        if instruction.get("type") == "label":
            i += 1
            continue

        if instruction.get("type") == "macro":
            namespace = instruction["namespace"]
            subcommand = instruction["subcommand"].lower()
            
            registry = packages.get_all_macro_registries().get(namespace)
            if not registry:
                print(f"{RED}[Error] No macro package registered for namespace '{namespace}'{RESET}")
                exit(1)
            
            macro_fn = registry["macros"].get(subcommand)
            if not macro_fn:
                print(f"{RED}[Error] No macro expansion function found for '{namespace} {subcommand}'{RESET}")
                exit(1)

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
                    print(f"{RED}[Error] Invalid macro expansion item: {line}{RESET}")
                    exit(1)

            instruction_list[i:i+1] = parsed_instructions
            
            passes += 1
            # Recheck the newly inserted instructions for further expansions
            # so do not increment i here.
            
        else:
            i += 1
                
    return instruction_list

def expand_immediates(instruction):
    args = instruction.get("args", [])
    opcode = instruction["opcode"]
    
    if len(args) < 2:
        return None
    
    dest = args[0]
    src = args[1]

    # Only expand if second arg is immediate (int), and NOT if it's already a SET
    if isinstance(src, int):
        if opcode == "set":
            # Don't expand a raw SET of immediate — already base level
            return None
        
        return [
            f"set {TEMP_REGISTER} #{src}",
            f"{opcode} {dest} {TEMP_REGISTER}"
        ]
    
    return None

def expand_jmp(instruction):
    opcode = instruction["opcode"]
    reg, immediate, label = instruction["args"]
    
    # If the second argument is an immediate, expand it.
    if isinstance(immediate, int):
        return [
            f"set {TEMP_REGISTER} #{immediate}",
            f"{opcode} {reg} {TEMP_REGISTER} @{label}"
        ]
    else:
        return None


    
def expand_rand(instruction):
    dest, min_val, max_val = instruction["args"]

    # If both min and max are already registers (not ints), no expansion needed
    if not isinstance(min_val, int) and not isinstance(max_val, int):
        return None  # Stop expanding here

    expanded_lines = []
    

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
    "jlt": expand_jmp,
    "jeq": expand_jmp,
    "jgt": expand_jmp,
    "rand": expand_rand
}
