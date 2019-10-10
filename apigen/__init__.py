import re
import sys

REGEXPS = {
    r'@(\w+)\("([a-z/:]+)".*': r'# \1 \2'
}


def handle_line(rawline, context, regexp_dict):
    line = rawline.strip('\n').strip()
    for regexp_str, replacement in regexp_dict.items():
        regexp = re.compile(regexp_str)
        if regexp.match(line):
            return regexp.sub(replacement, line)


def generate_doc_for_file(filepath):
    with open(filepath, mode='r') as file:
        doc_lines = []
        context = dict()
        for line in file.readlines():
            doc_lines.append(handle_line(line, context, REGEXPS))
        return [l for l in doc_lines if l is not None]


def main():
    for filepath in sys.argv[1:]:
        print(generate_doc_for_file(filepath))


if __name__ == "__main__":
    main()
