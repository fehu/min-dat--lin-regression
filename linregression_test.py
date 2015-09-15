
from linregression import *

def test_1(max_iter = None):
    a = [ [1, 0, 0] for _ in range(20) ]
    b = [ [2, 1, 0] for _ in range(40) ]
    c = [ [0, 0, 4] for _ in range(20) ]
    d = [ [0, 0, 8] for _ in range(5) ] + \
        [ [0, 1, 7] for _ in range(5) ]
    #e = [ [7, 0, 0] for _ in range(5) ] + \
        #[ [0, 7, 0] for _ in range(5) ]
      
    #d = [ [randint(3, 8), randint(0, 8), randint(0, 8)] for _ in range(10) ]
    
    exs = {
      2:  a,
      4:  b,
      8:  c,
      16: d
      #30: e
      }
    
    #exs = {
      #2:  a,
      #4:  b,
      #8:  c,
      #16: d,
      #32: e
      #}
      
    #exs = {
      #1:   a,
      #10:  b,
      #1e2: c,
      #1e3: d,
      #1e4: e
      #}
    
    opts  = ga.default_options(200, 4, Mutate_Stdev = 0.1)
    res   = minimize_linregr(exs, sq_error, 1e-10, 200, opts, max_iter, test_classification=True)
    
    print "Result:"
    print res
    print 
    
    return res