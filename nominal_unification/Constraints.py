from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *

# Constraints
class Closure():
    def __init__(self, av, binderMap):
        self.av = av
        self.binderMap = binderMap
    
    def __str__(self):
        return "Clo(" + str(self.av) + ", " + str(self.binderMap) + ")"
    __repr__ = __str__

def sameClo(clo1, clo2):
    l1 = lookupAtom(clo1.av, clo1.binderMap)
    l2 = lookupAtom(clo2.av, clo2.binderMap)
    
    if type(l1) == Free and type(l2) == Free:
        return clo1.av == clo2.av
    elif type(l1) == Bound and type(l2) == Bound:
        return l1.index == l2.index
    else:
        return False

class NuEquation():
    def __init__(self, clo1, clo2):
        self.clo1 = clo1 # Clo Atom
        self.clo2 = clo2
        self.var = type(clo2.av) == Var
        # If self.var is true, then self.clo2 will be a closure over
        # a Var, otherwise it's a closure over an Atom.
    
    def __str__(self):
        if self.var:
            return "AV(" + str(self.clo1) + ", " + str(self.clo2) + ")"
        else:
            return "AA(" + str(self.clo1) + ", " + str(self.clo2) + ")"
    __repr__ = __str__

# A NuProblem is a list of NuEquations

class DeltaEquation():
    def __init__(self, clo1, clo2):
        self.clo1 = clo1 # Clo Var
        self.clo2 = clo2 # Clo Var
    
    def __str__(self):
        return "VV(" + str(self.clo1) + ", " + str(self.clo2) + ")"
    __repr__ = __str__

# A DeltaProblem is a list of DeltaEquations

class MultiEquation():
    def __init__(self, clo1, clo2):
        self.clo1 = clo1 # Clo Expr
        self.clo2 = clo2 # Clo Expr
    
    def __str__(self):
        return "EE(" + str(self.clo1) + ", " + str(self.clo2) + ")"
    __repr__ = __str__

# A RhoProblem is a list of MultiEquations

# A substitution is literally just a dicitonary mapping stings (inside variables) to expressions.

def extendSubst(var, expr, sub):
    subp = sub.copy()
    subp[var.string] = expr
    return subp

def subst(expr, sub):
    if type(expr) == Var:
        e = sub.get(expr.string, -1)
        if e == -1:
            return expr
        return subst(e, sub)
    elif type(expr) == Abs:
        return Abs(expr.string, subst(expr.expr, sub))
    return expr
