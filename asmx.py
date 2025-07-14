# asmx assembler
# This file is the main entry point into the assembler
import tokeniser
import parser

import sys

source_file_location = sys.argv[1]
source_file = tokeniser.read_source_file(source_file_location)

for line_num, line in source_file:
        tokens = line.split()
        try:
            result = parser.parse_line(tokens, line_num)
            print(result)
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            break