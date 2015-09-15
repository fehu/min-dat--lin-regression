
import random
import operator
import sys

from utils import *



# Judjes stallation by elite_fit_mean
# `fitness_func` has sense "unfitness_func" while minimizing
def minimize_until_stall(fitness_func, stall_precision, max_stalled_in_row, options, 
                         max_iter = None):
    initial_population   = _initial_population(options)
    print_the_info       = _get_print_the_info(options)
    next_generation_func = next_generation(options)
    
    if max_iter:
        stop_func = lambda count: count == max_iter
    else:
        stop_func = lambda count: False
    
    inner = _minimize_until_stall(fitness_func, stop_func, stall_precision, max_stalled_in_row,
                                  options, print_the_info)
    
    _stop_flag = False
    _population = initial_population
    _count = 0
    _last_elite_fit_mean = sys.maxint
    _stalled = 0
    
    while not _stop_flag:
        res = inner(_population, _count, _last_elite_fit_mean, _stalled)
        if res['success'] == None: 
            _population = next_generation_func(res['result'])
            _count = _count + 1
            _last_elite_fit_mean = res['elite_fit_mean']
            _stalled = res['stalled']
        else:
            _stop_flag = True
    
    return res


def _minimize_until_stall(fitness_func, stop_func, stall_precision, 
                          max_stalled_in_row, options, print_the_info):
  
  
    def inner(generation, count, last_elite_fit_mean, stalled_count):
        fit_of_gen = [ (ex, fitness_func(ex)) for ex in generation ]
        
        elite = fit_of_gen[:options['N_Elite']]
        elite_fit_mean = mean(map(lambda (_,f): f, elite))
        
        print_the_info(fit_of_gen, count, options, elite_fit_mean)
        
        if last_elite_fit_mean - elite_fit_mean <= stall_precision:
            stalled = stalled_count + 1
        else:
            stalled = 0
        
        if stalled == max_stalled_in_row:
            return { 'success': True, 
                     'result' : elite,
                     'count'  : count,
                     'best'   : max(elite, key = lambda (_,f): f),
                     'elite_fit_mean': elite_fit_mean
                    }
        elif stop_func(count):
            return { 'success': False,
                     'result' : fit_of_gen,
                     'count'  : count,
                     'best'   : max(elite, key = lambda (_,f): f),
                     'elite_fit_mean': elite_fit_mean
                    }
        else:
            return { 'success': None, 
                     'result' : fit_of_gen,
                     'stalled': stalled,
                     'elite_fit_mean': elite_fit_mean
                    }
        

    return inner
    


def minimize_to_target(fitness_func, target_fitness, max_iter, options, n_retry=0):
    initial_population   = _initial_population(options)
    print_the_info       = _get_print_the_info(options)
    next_generation_func = next_generation(options)
    
    target_fit_func = lambda f: f <= target_fitness
    stop_func       = lambda count: count == max_iter
    
    _stop_flag = False
    _population = initial_population
    _count = 0
    
    while not _stop_flag:
        res = _minimize_to_target_inner(_population, _count, fitness_func, stop_func, target_fit_func)
        if res['success'] == None: 
            _res = res['result']
            _population = next_generation_func(_res)
            _count = _count + 1
            print_the_info(_res, _count, options)
        elif res['success'] == False:
            _stop_flag = True
            if n_retry > 0:
                print "\nRetrying... " + str(n_retry-1) + " tries left.\n"
                res = minimize(fitness_func, target_fitness, max_iter, options, n_retry-1)
        else:
            _stop_flag = True
        
    
    return res

def _minimize_to_target_inner(generation, count, fitness_func, stop_func, target_fitness_func):
    fit_of_gen = [ (ex, fitness_func(ex)) for ex in generation ]
    fit = filter(lambda (ex, f): target_fitness_func(f), fit_of_gen)
    if len(fit) > 0:
        return { 'success': True, 
                 'result' : fit,
                 'count'  : count
                 }
    elif stop_func(count):
        return { 'success': False,
                 'result' : fit_of_gen,
                 'count'  : count
                 }
    else:
        return { 'success': None, 
                 'result' : fit_of_gen 
                }





def _get_print_the_info(options):
    if options['Print_Info_Each']:
        print_the_info = _print_the_info
    else:
        print_the_info = _nothing
    return print_the_info

