valid_instruction_tokens = [
    "add",
    "sub",
    "mul",
    "div",
    "set",
    "inc",
    "dec",
    "cmp",
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
    "jlt": ["register", "label"],
    "jeq": ["register", "label"],
    "jgt": ["register", "label"],
    "rand": ["register", "register_or_immediate", "register_or_immediate"],
    "hardcall": ["immediate"]
}

package_namespace = {}

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
            raise SyntaxError(f"[Line {self.line_num}] Expected {kind}, but got end of line.")

        if kind == "instruction":
            token = token.lower()
                
            if token in valid_instruction_tokens:
                return token # Regular instruction
            
            if token in package_namespace:
                return token # Namespace instruction
        
            raise SyntaxError(f"[Line {self.line_num}] Expected instruction, got '{token}'.")

        elif kind == "register":
            if token not in valid_registers:
                raise SyntaxError(f"[Line {self.line_num}] Expected register, got '{token}'.")
            return token
        
        elif kind == "immediate":
            if not token.startswith("#"):
                raise SyntaxError(f"[Line {self.line_num}] Expected immediate value, got '{token}'.")
            
            try:
                return int(token[1:])
            except ValueError:
                raise SyntaxError(f"[Line {self.line_num}] Invalid number: '{token}'.")
        
        elif kind == "label":
            if token.startswith("@"):
                return token[1:]
            else:
                raise SyntaxError(f"[Line {self.line_num}] Expected label, got '{token}'.")

        elif kind == "register_or_immediate":
            if token in valid_registers:
                return token
            elif token.startswith("#"):
                try:
                    return int(token[1:])
                except ValueError:
                    raise SyntaxError(f"[Line {self.line_num}] Invalid immediate: '{token}'")
            else:
                raise SyntaxError(f"[Line {self.line_num}] Expected register or immediate, got '{token}'")
        
        elif kind == "ram_address":
            # Immediate numeric address
            if token.startswith("#"):
                try:
                    return int(token[1:])
                except ValueError:
                    raise SyntaxError(f"[Line {self.line_num}] Invalid RAM address: '{token}'")
            # Label reference
            elif token.startswith("@"):
                return token[1:]  # leave as unresolved label for now
            else:
                raise SyntaxError(f"[Line {self.line_num}] Expected RAM address (e.g. #12 or @label), got '{token}'")

        else:
            raise ValueError(f"Unknown expect type: {kind}")
        

def parse_instruction(ts: TokenStream):
    opcode = ts.expect("instruction")

    expected_args = valid_instruction_grammar[opcode]
    parsed_args = []

    for expected_type in expected_args:
        arg = ts.expect(expected_type)
        parsed_args.append(arg)

    # Make sure there are no additional arguments that should not be there
    if ts.peek() is not None:
        raise SyntaxError(f"[Line {ts.line_num}] Unexpected additional argument: '{ts.peek()}'")
    
    return {
        "type": "instruction",
        "opcode": opcode,
        "args": parsed_args,
        "line_num": ts.line_num
    }

def parse_line(tokens, line_num):
    if not tokens:
        raise SyntaxError(f"[Line {line_num}] Empty or invalid line.")
    
    if tokens[0].startswith("@"):
        return {"type": "label", "name": tokens[0][1:], "line_num": line_num}
    return parse_instruction(TokenStream(tokens, line_num))

def register_package_macros(namespace, macros):
    package_namespace[namespace] = macros
