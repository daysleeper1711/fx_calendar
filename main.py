from datetime import datetime
from feed import *

import json

def run():
    try:
        print('-------START FEEDING----------')
        t_start = datetime.now()
        print('')
        # get current year
        currentYear = datetime.today().isocalendar()[0]
        startYear = 2010
        rangeOfYear = currentYear - 2010
        for i in range(rangeOfYear + 1):
            year = startYear + i
            fn = 'data/' + str(year) + '.json'
            print('Info: create file ', fn)
            with open(fn,'w') as f:
                print('Info: writting data to file...')
                json.dump(toJson(eventsInYear(year)),f)
            print('Info: finished file ', fn)
            print()
        t_end = datetime.now()
        t_consumed = (t_end - t_start).resolution
        print(f'Info: time consumed {t_consumed}')
        print('-------END-------------')
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly, but may be overridden in exception subclasses
        x, y = inst.args     # unpack args
        print('x =', x)
        print('y =', y)
        return -1

if __name__ == "__main__":
    run() #test