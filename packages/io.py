# packages/testkit.py

character_encoding = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8
}


def expand_text(instruction):
    # This just expands a text macro like:
    # IO TEXT #20 "HELLO" into a sequence of SET/STORE instructions
    print("expand_text was called.")

    start_addr, string = instruction["args"]
    line_num = instruction["line_num"]
    
    expanded = []
    for i, char in enumerate(string.upper()):
        ascii_code = ord(char) - 64 if char.isalpha() else 27 if char == " " else 0
        expanded.append(f"set u1 #{ascii_code}")
        expanded.append(f"store #{start_addr + i} u1")

    # Add null terminator
    expanded.append(f"set u1 #0")
    expanded.append(f"store #{start_addr + len(string)} u1")

    # Add a hardcall (100)
    expanded.append("hardcall #100")

    return expanded

def expand_mode(instruction):
    mode = instruction["args"][0]
    return [
        f"SET a1 #{mode}",
        f"STORE #1 a1"
    ]

def expand_config(instruction):
    x, y, size, spacing = instruction["args"]
    return [
        f"SET a1 #{x}",
        "STORE #2 a1",
        f"SET a1 #{y}",
        "STORE #3 a1",
        f"SET a1 #{size}",
        "STORE #4 a1",
        f"SET a1 #{spacing}",
        "STORE #6 a1"
    ]

# This is the package registry
package_registry = {
    "namespace": "io",
    "grammar": {
        "text": ["ram_address", "string"],
        "mode": ["immediate"]
    },
    "macros": {
        "text": expand_text,
        "mode": expand_mode
    }
}
