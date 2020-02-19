from nominal_unification.Syntax import *
from nominal_unification.Constraints import *
from nominal_unification.NuMachines import *
from nominal_unification.DeltaMachines import *
from nominal_unification.RhoMachines import *


def _unify(l, r):
    """ Given two well-formed expressions (consisting of Var, Abs, tuples,
        strings, and/or ints) produce its most general unifier.
    """
    rm = RhoMachine()
    rm.eval([MultiEquation(Closure(l, emptyScope()),
                           Closure(r, emptyScope()))])

    nu = NuMachine(rm.s)
    nu.eval(rm.p)

    return evalDelta(nu.s, rm.d, list(map(Var, nu.s.keys())))

def unify(l, r):
    """ Given two well-formed expressions (consisting of Var, Abs, tuples,
        strings, and/or ints) produce its most general unifier.

        Returns only unifier, and "False" if unification fails.
    """
    try:
        res, dp = _unify(l, r)

        if len(dp) != 0:
          return False

        return res
    except UnificationError:
        return False

