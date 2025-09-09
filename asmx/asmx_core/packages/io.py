# packages/io.py

character_encoding = {
    "!": 1,
    "#": 2,
    "$": 3,
    "%": 4,
    "&": 5,
    "'": 6,
    '"': 7,
    "(": 8,
    ")": 9,
    "*": 10,
    "+": 11,
    ",": 12,
    "-": 13,
    ".": 14,
    "/": 15,
    "0": 16,
    "1": 17,
    "2": 18,
    "3": 19,
    "4": 20,
    "5": 21,
    "6": 22,
    "7": 23,
    "8": 24,
    "9": 25,
    ":": 26,
    ";": 27,
    "<": 28,
    "=": 29,
    ">": 30,
    "?": 31,
    "@": 32,
    "A": 33,
    "B": 34,
    "C": 35,
    "D": 36,
    "E": 37,
    "F": 38,
    "G": 39,
    "H": 40,
    "I": 41,
    "J": 42,
    "K": 43,
    "L": 44,
    "M": 45,
    "N": 46,
    "O": 47,
    "P": 48,
    "Q": 49,
    "R": 50,
    "S": 51,
    "T": 52,
    "U": 53,
    "V": 54,
    "W": 55,
    "X": 56,
    "Y": 57,
    "Z": 58,
    "[": 59,
    "\\": 60,
    "]": 61,
    "^": 62,
    "_": 63,
    "`": 64,
    "{": 65,
    "|": 66,
    "}": 67,
    "~": 68,
    " ": 70,
}


def expand_text(instruction):
    string, x, y, size, spacing = instruction["args"]
    
    expanded = []

    # Push spacing, size, y, x
    expanded.append(f"SET a1 #{spacing}")
    expanded.append("STACK PUSH a1")
    # Push the text pointer
    expanded.append("STACK PUSH a3")
    expanded.append(f"SET a1 #{size}")
    expanded.append("STACK PUSH a1")
    expanded.append(f"SET a1 #{y}")
    expanded.append("STACK PUSH a1")
    expanded.append(f"SET a1 #{x}")
    expanded.append("STACK PUSH a1")
    # Set the mode to TextOutput mode.
    expanded.append("SET a1 #1")
    expanded.append("STACK PUSH a1")

    

    for i, char in enumerate(string.upper()):
        encoded = character_encoding.get(char, 72)
        expanded.append(f"set a1 #{encoded}")
        expanded.append(f"storer a3 a1")
        expanded.append("inc a3")

    # Add null terminator
    expanded.append(f"set a1 #0")
    expanded.append(f"storer a3 a1")
    expanded.append("inc a3")

    # Add a hardcall (100)
    expanded.append("hardcall #100")

    return expanded

def expand_input(instruction):
    x, y, size, spacing = instruction["args"]
    expanded = []

    # Push spacing, size, y, x
    expanded.append(f"SET a1 #{spacing}")
    expanded.append("STACK PUSH a1")
    # Push the text pointer
    expanded.append("STACK PUSH a3")
    expanded.append(f"SET a1 #{size}")
    expanded.append("STACK PUSH a1")
    expanded.append(f"SET a1 #{y}")
    expanded.append("STACK PUSH a1")
    expanded.append(f"SET a1 #{x}")
    expanded.append("STACK PUSH a1")
    
    # Set the mode to TextInput mode.
    expanded.append("SET a1 #2")
    expanded.append("STACK PUSH a1")

    # Make a hardcall
    expanded.append("hardcall #100")

    return expanded


# This is the package registry
package_registry = {
    "namespace": "io",
    "grammar": {
        "text": ["string", "immediate", "immediate", "immediate", "immediate"],
        "input": ["immediate", "immediate", "immediate", "immediate"]
    },
    "macros": {
        "text": expand_text,
        "input": expand_input
    }
}
