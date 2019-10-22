from unittest import TestCase

from apigen import handle_line, LineHandler


class TestApigen(TestCase):
    def test_handle_empty_doc(self):
        context = {'javadoc': 'false'}
        self.assertEqual([], handle_line('a line', context, [LineHandler('name', r'not matching', r'')]))

    def test_handle_line(self):
        context = {'javadoc': 'false'}
        self.assertEqual(['a line'], handle_line('a line', context, [LineHandler('name', r'(.*)', r'\1')]))

    def test_handle_http_method(self):
        context = {'javadoc': 'false'}
        self.assertEqual(['# Post /my/url'], handle_line('@Post("/my/url")', context, [LineHandler('http_endpoint', r'@(\w+)\("([a-z/]+)".*', r'# \1 \2')]))

    def test_handle_http_method_with_javadoc_lines(self):
        context = {'javadoc': 'false','javadoc_lines': ['line 1', 'line 2']}
        self.assertEqual(['# Post /my/url', 'line 1', 'line 2'], handle_line('@Post("/my/url")', context, [LineHandler('http_endpoint', r'@(\w+)\("([a-z/]+)".*', r'# \1 \2')]))
        self.assertEqual({'javadoc': 'false'}, context)

    def test_handle_line_with_param(self):
        context = {'javadoc': 'false'}
        self.assertEqual(['# Get url/with/:param'], handle_line('@Get("url/with/:param")', context, [LineHandler('http_endpoint',r'@(\w+)\("([a-z/:]+)".*', r'# \1 \2')]))

    def test_handle_line_with_context_property(self):
        context = {'javadoc': 'false',
                   'url_prefix': 'pre/fix/'}
        self.assertEqual(['# Get pre/fix/url'], handle_line('@Get("url")', context, [LineHandler('http_endpoint', r'@(\w+)\("([a-z/:]+)".*',r'# \1 {url_prefix}\2')]))

    def test_handle_line_save_into_context(self):
        context = {'javadoc': 'false'}
        self.assertEqual([], handle_line('@Prefix("prefix")', context, [LineHandler('context_line', r'@Prefix\("([a-z/]+)".*', 'context[url_prefix]')]))
        self.assertEqual({'javadoc': 'false', 'url_prefix': 'prefix'}, context)

    def test_handle_line_javadoc_begin(self):
        context = dict()
        self.assertEqual([], handle_line('/**', context, list()))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': []}, context)

    def test_handle_line_javadoc_end(self):
        context = {'javadoc': 'true'}
        self.assertEqual([], handle_line('*/', context, list()))
        self.assertEqual({'javadoc': 'false'}, context)

    def test_handle_line_javadoc(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('* this is javadoc comment', context, list()))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['this is javadoc comment']}, context)

    def test_handle_line_javadoc_parameter(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('* @param name parameter name', context, list()))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['* **Parameter** name parameter name']}, context)

    def test_handle_line_javadoc_return(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('* @return object returned', context, list()))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['* **Return** object returned']}, context)

    def test_handle_javadoc_line_with_command_line(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('$(echo "hello world"| sed "s/ /\\n/")', context, list()))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['```', 'echo "hello world"| sed "s/ /\\n/"', 'hello', 'world', '```']}, context)

    def test_handle_javadoc_line_with_failing_command(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('$(unknown_command)', context, list()))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['```', 'unknown_command', '', '```']}, context)