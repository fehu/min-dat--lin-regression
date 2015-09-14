
import sys

from linregression import *
from read_weka_data import *
from utils import *

#filename = sys.argv[1]
#expected = sys.argv[2]

def read_and_minumize_linreger(filename, expected):
    weka_read  = read_weka_numeric_data(filename)
    weka_attrs = weka_read['attributes']

    if expected in weka_attrs:
        expected_ind = weka_attrs.index(expected)
    else:
        error("not found attribute " + expected)

    weka_data = weka_read['data']
    data = {}

    for row in weka_data:
        exp = row.pop(expected_ind)
        if exp in data:
            old = data[exp]
            old.append(row)
        else:
            data[exp] = [row]

    #print data

    max_try    = 3
    max_iter   = 2000
    target_err = 800000 # 100

    opts  = ga.default_options(200, len(weka_attrs), Mutate_Stdev = 0.1)
    res   = minimize_linregr(data, sq_error, target_err, max_try, max_iter, opts)

    print "Result:"
    print res
    print 
    
    return res