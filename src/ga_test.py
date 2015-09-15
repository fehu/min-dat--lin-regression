import ga

def _print_1():
    print "Minimizing with fitness: (x + 10) ** 2"

_fit_f_1 = lambda (x,): (x - 10) ** 2
_opts_1  = ga.default_options(200, 1)

def ga_test_1():
    _print_1()
    res = ga.minimize_to_target(_fit_f_1, 0.00001, 1000, _opts_1)
    print "Result:"
    print res
    
def ga_test_s_1():
    _print_1()
    res = ga.minimize_until_stall(_fit_f_1, 1e-5, 40, _opts_1) # fitness_func, stall_precision, options, max_iter = None)
    print "Result:"
    print res
    
    
    



def _print_2():
    print "Minimizing with fitness: x ** 2 + (y - 4) ** 2"

_fit_f_2 = lambda (x, y): x ** 2 + (y - 4) ** 2
_opts_2  = ga.default_options(200, 2)
    
    
def ga_test_2():
    _print_2()
    res   = ga.minimize_to_target(_fit_f_2, 0.00001, 1000, _opts_2)
    print "Result:"
    print res

def ga_test_s_2():
    _print_2()
    res   = ga.minimize_until_stall(_fit_f_2, 1e-5, 40, _opts_2)
    print "Result:"
    print res
