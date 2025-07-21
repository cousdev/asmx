# asmx assembler
# This file is the main entry point into the assembler

def open_docs():
    import webbrowser
    from pathlib import Path

    docs_path = Path(__file__).parent / "docs" / "index.html"
    docs_url = f"file://{docs_path.resolve()}"

    try:
        if not webbrowser.open(docs_url):
            raise Exception("[Error] Couldn't open docs, no suitable browser found.")
        else:
            print("Opening documentation...")
    except Exception as e:
        print("You could try manually opening it here:")
        print(f"{docs_url}")

def main():
    import asmx.asmx_core.tokeniser as tokeniser
    import asmx.asmx_core.parser as parser
    import asmx.asmx_core.macros as macros
    import asmx.asmx_core.codegen as codegen
    import asmx.asmx_core.packages as packages

    import argparse
    from colorama import init, Fore, Style

    init()

    argparse_parser = argparse.ArgumentParser(
         description="ASMX Assembler, for the ASMX VM platform."
    )

    # Optional flag
    argparse_parser.add_argument("--docs", action="store_true", help="Shows documentation.")
    argparse_parser.add_argument("--version", action="store_true", help="Shows the version number.")

    # Positional args (required by default)
    argparse_parser.add_argument("input_file", nargs="?", help="Source .asmx file to assemble.")
    argparse_parser.add_argument("output_file", nargs="?", help="Output machine code file.")


    args = argparse_parser.parse_args()

    if args.docs:
        # Shows docs
        open_docs()
        return

    if args.version:
        # Shows the version
        print("ASMX Assembler version 0.1.0")
        return

    # If neither docs/version flags given, input_file AND output_file must be present
    if not (args.input_file and args.output_file):
        argparse_parser.error(f"{Fore.RED}The following arguments are required: input_file, output_file{Style.RESET_ALL}")

    print(f"{Fore.GREEN}Assembling {args.input_file} -> {args.output_file}{Style.RESET_ALL}")


    packages.load_all_packages()


    source_file_location = args.input_file
    dest_file_location = args.output_file
    source_file = tokeniser.read_source_file(source_file_location)


    results = []

    for line_num, line in source_file:
            tokens = tokeniser.tokenize_line_with_strings(line)
            try:
                results.append(parser.parse_line(tokens, line_num))
            except SyntaxError as e:
                print(f"{Fore.RED}Syntax error: {e}{Style.RESET_ALL}")
                break

    instructions = macros.dispatch_macros(results)

    address_table = codegen.find_labels(instructions)

    generated_code = codegen.generate_code(instructions, address_table)

    codegen.write_output_file(dest_file_location, generated_code)
    print(f"{Fore.GREEN}Successfully assembled {args.input_file} -> {args.output_file}{Style.RESET_ALL}")
