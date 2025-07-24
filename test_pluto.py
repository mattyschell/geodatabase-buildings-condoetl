import os
import unittest
import pathlib

import pluto


class PlutoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.teardowntestdata = 'Y'

        self.datadirectory = os.path.join(pathlib.Path(__file__).parent
                                         ,'data'
                                         ,'testdata')

        self.testpluto = pluto.Pluto(self.datadirectory)


    @classmethod
    def tearDownClass(self):

        if self.teardowntestdata == 'Y':

            self.testpluto.cleanallfiles()
        

    def test_adownload(self):

        self.testpluto.download()
        self.assertTrue(pathlib.Path(self.testpluto.plutocsv).is_file())

    def test_bextractbbls(self):

        self.testpluto.extractbbls()
        self.assertTrue(pathlib.Path(self.testpluto.plutobbls).is_file())

    def test_cextractcondosql(self):

        self.testpluto.extractcondosql()
        self.assertTrue(pathlib.Path(self.testpluto.condosqls).is_file())

    def test_dbadplutoerrors(self):

        os.environ['PLUTOVERSION'] = 'BADPLUTOVERSION'
        self.testpluto = pluto.Pluto(self.datadirectory)

        with self.assertRaises(RuntimeError) as context:
            self.testpluto.download()
    
if __name__ == '__main__':
    unittest.main()
