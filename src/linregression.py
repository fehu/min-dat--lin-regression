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
  


def minimize_linregr(expected_xs_dict, err_func, stall_precision, max_stalled_in_row, ga_options,
                     return_classify = False, test_classification = False):
    error_f = lambda coefs: sum([ err_func(linregr(coefs, xs), expected) 
                                    for expected, xss in expected_xs_dict.iteritems() 
                                    for xs in xss
                                ])
    res = ga.minimize_until_stall(error_f, stall_precision, max_stalled_in_row, ga_options)
    
    res_ = (res, )
    
    if return_classify or test_classification:
        classify = linregr_classifier(expected_xs_dict.keys(), res['best'][0])
        res_ = res_ + (classify, )
    
    if test_classification:
        test_results = [ (clazz, [classify(xs) == clazz for xs in xss])
                          for clazz, xss in expected_xs_dict.iteritems()
                          ]
        
        test_count   = map(lambda (clazz,rs): (clazz, count(identity, rs), len(rs)), test_results)
        
        test_results = map(lambda (clazz,c,n): (clazz, str(c) + " of " + str(n)),
                           test_count
                           )
        
        test_results_total = reduce(lambda (ac,an), (_,c,n): (ac+c, an+n), test_count, (0,0))
        
        test_results.sort(key=lambda(c,_): c)
        
        res_ = res_ + (test_results, test_results_total)
        
    
    return res_


def print_minimize_linregr_result(res):
    ga.print_intil_stall_result(head(res))
      
    if len(res) == 4:
        print "\nTest results:"
        for (clazz, test_res) in res[2]:
            print "\t" + str(clazz) + "\t" + test_res
        
        matched, total = res[3]
        print
        print "Total: " + str(matched) + " of " + str(total)




def linregr_classifier(classes, coefs):
    
    def classify(xs):
        res = linregr(coefs, xs)
        
        c_class_dist = map(lambda c: (c, abs(c-res)), classes)
        
        return min(c_class_dist, key = lambda (_,x): x)[0]
      
    
    return classify