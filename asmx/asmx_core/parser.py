valid_instruction_tokens = [
    "add",
    "sub",
    "mul",
    "div",
    "set",
    "inc",
    "dec",
    "mov",
    "jmp",
    "halt",
    "load",
    "store",
    "jlt",
    "jeq",
    "jgt",
    "rand",
    "hardcall"
]

from colorama import init, Fore, Style
RESET = Style.RESET_ALL
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW

valid_user_registers = { f"u{i}" for i in range(1, 9) }
valid_auto_registers = { f"a{i}" for i in range(1, 5) } 
valid_registers = valid_user_registers | valid_auto_registers

valid_instruction_grammar = {
    "add": ["register", "register_or_immediate"],
    "sub": ["register", "register_or_immediate"],
    "mul": ["register", "register_or_immediate"],
    "div": ["register", "register_or_immediate"],
    "set": ["register", "immediate"],
    "inc": ["register"],
    "dec": ["register"],
    "cmp": ["register", "register"],
    "mov": ["register", "register"],
    "jmp": ["label"],
    "halt": [],
    "load": ["register", "ram_address"],
    "store": ["ram_address", "register"],
    "jlt": ["register", "register_or_immediate", "label"],
    "jeq": ["register", "register_or_immediate", "label"],
    "jgt": ["register", "register_or_immediate", "label"],
    "rand": ["register", "register_or_immediate", "register_or_immediate"],
    "hardcall": ["immediate"]
}

package_namespaces = {}

class TokenStream:
    def __init__(self, tokens, line_num):
        self.tokens = tokens
        self.line_num = line_num
        self.index = 0

    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None
    
    def next(self):
        token = self.peek()
        self.index += 1
        return token
    
    def expect(self, kind):
        token = self.next()
        if token is None:
            print(f"{RED}[Line {self.line_num}] Expected {kind}, but got end of line.{RESET}")
            exit(1)

        if kind == "instruction":
            token = token.lower()
                
            if token in valid_instruction_tokens:
                return token # Regular instruction
            
            if token in package_namespaces:
                return token # Namespace instruction
        
            print(f"{RED}[Line {self.line_num}] Expected instruction, got '{token}'.{RESET}")
            exit(1)

        elif kind == "register":
            if token not in valid_registers:
                print(f"{RED}[Line {self.line_num}] Expected register, got '{token}'.{RESET}")
                exit(1)
            return token
        
        elif kind == "immediate":
            if not token.startswith("#"):
                print(f"{RED}[Line {self.line_num}] Expected immediate value, got '{token}'.{RESET}")
                exit(1)
            
            try:
                return int(token[1:])
            except ValueError:
                print(f"{RED}[Line {self.line_num}] Invalid number: '{token}'.{RESET}")
                exit(1)
        
        elif kind == "label":
            if token.startswith("@"):
                return token[1:]
            else:
                print(f"{RED}[Line {self.line_num}] Expected label, got '{token}'.{RESET}")
                exit(1)

        elif kind == "register_or_immediate":
            if token in valid_registers:
                return token
            elif token.startswith("#"):
                try:
                    return int(token[1:])
                except ValueError:
                    print(f"{RED}[Line {self.line_num}] Invalid immediate: '{token}'{RESET}")
                    exit(1)
            else:
                print(f"{RED}[Line {self.line_num}] Expected register or immediate, got '{token}'{RESET}")
                exit(1)
        
        elif kind == "ram_address":
            # Immediate numeric address
            if token.startswith("#"):
                try:
                    return int(token[1:])
                except ValueError:
                    print(f"{RED}[Line {self.line_num}] Invalid RAM address: '{token}'{RESET}")
                    exit(1)
            # Label reference
            elif token.startswith("@"):
                return token[1:]  # leave as unresolved label for now
            else:
                print(f"{RED}[Line {self.line_num}] Expected RAM address (e.g. #12 or @label), got '{token}'{RESET}")
                exit(1)

        elif kind == "string":
            if not (token.startswith('"') and token.endswith('"')):
                print(f"{RED}[Line {self.line_num}] Expected string, got '{token}'{RESET}")
                exit(1)
            
            return token[1:-1]

        else:
            print(f"{RED}[Error] Unknown expect type: {kind}{RESET}")
            exit(1)
        

def parse_instruction(ts: TokenStream):
    first_token = ts.expect("instruction") # This could either be a real instruction, or a namespace.

    if first_token in package_namespaces:
        subcommand = ts.next().lower()
        if subcommand is None:
            print(f"{RED}[Line {ts.line_num}] Expected subcommand after namespace '{first_token}'{RESET}")
            exit(1)
        
        grammar = package_namespaces[first_token]["grammar"].get(subcommand)
        if grammar is None:
            print(f"{RED}[Line {ts.line_num}] Unknown subcommand '{subcommand}' in namespace '{first_token}'{RESET}")
            exit(1)

        parsed_args = []
        for expected_type in grammar:
            parsed_args.append(ts.expect(expected_type))

        if ts.peek() is not None:
            print(f"{RED}[Line {ts.line_num}] Unexpected additional argument: '{ts.peek()}'{RESET}")
            exit(1)
        
        return {
            "type": "macro",
            "namespace": first_token,
            "subcommand": subcommand,
            "args": parsed_args,
            "line_num": ts.line_num
        }

    # Regular instruction
    expected_args = valid_instruction_grammar[first_token]
    parsed_args = []

    for expected_type in expected_args:
        arg = ts.expect(expected_type)
        parsed_args.append(arg)

    # Make sure there are no additional arguments that should not be there
    if ts.peek() is not None:
        print(f"{RED}[Line {ts.line_num}] Unexpected additional argument: '{ts.peek()}'{RESET}")
        exit(1)
    
    return {
        "type": "instruction",
        "opcode": first_token,
        "args": parsed_args,
        "line_num": ts.line_num
    }

def parse_line(tokens, line_num):
    if not tokens:
        print(f"{RED}[Line {line_num}] Empty or invalid line.{RESET}")
        exit(1)
    
    if tokens[0].startswith("@"):
        return {"type": "label", "name": tokens[0][1:], "line_num": line_num}
    return parse_instruction(TokenStream(tokens, line_num))

def register_package_macros(namespace, macros):
    package_namespaces[namespace] = macros
