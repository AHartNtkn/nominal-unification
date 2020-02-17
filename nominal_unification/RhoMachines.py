from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *


class RhoMachine():
    """ A rho machine exists to proccess a list of multi-equations into a list
        of nu (name-name and name-var) and delta (var-var) problems from two
        full expressions.
    """

    def __init__(self, p=None, d=None, s=None, fresh=None):
        if p is None:
            self.p = []
        else:
            self.p = p

        if d is None:
            self.d = []
        else:
            self.d = d

        if s is None:
            self.s = dict([])
        else:
            self.s = s

        if fresh is None:
            self.fresh = 0
        else:
            self.fresh = fresh

    def newVar(self):
        """ Generate a fresh variable.
        """
        v = Var("$X" + str(self.fresh))
        self.fresh += 1
        return v

    def newName(self):
        """ Generate a fresh name.
        """
        a = "$a" + str(self.fresh)
        self.fresh += 1
        return a

    def step(self, m):
        """ Given a  single multi-equations, proccess it into a nu problem, a
            delta problem, and a substitution.

            In the original white paper, this operation is denoted by the
            judgement ν0; δ0; σ0 ⊦ e ⇒s ν1; δ1; σ1, where ν0 is an input nu
            problem, δ0 is an input delta problem, σ0 is an input substitution,
            e is an input multi-equation, ν1 is an output nu problem, δ1 is an
            output delta problem, and σ1 is an output substitution.

            See [N-N], [N-V], [V-V], [C-C], [A-A], [V-C], [V-A], [V-A'] in
            Figure 8.
        """
        clo1 = m.clo1
        clo2 = m.clo2
        el = clo1.expr
        Phi1 = clo1.scope
        er = clo2.expr
        Phi2 = clo2.scope

        if isName(el):
            if isName(er):
                # [N-N] Figure 8
                # p1 = (〈a1; Φ1〉≈NN〈a2; Φ2〉) ∪ p0
                # -------------------------------------------------
                # p0; δ0; σ0 ⊦ (〈a1; Φ1〉≈EE〈a2; Φ2〉) ⇒s p1; δ0; σ0

                a1 = el
                a2 = er

                self.p.insert(
                    0, NuEquation(
                        Closure(
                            a1, Phi1), Closure(
                            a2, Phi2)))
            elif isinstance(er, Var):
                # [N-V] Figure 8
                # p1 = (〈a1; Φ1〉≈NV〈X2; Φ2〉) ∪ p0
                # -------------------------------------------------
                # p0; δ0; σ0 ⊦ (〈a1; Φ1〉≈EE〈X2; Φ2〉) ⇒s p1; δ0; σ0

                a1 = el
                X2 = er

                self.p.insert(
                    0, NuEquation(
                        Closure(
                            a1, Phi1), Closure(
                            X2, Phi2)))
            elif isinstance(er, tuple):
                raise EEMismatchError(str(clo1) + "\n" + str(clo2))
            elif isinstance(er, Abs):
                raise EEMismatchError(str(clo1) + "\n" + str(clo2))
            else:
                raise Exception(str(er) + 'is not an expression')
        elif isinstance(el, Var):
            if isName(er):
                self.step(MultiEquation(clo2, clo1))
            elif isinstance(er, Var):
                # [V-V] Figure 8
                # δ1 = (〈X1; Φ1〉≈VV〈X2; Φ2〉) ∪ δ0
                # ----------------------------------------------------
                # p0; δ0; σ0 ⊦ (〈X1; Φ1〉≈EE〈X2; Φ2〉) ⇒s p0; δ1; σ0

                X1 = el
                X2 = er

                self.d.insert(
                    0, DeltaEquation(
                        Closure(
                            X1, Phi1), Closure(
                            X2, Phi2)))
            elif isinstance(er, tuple):
                # [V-C] Figure 8
                # X0 = (new-var) ... Xi = (new-var)
                # p0; δ0; {Y/(X0...Xi)} ∪ σ0 ⊦ (〈X0; Φ1〉≈EE〈a0; Φ2〉) ⇒s p1; δ1; σ1
                # p1; δ1; σ1 ⊦ (〈X1; Φ1〉≈EE〈a1; Φ2〉) ⇒s p2; δ2; σ2
                # p2; δ2; σ2 ⊦ ...
                # pi; δi; σi ⊦ (〈Xi; Φ1〉≈EE〈ai; Φ2〉) ⇒s pi'; δi'; σi'
                # -------------------------------------------------------------
                # p0; δ0; σ0 ⊦ (〈Y; Φ1〉≈EE〈(a0...ai); Φ2〉) ⇒s pi'; δi'; σi'

                Y = el
                a = er

                X = [self.newVar() for _ in er]

                self.s[Y.string] = tuple(X)

                for Xi, ai in zip(X, a):
                    self.step(
                        MultiEquation(
                            Closure(
                                Xi, Phi1), Closure(
                                ai, Phi2)))
            elif isinstance(er, Abs):
                X1 = el

                a2 = er.string
                t2 = er.expr

                res = lookupName(a2, Phi1)
                if isinstance(res, Free):
                    # [V-A] Figure 8
                    # Φ1 ⊦ Fr a2
                    # a1 = (new-name)
                    # Xt = (new-var)
                    # Φ1' = (ext Φ1 a1)
                    # Φ2' = (ext Φ2 a2)
                    # p0; δ0; {X1/λa1.Xt} ∪ σ0 ⊦ (〈Xt; Φ1'〉≈EE〈t2; Φ2'〉) ⇒s p1; δ1; σ1
                    # --------------------------------------------------------------------
                    # p0;δ0;σ0`(〈X1; Φ1〉≈EE〈λa2.t2; Φ2〉) ⇒s p1; δ1; σ1

                    a1 = self.newName()
                    Xt = self.newVar()
                    Phi1p = extend(a1, Phi1)
                    Phi2p = extend(a2, Phi2)

                    self.s[X1.string] = Abs(a1, Xt)

                    self.step(
                        MultiEquation(
                            Closure(
                                Xt, Phi1p), Closure(
                                t2, Phi2p)))

                elif isinstance(res, Bound):
                    # [V-A'] Figure 8
                    # Φ1 ⊦ Bd a1 i
                    # Φ2 ⊦ Bd a2 i
                    # Xt = (new-var)
                    # Φ1' = (ext Φ1 a1)
                    # Φ2' = (ext Φ2 a2)
                    # p0; δ0; {X1/λa1.Xt} ∪ σ0 ⊦ (〈Xt; Φ1'〉≈EE〈t2; Φ2'〉) ⇒s p1; δ1; σ1
                    # --------------------------------------------------------------------
                    # p0; δ0; σ0 ⊦ (〈X1; Φ1〉≈EE〈λa2.t2; Φ2〉) ⇒s p1; δ1; σ1

                    a1 = self.newName()
                    a2 = Phi2.i2a.get(res.index, -1)

                    if a2 == -1:
                        raise Exception(
                            "Scopes within expressions " +
                            str(clo1) +
                            " and " +
                            str(clo2) +
                            " have inequal length.")

                    Xt = self.newVar()

                    Phi1p = extend(a1, Phi1)
                    Phi2p = extend(a2, Phi2)

                    self.s[X1.string] = Abs(a1, Xt)

                    self.step(
                        MultiEquation(
                            Closure(
                                Xt, Phi1p), Closure(
                                t2, Phi2p)))
            else:
                raise Exception(str(er) + 'is not an expression')
        elif isinstance(el, tuple):
            if isName(er):
                raise EEMismatchError(str(clo1) + "\n" + str(clo2))
            elif isinstance(er, Var):
                self.step(MultiEquation(clo2, clo1))
            elif isinstance(er, tuple):
                # [C-C] Figure 8
                # p0; δ0; σ0 ⊦ (〈l0; Φ1〉〈r0; Φ2〉) ⇒s p1; δ1; σ1
                # p1; δ1; σ1 ⊦ (〈l1; Φ1〉〈r1; Φ2〉) ⇒s p2; δ2; σ2
                # p2; δ2; σ2 ⊦ ...
                # pi; δi; σi ⊦ (〈li; Φ1〉〈ri; Φ2〉) ⇒s pi'; δi'; σi'
                # -----------------------------------------------------------------
                # p0; δ0; σ0 ⊦ (〈(li...); Φ1〉≈EE〈(ri...); Φ2〉) ⇒s pi'; δi'; σi'

                if len(el) != len(er):
                    raise EEMismatchError(str(clo1) + "\n" + str(clo2))

                for li, ri in zip(el, er):
                    self.step(
                        MultiEquation(
                            Closure(
                                li, Phi1), Closure(
                                ri, Phi2)))
            elif isinstance(er, Abs):
                raise EEMismatchError(str(clo1) + "\n" + str(clo2))
            else:
                raise Exception(str(er) + 'is not an expression')
        elif isinstance(el, Abs):
            if isName(er):
                raise EEMismatchError(clo1, clo2)
            elif isinstance(er, Var):
                self.step(MultiEquation(clo2, clo1))
            elif isinstance(er, tuple):
                raise EEMismatchError(str(clo1) + "\n" + str(clo2))
            elif isinstance(er, Abs):
                # [A-A] Figure 8
                # Φ1' = (ext Φ1 a1)
                # Φ2' = (ext Φ2 a2)
                # p0; δ0;σ0 ⊦ (〈t1; Φ1'〉≈EE〈t2; Φ2'〉) ⇒s p1; δ1; σ
                # ---------------------------------------------------------
                # p0;δ0;σ0 ⊦ (〈λa1.t1; Φ1〉≈EE〈λa2.t2; Φ2〉)⇒s p1; δ1; σ1

                a1 = el.string
                t1 = el.expr

                a2 = er.string
                t2 = er.expr

                Phi1p = extend(a1, Phi1)
                Phi2p = extend(a2, Phi2)

                self.step(
                    MultiEquation(
                        Closure(
                            t1, Phi1p), Closure(
                            t2, Phi2p)))
            else:
                raise Exception(str(er) + 'is not an expression')
        else:
            raise Exception(str(el) + 'is not an expression')

    def eval(self, rp):
        """ Evaluate a list of multi-equations in sequence using step.
        """
        for eq in rp:
            self.step(eq)
