# packages/stack.py

def expand_push(instruction):
    target_reg = instruction["args"][0]
    expanded = []

    expanded.append("DEC u8")
    expanded.append(f"STORER u8 {target_reg}")


def expand_pop(instruction):
    target_reg = instruction["args"][0]
    expanded = []

    expanded.append(f"LOADR {target_reg} u8")
    expanded.append("INC u8")
    

def expand_peek(instruction):
    print()

def expand_drop(instruction):
    print()

package_registry = {
    "namespace": "stack",
    "grammar": {
        "push": ["register"],
        "pop": ["register"],
        "peek": ["register"],
        "drop": []
    },
    "macros": {
        "push": expand_push,
        "pop": expand_pop,
        "peek": expand_peek,
        "drop": expand_drop
    }
}
