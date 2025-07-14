import re

def read_source_file(source_file_location):
    with open(source_file_location, 'r') as source_file:
        source_file_lines = source_file.readlines()

    cleaned_source_file_tokens = []
    for line_number, line in enumerate(source_file_lines, start=1):
        # Use regular expressions to remove inline comments and whitespace.
        line = re.sub(r';.*', '', line).strip()

        # If the line is not empty, add it to the cleaned lines.
        if line:
            cleaned_source_file_tokens.append((line_number, line))

    return cleaned_source_file_tokens