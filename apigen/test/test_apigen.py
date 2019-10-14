from unittest import TestCase

from apigen import handle_line


class TestApigen(TestCase):
    def test_handle_empty_doc(self):
        context = {'javadoc': 'false'}
        self.assertIsNone(handle_line('a line', context, {r'not matching': r''}))

    def test_handle_line(self):
        context = {'javadoc': 'false'}
        self.assertEqual('# Post /my/url', handle_line('@Post("/my/url")\n', context, {r'@(\w+)\("([a-z/]+)".*': r'# \1 \2'}))

    def test_handle_line_with_param(self):
        context = {'javadoc': 'false'}
        self.assertEqual('# Get url/with/:param', handle_line('@Get("url/with/:param")\n',context, {r'@(\w+)\("([a-z/:]+)".*': r'# \1 \2'}))

    def test_handle_line_with_prefix(self):
        context = {'javadoc': 'false',
                   'url_prefix': 'pre/fix/'}
        self.assertEqual('# Get pre/fix/url', handle_line('@Get("url")\n', context, {r'@(\w+)\("([a-z/:]+)".*': r'# \1 {url_prefix}\2'}))

    def test_handle_prefix_line(self):
        context = {'javadoc': 'false'}
        self.assertIsNone(handle_line('@Prefix("prefix")\n', context, {r'@Prefix\("([a-z/]+)".*': 'context[url_prefix]'}))
        self.assertEqual({'javadoc': 'false', 'url_prefix': 'prefix'}, context)

    def test_handle_line_javadoc_begin(self):
       context=dict()
       self.assertEqual('first line comment', handle_line('/**first line comment \n', context, dict()))
       self.assertEqual({'javadoc': 'true'}, context)

    def test_handle_line_javadoc_end(self):
        context = {'javadoc': 'true'}
        self.assertEqual('last line comment' , handle_line('last line comment*/ \n', context, dict()))
        self.assertEqual({'javadoc': 'false'}, context)

    def test_handle_line_javadoc(self):
        context = {'javadoc': 'true'}
        self.assertEqual('this is javadoc comment', handle_line('* this is javadoc comment', context, dict()))
        self.assertEqual({'javadoc': 'true'}, context)

    def test_handle_line_javadoc_parameter(self):
        context = {'javadoc': 'true'}
        self.assertEqual('**Parameter** name parameter name', handle_line('* @param name parameter name', context, dict()))
        self.assertEqual({'javadoc': 'true'}, context)

    def test_handle_line_javadoc_return(self):
        context = {'javadoc': 'true'}
        self.assertEqual('**Return** object returned', handle_line('* @return object returned', context, dict()))
        self.assertEqual({'javadoc': 'true'}, context)