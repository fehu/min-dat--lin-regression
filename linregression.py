# -*- coding: utf-8 -*-

import operator as op

def linregr(coefs, xs): 
    assert( len(xs) == len(coefs) - 1 )
    weighted_xs_t = map(op.mul, zip(xs, tail(coefs)))
    return reduce(op.add, weighted_xs_t, head(coefs))

    #return head(coefs) + sum(map(op.mul, zip(xs, tail(coefs))))
    #
  
def sq_error(result, expected): 
    return (expected - result) ** 2
  


def minimize_linregr(regr_coefs, expected_xs_dict, err_func):
    error_f = lambda coefs: sum([ err_func(linregr(coefs, xs), expected) 
                                   for expected, xs in iteritems(expected_xs_dict) 
                                ])
 
def minimize(func, params):
    return 1
  
  
def head(l): return l[0]
def tail(l): return l[1:]