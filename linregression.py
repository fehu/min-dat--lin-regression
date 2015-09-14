# -*- coding: utf-8 -*-

import operator as op
from random import randint

from utils import *
import ga


def linregr(coefs, xs): 
    assert( len(xs) == len(coefs) - 1 )
    weighted_xs_t = map(lambda (x,y): x*y, zip(xs, tail(coefs)))
    return reduce(op.add, weighted_xs_t, head(coefs))

  
def linregr_f(coefs): return lambda xs: linregr(coefs, xs)


def sq_error(result, expected): 
    return (expected - result) ** 2
  


def minimize_linregr(expected_xs_dict, err_func, target_err, max_tries, max_iterations, ga_options):
    error_f = lambda coefs: sum([ err_func(linregr(coefs, xs), expected) 
                                    for expected, xss in expected_xs_dict.iteritems() 
                                    for xs in xss
                                ])
    return ga.minimize(error_f, target_err, max_iterations, ga_options, max_tries)
 
