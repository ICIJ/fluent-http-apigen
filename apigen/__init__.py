import re
import sys

REGEXPS = {
    r'@Prefix\("([a-zA-Z/]+)".*': 'context[url_prefix]',
    r'@(\w+)\("([a-zA-Z/:\?=]+)".*': r'# \1 {url_prefix}\2'
}

CONTEXT_REGEXP = re.compile(r'context\[([a-z_]+)\]')


def handle_line(rawline, context, regexp_dict):
    line = rawline.strip('\n').strip()
    if line.startswith('/**'):
        context['javadoc'] = 'true'
        return line[3:]

    if context['javadoc'] == 'true':
        javadoc_line = line.replace('*', '').strip()
        if javadoc_line.startswith('@param'):
            return javadoc_line.replace('@param', '**Parameter**')
        if javadoc_line.startswith('@return'):
            return javadoc_line.replace('@return', '**Return**')
        if javadoc_line.endswith('/'):
            context['javadoc'] = 'false'
            return javadoc_line.strip('/')
        else:
            return javadoc_line

    for regexp_str, replacement in regexp_dict.items():
        regexp = re.compile(regexp_str)
        if regexp.match(line):
            if 'context' in replacement:
                key_match = CONTEXT_REGEXP.match(replacement)
                value_match = regexp.match(line)
                context[key_match.group(1)] = value_match.group(1)
                return
            else:
                return regexp.sub(replacement, line).format(**context)


def generate_doc_for_file(filepath):
    print(filepath)
    with open(filepath, mode='r') as file:
        doc_lines = []
        context = {'javadoc': 'false'}
        for line in file.readlines():
            doc_lines.append(handle_line(line, context, REGEXPS))
        return [l for l in doc_lines if l is not None]


def main():
    for filepath in sys.argv[1:]:
        for line in generate_doc_for_file(filepath):
            print(line)


if __name__ == "__main__":
    main()