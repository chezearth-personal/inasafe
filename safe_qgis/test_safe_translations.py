"""
InaSAFE Disaster risk assessment tool developed by AusAid -
 **Safe Translations Test .**

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'ismailsunni@yahoo.co.id'
__version__ = '0.5.1'
__date__ = '12/10/2011'
__copyright__ = ('Copyright 2012, Australia Indonesia Facility for '
                 'Disaster Reduction')
import unittest
import os
from safe_interface import safeTr, getFunctionTitle, get_plugins


class SafeTranslationsTest(unittest.TestCase):

    def setUp(self):
        if 'LANG' in os.environ.iterkeys():
            os.environ.__delitem__('LANG')

    def tearDown(self):
        if 'LANG' in os.environ.iterkeys():
            os.environ.__delitem__('LANG')

    def testDynamicTranslationFunctionTitle(self):
        """Test for dynamic translations for function title
        """

        plugins_dict = get_plugins()
        myPluginName = 'Volcano Building Impact'
        myMessage = '%s not found in %s' % (myPluginName, str(plugins_dict))
        assert myPluginName in plugins_dict, myMessage
        func = plugins_dict[myPluginName]

        # English
        func_title = getFunctionTitle(func)
        expected_title = 'Be affected'
        msg = 'expected %s but got %s' % (expected_title, func_title)
        assert func_title == expected_title, msg

        # Indonesia
        os.environ['LANG'] = 'id'
        func_title = getFunctionTitle(func)
        expected_title = 'Terkena dampak'
        msg = ('expected %s but got %s, in lang = %s'
               % (expected_title, func_title, os.environ['LANG']))
        assert expected_title == func_title, msg

    def testDynamicTranslation(self):
        """Test for dynamic translations for a string
        """

        # English
        func_title = 'Be affected'
        expected_title = 'Be affected'
        assert func_title == expected_title

        # Indonesia
        os.environ['LANG'] = 'id'
        func_title = 'Be affected'
        real_title = safeTr(func_title)
        expected_title = 'Terkena dampak'
        msg = 'expected %s but got %s' % (expected_title, real_title)
        assert expected_title == real_title, msg

if __name__ == "__main__":
    suite = unittest.makeSuite(SafeTranslationsTest, 'test')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)