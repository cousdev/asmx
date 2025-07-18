from colorama import init, Fore, Style
RESET = Style.RESET_ALL
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW

def find_labels(instructions):
    label_addresses = {}
    address = 1

    for instruction in instructions:
        if instruction["type"] == "label":
            label_addresses[instruction["name"]] = address
        else:
            address += 1

    return label_addresses


def normalise_arg(arg, label_addresses):
    if isinstance(arg, str):
        if arg in label_addresses:
            # Replace label with its resolved address
            return label_addresses[arg]
        elif arg.startswith("u"):
            # User register: strip 'u' and convert to int
            return int(arg[1:])
        elif arg.startswith("a"):
            # Assembler register: strip 'a', convert to int, add 8
            return int(arg[1:]) + 8
        else:
            print(f"{RED}[Argument Normalisation Failure] Unknown argument string: {arg}{RESET}")
            exit(1)
    elif isinstance(arg, int):
        # Immediate number, leave as is
        return arg
    else:
        print(f"{RED}[Argument Normalisation Failure] Unexpected argument type: {type(arg)}{RESET}")
        exit(1)


def generate_code(instructions, label_addresses):
    output_lines = []
    for instruction in instructions:
        if instruction.get("type") != "instruction":
            continue

        opcode = instruction["opcode"]
        normalised_args = [str(normalise_arg(arg, label_addresses)) for arg in instruction["args"]]
        output_line = "_".join([opcode] + normalised_args)
        output_lines.append(output_line)

    return output_lines

def write_output_file(filename, assembled_lines):
    with open(filename, 'w') as f:
        for line in assembled_lines:
            f.write(line + '\n')