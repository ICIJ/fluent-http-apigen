from unittest import TestCase

from apigen import handle_line, LINE_HANDLERS, TOC_LINE_HANDLERS


class TestApigen(TestCase):
    def test_handle_empty_doc(self):
        context = {'javadoc': 'false'}
        self.assertEqual([], handle_line('a line', context, LINE_HANDLERS))

    def test_handle_http_method(self):
        context = {'javadoc': 'false', 'url_prefix': 'prefix'}
        self.assertEqual(['## <a name="post_prefix_my_url"></a> Post prefix/my/url'], handle_line('@Post("/my/url")', context, LINE_HANDLERS))

    def test_handle_http_method_with_empty_string(self):
        context = {'url_prefix': 'prefix'}
        self.assertEqual(['## <a name="post_prefix"></a> Post prefix'], handle_line('@Post()', context, LINE_HANDLERS))

    def test_handle_http_method_with_javadoc_lines(self):
        context = {'javadoc': 'false','javadoc_lines': ['line 1', 'line 2'], 'url_prefix': ''}
        self.assertEqual(['## <a name="post__my_url"></a> Post /my/url', 'line 1', 'line 2'], handle_line('@Post("/my/url")', context, LINE_HANDLERS))
        self.assertEqual({'javadoc': 'false', 'url_prefix': ''}, context)

    def test_handle_line_with_param(self):
        context = {'javadoc': 'false', 'url_prefix': ''}
        self.assertEqual(['## <a name="get_url_with__param"></a> Get url/with/:param'], handle_line('@Get("url/with/:param")', context, LINE_HANDLERS))

    def test_handle_line_with_context_property(self):
        context = {'javadoc': 'false', 'url_prefix': 'pre/fix/'}
        self.assertEqual(['## <a name="get_pre_fix_url"></a> Get pre/fix/url'], handle_line('@Get("url")', context, LINE_HANDLERS))

    def test_handle_line_save_into_context(self):
        context = dict()
        self.assertEqual(['# <a name="prefix"></a>prefix'], handle_line('@Prefix("prefix")', context, LINE_HANDLERS))
        self.assertEqual({'url_prefix': 'prefix'}, context)

    def test_handle_line_javadoc_begin(self):
        context = dict()
        self.assertEqual([], handle_line('/**', context, LINE_HANDLERS))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': []}, context)

    def test_handle_line_javadoc_end(self):
        context = {'javadoc': 'true'}
        self.assertEqual([], handle_line('*/', context, LINE_HANDLERS))
        self.assertEqual({'javadoc': 'false'}, context)

    def test_handle_line_javadoc(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('* this is javadoc comment', context, LINE_HANDLERS))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['this is javadoc comment']}, context)

    def test_handle_line_javadoc_parameter(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('* @param name parameter name', context, LINE_HANDLERS))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['* **Parameter** name parameter name']}, context)

    def test_handle_line_javadoc_with_variable(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('* a line with {data}', context, LINE_HANDLERS))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['a line with {data}']}, context)

    def test_handle_line_javadoc_return(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('* @return object returned', context, LINE_HANDLERS))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['* **Return** object returned']}, context)

    def test_handle_javadoc_line_with_command_line(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('* $(echo "hello world"| sed "s/ /\\n/")', context, LINE_HANDLERS))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['```', 'echo "hello world"| sed "s/ /\\n/"', 'hello', 'world', '```']}, context)

    def test_handle_javadoc_line_with_failing_command(self):
        context = {'javadoc': 'true', 'javadoc_lines': []}
        self.assertEqual([], handle_line('* $(unknown_command)', context, LINE_HANDLERS))
        self.assertEqual({'javadoc': 'true', 'javadoc_lines': ['```', 'unknown_command', '', '```']}, context)

    def test_generate_toc_line(self):
        context = {'url_prefix': '/prefix'}
        self.assertEqual(["  - [Post /prefix/my/url](#post__prefix_my_url)"], handle_line('@Post("/my/url")', context, TOC_LINE_HANDLERS))

    def test_generate_toc_line_empty_string(self):
        context = {'url_prefix': '/prefix'}
        self.assertEqual(["  - [Post /prefix](#post__prefix)"], handle_line('@Post()', context, TOC_LINE_HANDLERS))