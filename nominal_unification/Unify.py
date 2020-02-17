from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *
from nominal_unification.NuMachines import *
from nominal_unification.DeltaMachines import *
from nominal_unification.RhoMachines import *

def unify(l, r):
    """ Given two well-formed expressions (consisting of Var, Abs, tuples,
        strings, and/or ints) produce its most general unifier.
    """
    rm = RhoMachine()
    rm.eval([MultiEquation(Closure(l, emptyScope()),
                           Closure(r, emptyScope()))])
    
    nu = NuMachine(rm.s)
    nu.eval(rm.p)
    
    return evalDelta(nu.subst, rm.d, list(map(Var, nu.subst.keys())))
