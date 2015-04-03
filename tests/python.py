#!/usr/bin/env python3

#
#
#
import unittest

import sys
print(" Running Python Version [%s] " % sys.version)

class TestMain(unittest.TestCase):

    def setUp(self):
        from saveme.api import CommandLine
        self._cl = CommandLine()

    def test_cli_go(self):
        self.assertEqual( self._cl.go(["me"]), 12)

    def test_cli_help(self):
        self.assertEqual( self._cl.help(), True)


class TestUtil(unittest.TestCase):

    _parsedate = None
    
    def setUp(self):
        from saveme.main import culltimeline
        from saveme.external import parsedate
        self._parsedate = parsedate
        self._culltimeline = culltimeline

    def test_util_parsedate(self):
        # date '+%Y%m%d_%H:%M:%S_%z'
        self.assertEqual( self._parsedate('20150329_23:35:41_-0400'), 1427686541)


    def test_util_culltimeline(self):
        # date '+%Y%m%d_%H:%M:%S_%z'
        from saveme.main import culltimeline as _culltimeline
        import pdb
        #pdb.set_trace()
        self.assertEqual(_culltimeline(['20150329_23:35:41_-0400'],
                                       "0-1dy: all, 1dy-1wk: 4hr, 1wk-12wk: 1wk, 12wk-1yr: 4wk, 1yr+: none",
                                       1427690151), [] )
        self.assertEqual(_culltimeline(['20150329_23:35:41_-0400','20150301_23:35:41_-0400','20150201_23:35:41_-0400'],
                                       "0-1dy: all, 1dy-1wk: 4hr, 1wk-12wk: 1wk, 12wk-1yr: 4wk, 1yr+: none",
                                       1427690151), [] )
        self.assertEqual(_culltimeline(['20150329_23:35:41_-0400','20150329_23:30:41_-0400','20150329_23:25:41_-0400'],
                                       "0-1dy: 1hr,1dy-1wk: 2hr, 1yr+: none",
                                       1427690151), ['20150329_23:35:41_-0400', '20150329_23:30:41_-0400'] )

        self.assertEqual(_culltimeline(["20150329_21:56:37_-0400","20150402_02:21:14_-0400","20150402_20:39:11_-0400"],
                                       "0-1yr: 1dy",
                                       1428021888), ['20150402_20:39:11_-0400'] )

class TestExternal(unittest.TestCase):
    def setUp(self):
        pass

    def test_external_runcommand(self):
        from saveme.main import runcommand as _runcommand
        self.assertEqual(_runcommand(["/bin/bash","-c", "echo stdout\necho stderr 1>&2\nexit 3"]),(3, 'stdout\n', 'stderr\n'))
        pass

    def test_external_runcommand_stdin(self):
        from saveme.main import runcommand as _runcommand
        self.assertEqual(_runcommand(["/bin/bash","-c", "tac\necho stderr 1>&2\nexit 3"],stdin="stdin\nfrom\n"),(3, 'from\nstdin\n', 'stderr\n'))
        pass

if __name__ == '__main__':
    import sys,os
    sys.path += [ os.path.abspath(os.path.dirname(sys.argv[0])  + "/../lib") ]
    unittest.main()
