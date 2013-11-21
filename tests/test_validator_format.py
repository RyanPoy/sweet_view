#coding: utf8

# The MIT License (MIT)
#
# Copyright (c) 2013 PengYi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from pyrails.activerecord import FormatValidator
import unittest


class FormatValidatorTest(unittest.TestCase):

    def test_foramt_with(self):
        self.assertTrue(FormatValidator().validate('abc.abc.abc.', '[(\w+)/.]{3}'))  

    def test_not_format_with(self):
        self.assertFalse(FormatValidator().validate('aba', '\d+'))
    
    def test_format_should_return_false_if_value_is_none_and_disallow_null(self):
        self.assertFalse(FormatValidator().validate(None, allow_null = False))
        
    def test_format_should_return_true_if_value_is_none_and_allow_null(self):
        self.assertTrue(FormatValidator().validate(None, allow_null = True))

    def test_format_should_return_result_which_depends_with_if_value_is_blank_and_disallow_blank(self):
        self.assertFalse(FormatValidator().validate('     ', **{'_with': '\d+', 'allow_blank': False}))
        self.assertTrue(FormatValidator().validate('     ', **{'_with': '\s+', 'allow_blank': False}))

    def test_format_should_return_false_if_value_is_blank_and_allow_blank(self):
        self.assertRaises(TypeError, FormatValidator().validate, '     ', **{'allow_blank': False})


if __name__ == '__main__':
    unittest.main()