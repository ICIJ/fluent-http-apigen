import re
import subprocess
import sys


class DefaultLineHandler:
    def __init__(self, regexp, replacement):
        self.replacement = replacement
        self.regexp = re.compile(regexp)

    def handle(self, line, context):
        return [self.regexp.sub(self.replacement, line).format(**context).strip()]

    def match(self, line):
        return self.regexp.match(line)


class ContextLineHandler(DefaultLineHandler):
    def __init__(self, regexp, context_key):
        super().__init__(regexp, None)
        self.context_key = context_key

    def handle(self, line, context):
        context[self.context_key] = self.regexp.match(line).group(1)
        return []


class JavadocLineHandler(DefaultLineHandler):
    def __init__(self):
        super().__init__(r'/?\*(.*)', r'\1')

    def handle(self, line, context):
        javadoc_line = self.regexp.sub(self.replacement, line).strip()

        if context.get('javadoc') == 'true':
            if javadoc_line.startswith('@param'):
                context['javadoc_lines'].append(javadoc_line.replace('@param', '* **Parameter**'))
            elif javadoc_line.startswith('@return'):
                context['javadoc_lines'].append(javadoc_line.replace('@return', '* **Return**'))
            elif javadoc_line.startswith('$('):
                command = javadoc_line.replace('$', '').strip('()')
                cp = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                context['javadoc_lines'].append('```')
                context['javadoc_lines'].append(command)
                context['javadoc_lines'] += cp.stdout.strip(b'\n').decode('utf-8').split('\n')
                context['javadoc_lines'].append('```')
            elif javadoc_line.endswith('/'):
                context['javadoc'] = 'false'
            else:
                context['javadoc_lines'].append(javadoc_line)
            return []
        elif javadoc_line == '*':
            context['javadoc'] = 'true'
            context['javadoc_lines'] = []
            return []


class EndPointLineHandler(DefaultLineHandler):
    def handle(self, line, context):
        lines = [self.add_anchor(self.regexp.sub(self.replacement, line).format(**context))]
        if 'javadoc_lines' in context:
            lines += context['javadoc_lines']
            del context['javadoc_lines']
        return lines

    def match(self, line):
        return 'Prefix' not in line and super().match(line)

    def add_anchor(self, line):
        line_array = line.split()
        line_array.insert(1, '<a name="%s"></a>' % generate_anchor(line_array[-2], line_array[-1]))
        return ' '.join(line_array)


class TocEndPointLineHandler(EndPointLineHandler):
    def add_anchor(self, line):
        [prefix, method, url] = line.split()
        anchor = generate_anchor(method, url)
        return '  %s [%s %s](#%s)' % (prefix, method, url, anchor)


def generate_anchor(method, url):
    return '%s_%s' % (method.lower(), url.lower().replace(' ', '_').replace('/', '_').replace(':', '_'))


LINE_HANDLERS = [
    JavadocLineHandler(),
    ContextLineHandler(r'@Prefix\("([a-zA-Z/]+)".*', 'url_prefix'),
    DefaultLineHandler(r'@Prefix\("([a-zA-Z/]+)".*', r'# <a name="\1"></a>\1'),
    EndPointLineHandler(r'@(\w+)\("?([a-zA-Z/:\?=]*)"?.*', r'## \1 {url_prefix}\2'),
]

TOC_LINE_HANDLERS = [
    ContextLineHandler(r'@Prefix\("([a-zA-Z/]+)".*', 'url_prefix'),
    DefaultLineHandler(r'@Prefix\("([a-zA-Z/]+)".*', r'- [\1](#\1)'),
    TocEndPointLineHandler(r'@(\w+)\("?([a-zA-Z/:\?=]*)"?.*', r'- \1 {url_prefix}\2'),
]


def handle_line(rawline, context, line_handlers):
    line = rawline.strip()
    lines = []
    for line_handler in line_handlers:
        if line_handler.match(line):
            lines += line_handler.handle(line, context)
    return lines


def generate_doc_for_file(filepath, handlers):
    with open(filepath, mode='r') as file:
        doc_lines = []
        context = {'javadoc': 'false'}
        for line in file.readlines():
            doc_lines += handle_line(line, context, handlers)
        return [l for l in doc_lines if l is not None]


def main():
    print('Generated with https://github.com/ICIJ/fluent-http-apigen')
    print('# Table of Content')
    for filepath in sys.argv[1:]:
        for line in generate_doc_for_file(filepath, TOC_LINE_HANDLERS):
            print(line)
    print('\n')
    for filepath in sys.argv[1:]:
        for line in generate_doc_for_file(filepath, LINE_HANDLERS):
            print(line)


if __name__ == "__main__":
    main()