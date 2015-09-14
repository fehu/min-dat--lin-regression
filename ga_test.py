import ga

def ga_test_1():
    print "Minimizing with fitness: (10 - x ** 2) ** 2"
    fit_f = lambda (x,): (10 - x ** 2) ** 2
    opts  = ga.ga_default_options(200, 1)
    res   = ga.ga(fit_f, 0.00001, 1000, opts)
    print "Result:"
    print res
    
def ga_test_2():
    print "Minimizing with fitness: x ** 2 + (y - 4) ** 2"
    fit_f = lambda (x, y): x ** 2 + (y - 4) ** 2
    opts  = ga.ga_default_options(200, 2)
    res   = ga.ga(fit_f, 0.00001, 1000, opts)
    print "Result:"
    print res
