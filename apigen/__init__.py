import re
import sys
from collections import namedtuple

LineHandler = namedtuple("LineHandler", "name regexp replacement")

LINE_HANDLERS = [
    LineHandler('prefix', r'@Prefix\("([a-zA-Z/]+)".*', 'context[url_prefix]'),
    LineHandler('http_endpoint', r'@(\w+)\("([a-zA-Z/:\?=]+)".*', r'## \1 {url_prefix}\2'),
]


CONTEXT_REGEXP = re.compile(r'context\[([a-z_]+)\]')


def handle_line(rawline, context, line_handlers):
    line = rawline.strip()
    if line.startswith('/**'):
        context['javadoc'] = 'true'
        context['javadoc_lines'] = []
        return []

    if context['javadoc'] == 'true':
        javadoc_line = line.replace('*', '').strip()
        if javadoc_line.startswith('@param'):
            context['javadoc_lines'].append(javadoc_line.replace('@param', '**Parameter**'))
        elif javadoc_line.startswith('@return'):
            context['javadoc_lines'].append(javadoc_line.replace('@return', '**Return**'))
        elif javadoc_line.endswith('/'):
            context['javadoc'] = 'false'
        else:
            context['javadoc_lines'].append(javadoc_line)
        return []

    for line_handler in line_handlers:
        regexp = re.compile(line_handler.regexp)
        if regexp.match(line):
            if 'context' in line_handler.replacement:
                key_match = CONTEXT_REGEXP.match(line_handler.replacement)
                value_match = regexp.match(line)
                context[key_match.group(1)] = value_match.group(1)
                return []
            elif line_handler.name == 'http_endpoint':
                lines = [regexp.sub(line_handler.replacement, line).format(**context)]
                if 'javadoc_lines' in context:
                    lines += context['javadoc_lines']
                    del context['javadoc_lines']
                return lines
            else:
                return [regexp.sub(line_handler.replacement, line).format(**context)]
    return []


def generate_doc_for_file(filepath):
    print(filepath)
    with open(filepath, mode='r') as file:
        doc_lines = []
        context = {'javadoc': 'false'}
        for line in file.readlines():
            doc_lines += handle_line(line, context, LINE_HANDLERS)
        return [l for l in doc_lines if l is not None]


def main():
    for filepath in sys.argv[1:]:
        for line in generate_doc_for_file(filepath):
            print(line)


if __name__ == "__main__":
    main()