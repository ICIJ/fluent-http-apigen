from unittest import TestCase

from apigen import handle_line


class TestApigen(TestCase):
    def test_handle_empty_doc(self):
        self.assertIsNone(handle_line('a line', {}, {r'not matching': r''}))

    def test_handle_line(self):
        self.assertEqual('# Post /my/url', handle_line('@Post("/my/url")\n', {}, {r'@(\w+)\("([a-z/]+)".*': r'# \1 \2'}))

    def test_handle_line_with_param(self):
        self.assertEqual('# Get url/with/:param', handle_line('@Get("url/with/:param")\n', {}, {r'@(\w+)\("([a-z/:]+)".*': r'# \1 \2'}))

    def test_handle_line_with_prefix(self):
        self.assertEqual('# Get pre/fix/url', handle_line('@Get("url")\n', {'url_prefix': 'pre/fix/'},{r'@(\w+)\("([a-z/:]+)".*': r'# \1 {url_prefix}\2'}))

    def test_handle_prefix_line(self):
        context = dict()
        self.assertIsNone(handle_line('@Prefix("prefix")\n', context, {r'@Prefix\("([a-z/]+)".*': 'context[url_prefix]'}))
        self.assertEqual({'url_prefix': 'prefix'}, context)