# -*- coding: utf-8 -*-

import operator as op
from random import randint

from utils import *
import ga


def linregr(coefs, xs): 
    assert( len(xs) == len(coefs) - 1 )
    weighted_xs_t = map(tupled(op.mul), zip(xs, tail(coefs)))
    return reduce(op.add, weighted_xs_t, head(coefs))

  
#def linregr_f(coefs): return lambda xs: linregr(coefs, xs)


def sq_error(result, expected): 
    return (expected - result) ** 2
  


def minimize_linregr(expected_xs_dict, err_func, stall_precision, max_stalled_in_row, ga_options, max_iterations = None,
                     return_classify = False, test_classification = False):
    error_f = lambda coefs: sum([ err_func(linregr(coefs, xs), expected) 
                                    for expected, xss in expected_xs_dict.iteritems() 
                                    for xs in xss
                                ])
    res = ga.minimize_until_stall(error_f, stall_precision, max_stalled_in_row, ga_options, max_iterations)
    
    res_ = (res, )
    
    if return_classify or test_classification:
        classify = linregr_classifier(expected_xs_dict.keys(), res['best'][0])
        res_ = res_ + (classify, )
    
    if test_classification:
        test_results = [ (clazz, [classify(xs) == clazz for xs in xss])
                          for clazz, xss in expected_xs_dict.iteritems()
                          ]
        test_results = map(lambda (clazz,rs): (clazz, str(count(identity, rs)) + " of " + len(rs)),
                           test_results
                           )
        #test_results = []
        #for clazz, xs in expected_xs_dict.iteritems():
            
        
        res_ = res_ + (test_results, )
        
    
    return res_
    


def linregr_classifier(classes, coefs):
    
    def classifier(xs):
        res = linregr(coefs, xs)
        
        return map(lambda c: (c, abs(c-res)), classes).min(key = lambda (_,x): x)[0]
      
    
    return classifier