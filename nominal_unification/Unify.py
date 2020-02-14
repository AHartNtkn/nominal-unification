from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *
from nominal_unification.NuMachines import *
from nominal_unification.DeltaMachines import *
from nominal_unification.RhoMachines import *

# Unify

# unify : Expr -> Expr -> (Substitution, DeltaProblem)
def unify(l, r):
    rm = RhoMachine()
    rm.eval([MultiEquation(Closure(l, emptyBinderMap()),
                           Closure(r, emptyBinderMap()))])
    
    nu = NuMachine(rm.s)
    nu.eval(rm.np)
    
    return evalDelta(nu.subst, rm.dp, list(nu.subst.keys()))
