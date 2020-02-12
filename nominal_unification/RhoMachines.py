from pymonad import *

from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

# Rho Machines : State Int a
# The int is just a counter to keep track of how many fresh variables have been created.

# runRhoMachine : RhoMachine a -> Except UnificationError a
def runRhoMachine(m):
    return m.getResult(0)

# freshVar : RhoMachine Var
def freshVar():
    return State(lambda n: (Var("$X" + str(n)), n + 1))

# freshAtom : RhoMachine Atom
def freshAtom():
    return State(lambda n: ("$a" + str(n), n + 1))

# evalRho : NuProblem -> DeltaProblem -> Substitution -> RhoProblem
# -> RhoMachine (NuProblem, DeltaProblem, Substitution)
def evalRho(np,dp,s,rp):
    return foldM(stepRho, (np, dp, s), rp)

def raiseEEMismatchError(cl, cr):
    raise EEMismatchError(str(cl) + "\n" + str(cr))

# stepRho : (NuProblem, DeltaProblem, Substitution) -> MultiEquation
# -> RhoMachine (NuProblem, DeltaProblem, Substitution)
def stepRho(p, m):
    np, dp, s = p
    cl = m.clo1
    cr = m.clo2
    el = cl.av
    bml = cl.binderMap
    er = cr.av
    bmr = cr.binderMap
    
    return expElim(el
    , lambda al: # atomElim
        expElim(er
        , lambda ar: # atomElim
               (npc := np.copy(),
                npc.insert(0, NuEquation(Closure(al, bml), Closure(ar, bmr))),
                State.unit((npc, dp, s))
               )[-1]
        , lambda vr: # varElim
               (npc := np.copy(),
                npc.insert(0, NuEquation(Closure(al, bml), Closure(Var(vr), bmr))),
                State.unit((npc, dp, s))
               )[-1]
        , lambda _, __: raiseEEMismatchError(cl, cr)
                # raise EEMismatch(str(cl) + "\n" + str(cr))
        , lambda _, __: raiseEEMismatchError(cl, cr)
                # raise EEMismatch(str(cl) + "\n" + str(cr))
        )
    ,   lambda vl: # varElim
        expElim(er
        , lambda _: # atomElim
                stepRho((np, dp, s), MultiEquation(cr, cl))
        , lambda vr: # varElim
                (dpc := dp.copy(),
                 dpc.insert(0, DeltaEquation(Closure(Var(vl), bml), Closure(Var(vr), bmr))),
                 State.unit((np, dpc, s))
                )[-1]
        , lambda r1, r2: # appElim
                freshVar().bind(
                    lambda v1: freshVar().bind(
                    lambda v2:
                        (sp := extendSubst(Var(vl), App(v1, v2), s),
                         stepRho((np, dp, sp), MultiEquation(Closure(v1, bml), Closure(r1, bmr))).bind(
                            lambda p: ( 
                                npp := p[0],
                                dpp := p[1],
                                spp := p[2],
                                stepRho((npp, dpp, spp), MultiEquation(Closure(v2, bml), Closure(r2, bmr)))
                                )[-1]
                         )
                        )[-1]
                ))
                  
        , lambda ar, br: # absElim
                freshAtom().bind(
                    lambda al:
                    freshVar().bind(
                    lambda vb: (
                        sp := extendSubst(Var(vl), Abs(al, vb), s),
                        bmlp := extend(al, bml),
                        bmrp := extend(ar, bmr),
                        stepRho((np, dp, sp), MultiEquation(Closure(vb, bmlp), Closure(br, bmrp)))
                        )[-1]
                ))
        )
    ,   lambda l1, l2: # appElim
        expElim(er
        , lambda _: raiseEEMismatchError(cl, cr)
                # raise EEMismatch(str(cl) + "\n" + str(cr))
        , lambda _: # varElim
                stepRho((np, dp, s), MultiEquation(cr, cl))
        , lambda r1, r2: # appElim
                stepRho((np, dp, s), MultiEquation(Closure(l1, bml), Closure(r1, bmr))).bind(
                    lambda p: (
                        npp := p[0],
                        dpp := p[1],
                        sp := p[2],
                        stepRho((npp, dpp, sp), MultiEquation(Closure(l2, bml), Closure(r2, bmr)))
                        )[-1]
                )
        , lambda _, __: raiseEEMismatchError(cl, cr)
                    # raise EEMismatch(str(cl) + "\n" + str(cr))
        )
    ,   lambda al, bl: # absElim
        expElim(er
        , lambda _: raiseEEMismatchError(cl, cr)
                # raise EEMismatch(str(cl) + "\n" + str(cr))
        , lambda _: # varElim
                stepRho((np, dp, s), MultiEquation(cr, cl))
        , lambda _, __: raiseEEMismatchError(cl, cr)
                # raise EEMismatch(str(cl) + "\n" + str(cr))
        , lambda ar, br: ( # absElim
                bmlp := extend(al, bml),
                bmrp := extend(ar, bmr),
                stepRho((np, dp, s), MultiEquation(Closure(bl, bmlp), Closure(br, bmrp)))
                )[-1]
        )
    )
