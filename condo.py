import os
import arcpy
import csv

class Condo(object):

    def __init__(self):

        self.sdeconn = os.environ['SDEFILE']

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
                     ,targetname):

        self.condotable = os.path.join(self.sdeconn
                                      ,sourcetable)

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
        