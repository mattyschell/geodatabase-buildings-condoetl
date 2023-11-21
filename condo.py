import os
import posixpath
import arcpy
import csv

class Condo(object):

    def __init__(self):

        if os.path.exists(os.environ['SDEFILE']):

            self.sdeconn = os.environ['SDEFILE']

        elif os.environ['SDEFILE'].startswith('http'):

            # should have followed the wisdom of the ancients
            # and simply called SDEFILE "the containah" 

            self.sdeconn = r"{0}".format(os.environ['SDEFILE'])
            # force a url / here, dont let os.path manage below
            self.sdeconn = posixpath.join(self.sdeconn,'')
 
        else:

            raise ValueError('{0} is not a valid sde file'.format(os.environ['SDEFILE']))

    def getsimplefieldmap(self
                         ,fields):
                       
        # our source is a versioned geodatabase with no SQL access
        # https://pro.arcgis.com/en/pro-app/latest/arcpy/classes/fieldmappings.htm
        fms = arcpy.FieldMappings()
        
        for field in fields:
            fm_field = arcpy.FieldMap()
            fm_field.addInputField(self.condotable, field)
            fm_field_out = fm_field.outputField
            fm_field_out.name = field
            fm_field.outputField = fm_field_out
            fms.addFieldMap(fm_field)

        return fms

    def countcondos(self):

        with open(self.condocsv, newline='') as csvfile:
            condocsvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            csvkount = sum(1 for row in condocsvreader)
    
        return (csvkount - 1)

    def extracttofile(self
                     ,sourcetable
                     ,targetdirectory
                     ,targetname='condo.csv'):

        self.condotable = os.path.join(self.sdeconn
                                      ,sourcetable)
        
        #print("condotable joined is {0}".format(self.condotable))

        self.condocsv = os.path.join(targetdirectory
                                    ,targetname)

        if os.path.exists(self.condocsv):
            os.remove(self.condocsv)

        # https://pro.arcgis.com/en/pro-app/latest/tool-reference/conversion/table-to-table.htm
        arcpy.conversion.TableToTable(self.condotable
                                     ,targetdirectory
                                     ,targetname
                                     ,"""CONDO_BASE_BBL IS NOT NULL AND CONDO_BILLING_BBL IS NOT NULL"""
                                     ,self.getsimplefieldmap(['CONDO_BASE_BBL','CONDO_BILLING_BBL']))
