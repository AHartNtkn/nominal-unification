from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

# Delta Machines : a (it's simply a wrapper)
def partition(f, x):
    return (list(filter(f, x)), list(filter(lambda z: not f(z), x)))

# occursInEq : Var -> DeltaEquation -> Bool
def occursInEq(var, deq):
    return (var == deq.clo1.av) or (var == deq.clo2.av)

# evalDelta : Substitution -> DeltaProblem -> [Var] -> DeltaMachine (Substitution, DeltaProblem)
def evalDelta(s, p, xs):
    if len(xs) == 0:
        return (s, p)
    elif len(p) == 0:
        return (s, p)
    else:
        w, wo = partition(lambda z: occursInEq(xs[0], z), p)
        sp, xsp = pull(s, xs[1:], w)
        return evalDelta(sp, wo, xsp)

# pull : Substitution -> [Var] -> DeltaProblem -> DeltaMachine (Substitution, [Var])
def pull(s, xs, p):
    if len(p) == 0:
        return (s, xs)
    else:
        x1 = p[0].clo1.av
        bm1 = p[0].clo1.binderMap
        x2 = p[0].clo2.av
        bm2 = p[0].clo2.binderMap
        pp = p[1:]
        
        x1p = subst(x1, s)
        x2p = subst(x2, s)
        
        if isName(x1p):
            if isName(x2p):
                if not sameClo(p[0].clo1, p[0].clo2):
                    raise AAMismatchError(str(p[0].clo1) + "\n" + str(p[0].clo2))

                return pull(s, xs, pp)
            elif type(x2p) == Var:
                sp = findSubstClo(s, x2p, bm2, Closure(a1, bm1))
                xsc = xs.copy()
                xsc.insert(0, x2p)
                return pull(sp, xsc, pp)
        elif type(x1p) == Var:
            if isName(x2p):
                sp = findSubstClo(s, x1p, bm1, Closure(a2, bm2))
                xsc = xs.copy()
                xsc.insert(0, x1p)
                return pull(sp, xsc, pp)
    raise Exception(str(x1p) ++ " failed to unify with " ++ str(x2p))

# findSubstClo : Substitution -> Var -> BinderMap -> Clo Atom -> DeltaMachine Substitution
def findSubstClo(s, x, bmx, clo):
    a = clo.av
    bma = clo.binderMap
    
    res1 = lookupAtom(a, bma)
    if type(res1) == Free:
        res2 = lookupAtom(a, bmx)
        if type(res2) == Free:
            return extendSubst(x, a, s)
        else:
            raise NameCaptureError(str(a) + "\n" + str(bmx))
    elif type(res1) == Bound:
        i = res1.index
        res2 = lookupIdx(i, bmx)
        return extendSubst(x, res2, s)
