from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

class RhoMachine():
    def __init__(self, np=None, dp=None, s=None, fresh=None):
        if np is None:
            self.np = []
        else:
            self.np = np
        
        if dp is None:
            self.dp = []
        else:
            self.dp = dp
        
        if s is None:
            self.s = dict([])
        else:
            self.s = s
        
        if fresh is None:
            self.fresh = 0
        else:
            self.fresh = fresh

    def freshVar(self):
        v = Var("$X" + str(self.fresh))
        self.fresh += 1
        return v
    
    def freshAtom(self):
        a = "$a" + str(self.fresh)
        self.fresh += 1
        return a
    
    def step(self, m):
        cl = m.clo1
        cr = m.clo2
        el = cl.av
        bml = cl.binderMap
        er = cr.av
        bmr = cr.binderMap
        
        if type(el) == str or type(el) == int:
            if type(er) == str or type(er) == int:
                self.np.insert(0, NuEquation(Closure(el, bml), Closure(er, bmr)))
            elif type(er) == Var:
                self.np.insert(0, NuEquation(Closure(el, bml), Closure(er, bmr)))
            elif type(er) == App:
                raise EEMismatchError(str(cl) + "\n" + str(cr))
            elif type(er) == Abs:
                raise EEMismatchError(str(cl) + "\n" + str(cr))
            else:
                raise Exception(str(er) + 'is not an expression')
        elif type(el) == Var:
            if type(er) == str or type(er) == int:
                self.step(MultiEquation(cr, cl))
            elif type(er) == Var:
                self.dp.insert(0, DeltaEquation(Closure(el, bml), Closure(er, bmr)))
            elif type(er) == App:
                v1 = self.freshVar()
                v2 = self.freshVar()
                self.s = extendSubst(el, App(v1, v2), self.s)
                self.step(MultiEquation(Closure(v1, bml), Closure(er.expr1, bmr)))
                self.step(MultiEquation(Closure(v2, bml), Closure(er.expr2, bmr)))
            elif type(er) == Abs:
                al = self.freshAtom()
                vb = self.freshVar()
                self.s = extendSubst(el, Abs(al, vb), self.s)
                bmlp = extend(al, bml)
                bmrp = extend(er.string, bmr)
                self.step(MultiEquation(Closure(vb, bmlp), Closure(er.expr, bmrp)))
            else:
                raise Exception(str(er) + 'is not an expression')
        elif type(el) == App:
            if type(er) == str or type(er) == int:
                raise EEMismatchError(str(cl) + "\n" + str(cr))
            elif type(er) == Var:
                self.step(MultiEquation(cr, cl))
            elif type(er) == App:
                self.step(MultiEquation(Closure(el.expr1, bml), Closure(er.expr1, bmr)))
                self.step(MultiEquation(Closure(el.expr2, bml), Closure(er.expr2, bmr)))
            elif type(er) == Abs:
                raise EEMismatchError(str(cl) + "\n" + str(cr))
            else:
                raise Exception(str(er) + 'is not an expression')
        elif type(el) == Abs:
            if type(er) == str or type(er) == int:
                raise EEMismatchError(cl, cr)
            elif type(er) == Var:
                self.step(MultiEquation(cr, cl))
            elif type(er) == App:
                raise EEMismatchError(str(cl) + "\n" + str(cr))
            elif type(er) == Abs:
                bmlp = extend(el.string, bml)
                bmrp = extend(er.string, bmr)
                self.step(MultiEquation(Closure(el.expr, bmlp), Closure(er.expr, bmrp)))
            else:
                raise Exception(str(er) + 'is not an expression')
        else:
            raise Exception(str(el) + 'is not an expression')
    
    def eval(self, rp):
        for eq in rp:
            self.step(eq)
