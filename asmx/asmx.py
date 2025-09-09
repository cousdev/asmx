# asmx assembler (BOOT/RECOVERY assembled, DATA empty for now)
import argparse
import json
from pathlib import Path
from colorama import init, Fore, Style
import asmx.asmx_core.codegen as codegen
import asmx.asmx_core.packages as packages

init()


def open_docs():
    import webbrowser

    docs_path = Path(__file__).parent / "docs" / "index.html"
    docs_url = f"file://{docs_path.resolve()}"

    try:
        if not webbrowser.open(docs_url):
            raise Exception("[Error] Couldn't open docs, no suitable browser found.")
        else:
            print("Opening documentation...")
    except Exception:
        print("You could try manually opening it here:")
        print(f"{docs_url}")


def assemble_file(input_file):
    # Assembles a file individually
    import asmx.asmx_core.tokeniser as tokeniser
    import asmx.asmx_core.parser as parser
    import asmx.asmx_core.macros as macros

    source_file = tokeniser.read_source_file(input_file)
    results = []

    for line_num, line in source_file:
        tokens = tokeniser.tokenize_line_with_strings(line)
        try:
            results.append(parser.parse_line(tokens, line_num))
        except SyntaxError as e:
            print(f"{Fore.RED}Syntax error in {input_file}: {e}{Style.RESET_ALL}")
            break

    instructions = macros.dispatch_macros(results)
    address_table = codegen.find_labels(instructions)
    generated_code = codegen.generate_code(instructions, address_table)
    return generated_code


def build_disk_image(input_dir, output_file):
    """
    Build a flat disk image from a project directory containing sys.json, raw partitions, and a DATA folder.
    BOOT / RECOVERY are assembled; DATA is left empty for now.
    """
    input_dir = Path(input_dir)
    sys_json_path = input_dir / "sys.json"

    if not sys_json_path.exists():
        raise FileNotFoundError(f"{Fore.RED}sys.json not found in {input_dir}{Style.RESET_ALL}")

    with open(sys_json_path, "r") as f:
        sys_config = json.load(f)

    partitions = sys_config.get("partitions", [])
    partition_contents = []

    # Assemble boot and recovery
    for part in partitions:
        part_type = part["type"]

        if part_type in ("BOOT", "RECOVERY"):
            part_file = input_dir / part["file"]
            if not part_file.exists():
                raise FileNotFoundError(f"{Fore.RED}Partition file {part_file} not found.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Assembling {part_type} partition: {part_file}{Style.RESET_ALL}")
            assembled = assemble_file(part_file)
            partition_contents.append(assembled)

        elif part_type == "DATA":
            # Work on later
            partition_contents.append([])

        else:
            print(f"{Fore.YELLOW}Unknown partition type: {part_type}, leaving empty{Style.RESET_ALL}")
            partition_contents.append([])

    # Build the partition table
    pt_size = 1 + len(partitions) + 1

    pt_lines = ["001"]
    current_address = pt_size + 1  # first partition starts after PT
    for part, content in zip(partitions, partition_contents):
        name = part["name"]
        part_type = part["type"]
        pt_lines.append(f"{name}|{part_type}|{current_address}")
        current_address += len(content)  # next partition starts after current partition's content
    pt_lines.append("PT_END")

    # Combing the partition table and assembled code
    disk_image = pt_lines.copy()
    for content in partition_contents:
        disk_image.extend(content)

    # Write disk image
    codegen.write_output_file(output_file, disk_image)
    print(f"{Fore.GREEN}Successfully built disk image -> {output_file}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(description="ASMX Assembler / Disk Image Builder")
    parser.add_argument("--docs", action="store_true", help="Open documentation")
    parser.add_argument("--version", action="store_true", help="Show version number")
    parser.add_argument("input_dir", nargs="?", help="Directory containing sys.json and partitions")
    parser.add_argument("output_file", nargs="?", help="Output flat disk image file")

    args = parser.parse_args()

    if args.docs:
        open_docs()
        return

    if args.version:
        print("ASMX Assembler version 0.1.0")
        return

    if not (args.input_dir and args.output_file):
        parser.error(f"{Fore.RED}The following arguments are required: input_dir, output_file{Style.RESET_ALL}")

    packages.load_all_packages()
    build_disk_image(args.input_dir, args.output_file)


if __name__ == "__main__":
    main()
