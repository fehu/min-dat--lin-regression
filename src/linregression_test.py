
from linregression import *



test_1_a = [ [1, 0, 0] for _ in range(20) ]
test_1_b = [ [2, 1, 0] for _ in range(40) ]
test_1_c = [ [0, 0, 4] for _ in range(20) ]
test_1_d = [ [0, 0, 8] for _ in range(5) ] + \
           [ [0, 1, 7] for _ in range(5) ]

test_1_exs_1 = {
                1: test_1_a,
                2: test_1_b,
                3: test_1_c,
                4: test_1_d
              }

test_1_exs_2 = {
                2:  test_1_a,
                4:  test_1_b,
                8:  test_1_c,
                16: test_1_d
              }

def test_1(exs):
    opts  = ga.default_options(200, 4, Mutate_Stdev = 1, Mutate_Shrink_Stdev = 0.1, Max_Generations = 5000)
    res   = minimize_linregr(exs, sq_error, 1e-5, 200, opts, test_classification=True)
    
    print "="*30
    print 
    print_minimize_linregr_result(res)
    print 
    
    return res

def test_1_1(): return test_1(test_1_exs_1)
def test_1_2(): return test_1(test_1_exs_2)
  







test_2_e_1 = [ [7, 0, 0] for _ in range(5) ] + \
             [ [0, 7, 0] for _ in range(5) ]        



test_2_e_2 = [ [7, 7, 0] for _ in range(5) ] + \
             [ [4, 7, 4] for _ in range(5) ]


def test_2(e):
    exs = {
      2:  test_1_a,
      4:  test_1_b,
      8:  test_1_c,
      16: test_1_d,
      32: e,
      }

    opts  = ga.default_options(400, 4, Mutate_Stdev = 1, Mutate_Shrink_Stdev = 0.1, Max_Generations = 5000)
    res   = minimize_linregr(exs, sq_error, 1e-10, 200, opts, test_classification=True)
    
    print "="*30
    print 
    print_minimize_linregr_result(res)
    print 
    
    return res
  
def test_2_1(): return test_2(test_2_e_1)
def test_2_2(): return test_2(test_2_e_2)
 