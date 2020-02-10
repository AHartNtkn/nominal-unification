from pymonad import *

from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

# Nu Machines : State Substitution a

# runNuMachine : Substitution -> NuMachine -> Substitution
def runNuMachine(sub, nuM):
    return nuM.getState(sub)

# bind : Var -> Exp -> NuMachine
def bind(var, expr):
    return modify(lambda sub: extendSubst(var, expr, sub))

# stepNu : NuEquation -> NuMachine
def stepNu(nuEq):
    clo1 = nuEq.clo1
    clo2 = nuEq.clo2
    if nuEq.var:
        res1 = lookupAtom(clo1.av, clo1.binderMap)
        if type(res1) == Free:
            res2 = lookupAtom(clo1.av, clo2.binderMap)
            if type(res2) == Free:
                return bind(clo2.av, clo1.av)
            else:
                raise NameCaptureError(str(clo1.av) + "\n" + str(clo1.binderMap))
        elif type(res1) == Bound:
            res2 = lookupIdx(res1.index, clo2.binderMap)
            return bind(clo2.av, res2)
    else:
        if sameClo(clo1, clo2):
            return State.unit(())
        else:
            raise AAMismatchError(str(clo1) + "\n" + str(clo2))

# eval : NuProblem -> NuMachine
def evalNu(nuProb):
    return mapMU(stepNu, nuProb)
