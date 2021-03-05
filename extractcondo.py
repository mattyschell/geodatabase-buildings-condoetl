import sys
import os
import logging
import time
import pathlib
import arcpy
import csv

def main(sourcesdeconn
        ,outputdir):

    # https://pro.arcgis.com/en/pro-app/latest/tool-reference/conversion/table-to-table.htm

    condotable = os.path.join(sourcesdeconn, 'DOF_TAXMAP.Condo')
    condocsv = os.path.join(outputdir,'condo.csv')

    # https://pro.arcgis.com/en/pro-app/latest/arcpy/classes/fieldmappings.htm
    # how many lines does it take to declare SELECT column1, column2 from X?
    fms = arcpy.FieldMappings()
    fm_base_bbl = arcpy.FieldMap()
    fm_billing_bbl = arcpy.FieldMap()
    fm_base_bbl.addInputField(condotable, 'CONDO_BASE_BBL')
    fm_billing_bbl.addInputField(condotable, 'CONDO_BILLING_BBL')

    base_bbl_name = fm_base_bbl.outputField
    base_bbl_name.name = 'CONDO_BASE_BBL'
    fm_base_bbl.outputField = base_bbl_name

    billing_bbl_name = fm_billing_bbl.outputField
    billing_bbl_name.name = 'CONDO_BILLING_BBL'
    fm_billing_bbl.outputField = billing_bbl_name

    fms.addFieldMap(fm_base_bbl)
    fms.addFieldMap(fm_billing_bbl)
    # 13?

    if os.path.exists(condocsv):
        os.remove(condocsv)

    arcpy.conversion.TableToTable(condotable
                                 ,outputdir
                                 ,'condo.csv'
                                 ,"""CONDO_BASE_BBL IS NOT NULL AND CONDO_BILLING_BBL IS NOT NULL"""
                                 ,fms)

    with open(condocsv, newline='') as csvfile:
        condocsvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        csvkount = sum(1 for row in condocsvreader)
    
    return (csvkount - 1)


if __name__ == '__main__':

    psourcesdeconn = os.environ['SDEFILE']
        
    timestr = time.strftime("%Y%m%d-%H%M%S")

    if locals().get('TARGETLOGDIR'):
        targetlog = os.path.join(os.environ['TARGETLOGDIR'] 
                                ,'extractcondo-{0}.log'.format(timestr)) 
    else:
        targetlog = os.path.join(os.getcwd() 
                                ,'extractcondo-{0}.log'.format(timestr))

    logging.basicConfig(filename=targetlog
                       ,level=logging.INFO)

    datadir = os.path.join(pathlib.Path(__file__).parent
                          ,'data')

    kount = main(psourcesdeconn
                ,datadir)

    # at this point our csv still has two bad duplicate types
    # condo_base_bbl condo_billing_bbl
    #      A               X
    #      A               X
    #      B               Y
    #      B               Z

    if (kount == 0 or kount is None):
        logging.error('Failed to extract any condos')
    else:
        logging.info('Successfully extracted {0} bbls to data directory'.format(kount))