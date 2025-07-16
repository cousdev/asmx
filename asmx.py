#!/usr/bin/env python3

# asmx assembler
# This file is the main entry point into the assembler
import asmx_core.tokeniser as tokeniser
import asmx_core.parser as parser
import asmx_core.macros as macros
import asmx_core.codegen as codegen
import asmx_core.packages as packages

import sys

packages.load_all_packages()


source_file_location = sys.argv[1]
dest_file_location = sys.argv[2]
source_file = tokeniser.read_source_file(source_file_location)


results = []

for line_num, line in source_file:
        tokens = tokeniser.tokenize_line_with_strings(line)
        try:
            results.append(parser.parse_line(tokens, line_num))
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            break

instructions = macros.dispatch_macros(results)

address_table = codegen.find_labels(instructions)

generated_code = codegen.generate_code(instructions, address_table)

codegen.write_output_file(dest_file_location, generated_code)
print("Finished!")
