
from linregression import *

def test_1(max_try = 0, max_iter = 1000):
    a = [ [1, 0, 0] for _ in range(20) ]
    b = [ [2, 1, 0] for _ in range(40) ]
    c = [ [0, 0, 4] for _ in range(20) ]
    d = [ [randint(3, 8), randint(0, 8), randint(0, 8)] ]
    
    exs = {
      2: a,
      4: b,
      8: c,
      0: d
      }
    
    opts  = ga.default_options(200, 4, Mutate_Stdev = 0.1)
    res   = minimize_linregr(exs, sq_error, 0.01, max_try, max_iter, opts)
    
    print "Result:"
    print res
    print 
    
    if res['success']:
        return [ linregr_f(coefs) for (coefs,_) in res['result']]