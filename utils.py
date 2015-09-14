

  
def head(l): return l[0]
def tail(l): return l[1:]

def last(l):     return l[len(l)]
def but_last(l): return l[:len(l)-1]
    

def even(n): return n % 2 == 0
def odd (n): return not even(n)

def mean(l): return float(sum(l)) / len(l)

def tupled(f): return lambda tpl: f(*tpl)


