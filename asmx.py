# asmx assembler
# This file is the main entry point into the assembler
import tokeniser
import parser
import macros
import codegen
import packages

import sys

packages.load_all_packages()

"""
source_file_location = sys.argv[1]
dest_file_location = sys.argv[2]
source_file = tokeniser.read_source_file(source_file_location)


results = []

for line_num, line in source_file:
        tokens = line.split()
        try:
            results.append(parser.parse_line(tokens, line_num))
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            break

instructions = macros.dispatch_macros(results)
print(instructions)

address_table = codegen.find_labels(instructions)

generated_code = codegen.generate_code(instructions, address_table)

codegen.write_output_file(dest_file_location, generated_code)
print("Finished!")
"""