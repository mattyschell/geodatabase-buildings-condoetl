import os
import unittest
import pathlib

import condo

class CondoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.teardowntestdata = 'Y'

        # mock the SDE environmental ala
        #C:\matt_projects\geodatabase-buildings-condoetl\data\testdata\testdata.gdb\Condo
        self.datadirectory = os.path.join(pathlib.Path(__file__).parent
                                         ,'data'
                                         ,'testdata')
        self.testgeodatabase = os.path.join(os.path.abspath(self.datadirectory)
                                           ,'testdata.gdb')  
        self.badgeodatabase = os.path.join(os.path.abspath(self.datadirectory)
                                          ,'doesnotexist.gdb')        
        self.testtable = 'Condo'

        # we are unit testing with the real production service
        # seems bad!
        self.testhostedurl   = "https://services6.arcgis.com/yG5s3afENB5iO9fj/arcgis/rest/services/v_PIP_SCAR_Tables_view/FeatureServer/"
        self.testhostedurl2  = self.testhostedurl.rstrip('/')
        self.testhostedlayer = '1'

    @classmethod
    def tearDownClass(self):
        
        if self.teardowntestdata == 'Y':

            os.remove(os.path.join(self.datadirectory
                                  ,'condo.csv'))

            os.remove(os.path.join(self.datadirectory
                                  ,'condo.csv.xml'))
    
    def test_abadsde(self):

        os.environ["SDEFILE"] = self.badgeodatabase

        badgdb = False

        try:
            self.testcondo = condo.Condo()
        except:
            badgdb = True

        self.assertTrue(badgdb)

    def test_bextract(self):

        os.environ["SDEFILE"] = self.testgeodatabase
        self.testcondo = condo.Condo()

        self.testcondo.extracttofile(self.testtable
                                    ,self.datadirectory)

        self.assertEqual(self.testcondo.countcondos(), 5)

    def test_cextracthostedcondo(self):

        # mimic expected x:\path\database.sde\table 
        # with https:\pathtoservice\layer\
        os.environ["SDEFILE"] = self.testhostedurl
        self.testcondo = condo.Condo()

        self.testcondo.extracttofile(self.testhostedlayer
                                    ,self.datadirectory)
        
        self.assertGreater(self.testcondo.countcondos(), 0)

    def test_dextracthostedcondo2(self):

        # mimic expected x:\path\database.sde\table 
        # with https:\pathtoservice\layer
        # no closing slash
        os.environ["SDEFILE"] = self.testhostedurl2
        self.testcondo = condo.Condo()

        self.testcondo.extracttofile(self.testhostedlayer
                                    ,self.datadirectory)
        
        self.assertGreater(self.testcondo.countcondos(), 0)


if __name__ == '__main__':
    unittest.main()
