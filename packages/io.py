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
    start_addr, string = instruction["args"]
    line_num = instruction["line_num"]
    
    expanded = []

    # Set the mode to TextOutput mode.
    expanded.append("SET a1 #1")
    expanded.append("STORE #1 a1")

    # Set the text pointer to the start location.
    expanded.append(f"set a1 #{start_addr}")
    expanded.append("store #5 a1")

    for i, char in enumerate(string.upper()):
        encoded = character_encoding.get(char, 72)
        expanded.append(f"set a1 #{encoded}")
        expanded.append(f"store #{start_addr + i} a1")

    # Add null terminator
    expanded.append(f"set a1 #0")
    expanded.append(f"store #{start_addr + len(string)} a1")

    # Add a hardcall (100)
    expanded.append("hardcall #100")

    return expanded

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

def expand_input(instruction):
    start_addr = instruction["args"][0]

    expanded = []

    # Set the mode to TextInput mode.
    expanded.append("SET a1 #2")
    expanded.append("STORE #1 a1")

    # Set the text pointer to the start location.
    expanded.append(f"set a1 #{start_addr}")
    expanded.append("store #5 a1")

    # Make a hardcall
    expanded.append("hardcall #100")

    return expanded


# This is the package registry
package_registry = {
    "namespace": "io",
    "grammar": {
        "text": ["ram_address", "string"],
        "config": ["immediate", "immediate", "immediate", "immediate"],
        "input": ["ram_address"]
    },
    "macros": {
        "text": expand_text,
        "config": expand_config,
        "input": expand_input
    }
}
