
#import sys

from linregression import *
from read_weka_data import *
from utils import *

#filename = sys.argv[1]
#expected = sys.argv[2]


def read_and_minumize_linreger(filename, expected, Drop_Attributes = []):
    weka_read  = read_weka_numeric_data(filename)
    weka_attrs = weka_read['attributes']
    weka_data  = weka_read['data']
    
    drop_ind = map(weka_attrs.index, Drop_Attributes)
    drop_ind.sort(reverse=True)
    
    for i in drop_ind: weka_attrs.pop(i)
    
    for row in weka_data:
        for i in drop_ind: 
            row.pop(i)
    

    if expected in weka_attrs:
        expected_ind = weka_attrs.index(expected)
    else:
        error("not found attribute " + expected)
    data = {}

    for row in weka_data:
        exp = row.pop(expected_ind)
        if exp in data:
            old = data[exp]
            old.append(row)
        else:
            data[exp] = [row]

    

    #print data

    stall_precision    = 1 #1e-5
    max_stalled_in_row = 100
    max_iter           = 10000 #1000
    population_size    = 800 # 200

    opts  = ga.default_options(population_size, len(weka_attrs), Mutate_Stdev = 0.5) # 0.1 # 1
    res   = minimize_linregr(data, sq_error, stall_precision, max_stalled_in_row, opts, max_iter)

    print "Result:"
    print res[0]
    print 
    
    return res + (data, )
    #return data