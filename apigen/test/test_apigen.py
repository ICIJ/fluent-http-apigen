from unittest import TestCase

from apigen import handle_line


class TestApigen(TestCase):
    def test_handle_empty_doc(self):
        self.assertIsNone(handle_line('a line', None, {r'not matching': r''}))

    def test_handle_line(self):
        self.assertEqual(handle_line('@Post("/my/url")\n', None, {r'@(\w+)\("([a-z/]+)".*': r'# \1 \2'}), '# Post /my/url')

    def test_handle_line_with_param(self):
        self.assertEqual(handle_line('@Get("url/with/:param")\n', None, {r'@(\w+)\("([a-z/:]+)".*': r'# \1 \2'}), '# Get url/with/:param')
