from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

class NuMachine():
    def __init__(self, subst=None):
        if subst is None:
            self.subst = dict([])
        else:
            self.subst = subst
    
    def bind(self, var, expr):
        self.subst = extendSubst(var, expr, self.subst)
    
    def step(self, nuEq):
        clo1 = nuEq.clo1
        clo2 = nuEq.clo2
        if nuEq.var:
            res1 = lookupAtom(clo1.av, clo1.binderMap)
            if type(res1) == Free:
                res2 = lookupAtom(clo1.av, clo2.binderMap)
                if type(res2) == Free:
                    self.bind(clo2.av, clo1.av)
                else:
                    raise NameCaptureError(str(clo1.av) + "\n" + str(clo1.binderMap))
            elif type(res1) == Bound:
                res2 = lookupIdx(res1.index, clo2.binderMap)
                self.bind(clo2.av, res2)
        else:
            if sameClo(clo1, clo2):
                pass
            else:
                raise AAMismatchError(str(clo1) + "\n" + str(clo2))
                
    def eval(self, nuProb):
        for eq in nuProb:
            self.step(eq)
