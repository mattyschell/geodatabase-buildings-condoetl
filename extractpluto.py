import os
import logging
import time
import pathlib

import pluto


def main(outputdir):

        sourcepluto = pluto.Pluto(outputdir)

        # drop sql into \data directory 
        # return kount of condos in pluto, around 10k
        return sourcepluto.downloadextractcondosql() 


if __name__ == '__main__':
   
    timestr = time.strftime("%Y%m%d-%H%M%S")

    try:
        targetlog = os.path.join(os.environ['TARGETLOGDIR'] 
                                ,'extractpluto-{0}.log'.format(timestr)) 
    except:
        targetlog = os.path.join(os.getcwd() 
                                ,'extractpluto-{0}.log'.format(timestr))

    logging.basicConfig(filename=targetlog
                       ,level=logging.INFO)

    try:
        plutoversiontest = os.environ['PLUTOVERSION']
    except:
        logging.error('Pluto module requires environmental PLUTOVERSION set (ex 21V1)')
        raise ValueError('Pluto module requires environmental PLUTOVERSION set (ex 21V1)')

    datadir = os.path.join(pathlib.Path(__file__).parent
                          ,'data')

    kount = main(datadir)

    if (kount == 0 or kount is None):
        logging.error('Failed to extract any pluto condo bbls')
        retval = 1
    else:
        logging.info('Successfully extracted {0} pluto condo bbls to \data directory'.format(kount))
        retval = 0

    exit(retval)