def _print_the_info(gen_with_fit, count, options, elite_fit_mean = None):
        if count % options['Print_Info_Each'] == 0:
            best           = head(gen_with_fit)
            elite          = gen_with_fit[:options['N_Elite']]
            fit_mean       = mean(map(lambda (_,f): f, gen_with_fit))
            elite_fit_mean = elite_fit_mean or mean(map(lambda (_,f): f, elite))
            
            print 'Iteration ' + str(count) 
            print '\t fitness mean: ' + str(fit_mean)
            print '\t elite fitness mean: ' + str(elite_fit_mean)
            print "\t best: " + str(best)

def _nothing(x): return
  
def _initial_population(options):
    return [ [random.gauss(0, 1) for _ in range(options['N_Chromosomes'])] 
                                 for _ in range(options['Population']) 
                                ]






def default_options(population, chromosomes_count, Print_Info_Each = 10, Mutate_Stdev = 1): return {
  'Population':                 population,
  'N_Chromosomes':              chromosomes_count,
  'N_Elite':                    population / 100,
  'Crossover_Fraction':         0.5,
  'Crossover':                  xover_simple_between_best,
  'Crossover_Mutate_Chance':    0.5,
  'Crossover_Mutate_Preserve':  True,
  'Mutate':                     mutate_simple_random,
  'Chromosome_Mutation_Chance': 0.2,
  'Print_Info_Each':            Print_Info_Each,
  'Mutate_Stdev':               Mutate_Stdev,
  'Mutate_Shrink':              0
  }


# inspired by Matlab's globalOptimization: elite, xover, mutate 
#   All the elite go to the next generation;
#   The `crossover_fraction` of the best parents are chosen for crossover;
#   The rest is mutated
def next_generation(options): 
    population_size    = options['Population']
    elite_count        = options['N_Elite']
    crossover_fraction = options['Crossover_Fraction']
    
    crossover_func = options['Crossover']
    mutate_func    = options['Mutate']
    
    cm_ch       = options['Crossover_Mutate_Chance']
    cm_preserve = options['Crossover_Mutate_Preserve']
    
    xover_count  = int(crossover_fraction * population_size) - elite_count
    xover_last_index = elite_count+xover_count
    
    # case not cm_preserve
    default_mutate_count = population_size - xover_count - 2*elite_count
    
    def func(parents_with_fit):
        parents_with_fit.sort(key = lambda (_, f): f)
        parents = map(lambda (p,_): p, parents_with_fit)
        
        elite = parents[0:elite_count]
        xover = parents[elite_count:xover_last_index]
        
        xover_children = crossover_func(options, xover)
        mutated_elite  = mutate_func(options, elite)
        
        if cm_preserve:
            xover_2_mutate  = filter(lambda _: random.random() < cm_ch, xover_children)
            mutated_xover   = mutate_func(options, xover_2_mutate)
            # case cm_preserve
            mutate_count    = default_mutate_count - len(mutated_xover)
            resulting_xover = xover_children + mutated_xover
        else:
            mutate_count    = default_mutate_count
            resulting_xover = [ mutate_func(options, [ch])[0] if random.random() < cm_ch else ch
                                 for ch in xover_children
                               ]
        
        
        rest  = parents[xover_last_index:xover_last_index+mutate_count]
        
        mutated_rest   = mutate_func(options, rest)
        mutated        = mutated_elite + mutated_rest
        
        return elite + resulting_xover + mutated
    
    return func
  

def xover_simple_between_best(options, parents):
    chromosomes_count = options['N_Chromosomes']
  
    if even(len(parents)):
        one_more = None
        n = len(parents) - 1
    else:
        one_more = last(parents)
        n = len(parents)
    
    def xover_func(p1, p2):
        n = chromosomes_count / 2
        a1 = p1[:n]
        b1 = p1[n:]
        a2 = p2[:n]
        b2 = p2[n:]
        
        ch1 = a1 + b2
        ch2 = a2 + b1
        
        return [ch1, ch2]
    
    children_ = [ xover_func(parents[i], parents[i+1]) for i in range(0, n, 2) ]
    
    children = reduce(operator.add, children_)
    
    if one_more:
        children = children + xover_func(one_more, random.choice(but_last(parents)))
    
    return children



def mutate_simple_random(options, parents):
    mutate_chance = options['Chromosome_Mutation_Chance']
    
    #mutate_chromosome = lambda chrom: chrom*random.random() + random.random()
    mutate_chromosome = lambda chrom: chrom + random.gauss(0, options['Mutate_Stdev'])
    
    mutated = [ [ mutate_chromosome(c) if random.random() < mutate_chance else c for c in p ] 
                 for p in parents 
               ]
    return mutated
