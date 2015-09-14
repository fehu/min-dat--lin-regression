
import random
import operator

def minimize(fitness_func, target_fitness, max_iter, options):
    population_size   = options['Population']
    chromosomes_count = options['N_Chromosomes']
    
    initial_population = [ [random.gauss(0, 1) for _ in range(chromosomes_count)] for _ in range(population_size) ] # random.random() 
    next_generation_func = next_generation(options)
    
    target_fit_func = lambda f: f <= target_fitness
    
    #if target.lower() == "max":   target_fit_func = lambda f: f >= target_fitness
    #elif target.lower() == "min": target_fit_func = lambda f: f <= target_fitness
    #else: error("unrecognized target, should be 'max' or 'min'")
    
    stop_func = lambda count: count >= max_iter
    
    _stop_flag = False
    _population = initial_population
    _count = 0
    
    while not _stop_flag:
        res = _minimize_inner(_population, _count, fitness_func, stop_func, target_fit_func)
        if res['success'] == None: 
            _population = next_generation_func(res['result'])
            _count = _count + 1
        else:
            _stop_flag = True
    
    return res



def default_options(population, chromosomes_count): return {
  'Population':                 population,
  'N_Chromosomes':              chromosomes_count,
  'N_Elite':                    population / 100,
  'Crossover_Fraction':         0.5,
  'Crossover':                  xover_simple_between_best,
  'Mutate':                     mutate_simple_random,
  'Chromosome_Mutation_Chance': 0.2
  }


def _minimize_inner(generation, count, fitness_func, stop_func, target_fitness_func):
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
    
    xover_count  = int(crossover_fraction * population_size) - elite_count
    mutate_count = population_size - xover_count - 2*elite_count
    
    print "xover_count = " + str(xover_count)
    
    xover_last_index = elite_count+xover_count
    
    def func(parents_with_fit):
        parents_with_fit.sort(key = lambda (_, f): f)
        parents = map(lambda (p,_): p, parents_with_fit)
        
        elite = parents[0:elite_count]
        xover = parents[elite_count:xover_last_index]
        rest  = parents[xover_last_index:xover_last_index+mutate_count]
        
        xover_children = crossover_func(options, xover)
        mutated_elite  = mutate_func(options, elite)
        mutated_xover  = mutate_func(options, xover_children)
        mutated_rest   = mutate_func(options, rest)
        mutated        = mutated_elite + mutated_xover + mutated_rest
        
        return elite + mutated
    
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
    mutate_chromosome = lambda chrom: chrom + random.gauss(0, 1)
    
    mutated = [ [ mutate_chromosome(c) if random.random() < mutate_chance else c for c in p ] 
                 for p in parents 
               ]
    return mutated

    
def even(n): return n % 2 == 0
def odd (n): return not even(n)

def last(l):     return l[len(l)]
def but_last(l): return l[:len(l)-1]