# packages/stack.py

def expand_push(instruction):
    target_reg = instruction["args"][0]
    expanded = []

    expanded.append("DEC a4")
    expanded.append(f"STORER a4 {target_reg}")

    return expanded


def expand_pop(instruction):
    target_reg = instruction["args"][0]
    expanded = []

    expanded.append(f"LOADR {target_reg} a4")
    expanded.append("INC a4")

    return expanded
    

def expand_peek(instruction):
    target_reg = instruction["args"][0]
    expanded = []

    expanded.append(f"LOADR {target_reg} a4")

    return expanded

def expand_drop(instruction):
    return ["INC a4"]

def expand_reset(instruction):
    return [
        "SET a3 #20000",
        "SET a4 #200000"
    ]

package_registry = {
    "namespace": "stack",
    "grammar": {
        "push": ["register"],
        "pop": ["register"],
        "peek": ["register"],
        "drop": [],
        "reset": []
    },
    "macros": {
        "push": expand_push,
        "pop": expand_pop,
        "peek": expand_peek,
        "drop": expand_drop,
        "reset": expand_reset
    }
}
