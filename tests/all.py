# coding: utf8
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import logging
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s [%(levelname)s]: %(message)s",
)

import unittest

from tests.unit.test_template_basic import TestTemplateBasic
from tests.unit.test_template_complex import TestTemplateComplex
from tests.unit.test_template_extends import TestTemplateExtends
from tests.unit.test_template_for import TestTemplateFor
from tests.unit.test_template_if import TestTemplateIf
from tests.unit.test_template_include import TestTemplateInclude
from tests.unit.test_template_loader import TestTemplateLoader
from tests.unit.test_template_using import TestTemplateUsing

from tests.unit.test_form import TestForm
from tests.unit.test_form_button import TestFormButton
from tests.unit.test_form_checkbox import TestFormCheckbox
from tests.unit.test_form_color import TestFormColor
from tests.unit.test_form_date import TestFormDate
from tests.unit.test_form_datetime import TestFormDatetime
from tests.unit.test_form_email import TestFormEmail
from tests.unit.test_form_file import TestFormFile
from tests.unit.test_form_hidden import TestFormHidden
from tests.unit.test_form_label import TestFormLabel
from tests.unit.test_form_month import TestFormMonth
from tests.unit.test_form_number import TestFormNumber
from tests.unit.test_form_password import TestFormPassword
from tests.unit.test_form_radio import TestFormRadio
from tests.unit.test_form_range import TestFormRange
from tests.unit.test_form_search import TestFormSearch
from tests.unit.test_form_submit import TestFormSubmit
from tests.unit.test_form_tel import TestFormTel
from tests.unit.test_form_text import TestFormText
from tests.unit.test_form_textarea import TestFormTextarea
from tests.unit.test_form_time import TestFormTime
from tests.unit.test_form_url import TestFormUrl
from tests.unit.test_form_week import TestFormWeek


# template unit tests
unit_tests = [
    TestTemplateExtends,
    TestTemplateBasic,
    TestTemplateComplex,
    TestTemplateFor,
    TestTemplateIf,
    TestTemplateInclude,
    TestTemplateLoader,
    TestTemplateUsing,
]

# form tests
unit_tests += [
    TestForm,
    TestFormButton,
    TestFormCheckbox,
    TestFormColor,
    TestFormDate,
    TestFormDatetime,
    TestFormEmail,
    TestFormFile,
    TestFormHidden,
    TestFormLabel,
    TestFormMonth,
    TestFormNumber,
    TestFormPassword,
    TestFormRadio,
    TestFormRange,
    TestFormSearch,
    TestFormSubmit,
    TestFormTel,
    TestFormText,
    TestFormTextarea,
    TestFormTime,
    TestFormUrl,
    TestFormWeek,
]

integration_tests = [
]


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) == 2 else 'all'
    if cmd not in ('all', 'unit', 'integration'):
        print ('python %s [all|unit|integration]' % sys.argv[0])
        sys.exit(-1)

    suite = unittest.TestSuite()
    if cmd == 'all' or cmd == 'unit':
        for t in unit_tests:
            suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(t))
    if cmd == 'all' or cmd == 'integration':
        for t in integration_tests:
            suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(t))

    unittest.TextTestRunner().run(suite)
