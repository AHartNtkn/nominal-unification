from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *


def occursInEq(var, deq):
    """ Detects if a variable appears within a delta equation.
    """
    return (var == deq.clo1.expr) or (var == deq.clo2.expr)


def pull(s0, xs0, pp):
    """ The pull operation for a delta machine.

        Given a substitution, a list of known variables, and a delta problem
        (list of var-var equational constraints), the pull operation will solve
        the constraints to produce a new substitution and a new list of
        variables.

        In the original white-paper, this is denoted by the judgment,
        σ0 ; xs0 ⊦ δ ⇒pull σ1 ; xs1, where σ0 is an input substitution, xs0 is
        an input list of known variables, δ is an input list of delta problems,
        σ1 is an output substitution, and xs1 is an output list of known
        variables.

        See [Empty], [N-N], and [N-V] in Figure 6
    """
    if len(pp) == 0:
        # [Empty] Figure 6
        #
        # --------------------
        # σ;xs ⊦ ϵ ⇒pull σ;xs
        return (s0, xs0)
    else:
        clo1 = pp[0].clo1
        X1 = clo1.expr
        Phi1 = clo1.scope

        clo2 = pp[0].clo2
        X2 = clo2.expr
        Phi2 = clo2.scope

        p = pp[1:]

        if X1.string in s0:
            if X2.string in s0:
                # [N-N] Figure 6
                # 〈a1; Φ1〉≈〈a2; Φ2〉
                # σ0(X1) = a1
                # σ0(X2) = a2
                # σ0; xs0 ⊦ p ⇒pull σ1; xs1
                # -----------------------------------------------
                # σ0; xs0 ⊦〈X1; Φ1〉=〈X2; Φ2〉, p ⇒pull σ1; xs1

                a1 = s0[X1.string]
                a2 = s0[X2.string]

                if not alphaEq(Closure(a1, Phi1), Closure(a2, Phi2)):
                    raise NNMismatchError(
                        str(Closure(a1, Phi1)) + "\n" + str(Closure(a2, Phi2)))

                return pull(s0, xs0, p)

            else:
                # [N-V] Figure 6
                # 〈a1; Φ1〉≈〈a2; Φ2〉
                # σ0(X1) = a1
                # X2 ∉ dom(σ0)
                # {X2/a2} ∪ σ0; (X2 :: xs0) ⊦ p ⇒pull σ1; xs1
                # ------------------------------------------------
                # σ0; xs0 ⊦ 〈X1; Φ1〉=〈X2; Φ2〉, p ⇒pull σ1; xs1

                a1 = s0[X1.string]

                # Find an appropriate a2.
                # Is there's a better way to do this?
                res = lookupName(a1, Phi1)
                if isinstance(res, Free):
                    a2 = lookupName(a1, Phi2)
                    if not isinstance(a2, Free):
                        raise NameCaptureError(str(a1) + "\n" + str(Phi1))
                    a2 = a2.string
                elif isinstance(res, Bound):
                    a2 = lookupIdx(res.index, Phi2)

                xs0p = xs0.copy()
                xs0p.insert(0, X2)

                return pull(extendSubst(X2, a2, s0), xs0p, p)

        elif X2.string in s0:
            # In the case that the first closure has a variable, reverse the
            # equation.
            pp[0] = DeltaEquation(clo2, clo1)

            return pull(s0, xs0, pp)

        raise Exception(str(clo1) + " failed to unify with " + str(clo2))


def evalDelta(s0, d0, xs):
    """ Delta machine evaluation. This computes the final unifier on  three
        inputs:  the  substitution  resulting from a nu machine, a delta
        problem (list of var-var equational constraints), and  a  list  of
        known variables assumed to be the domain/keys of the substitution,
        initially.

        In the original white-paper, this is denoted by the judgment,
        σ0 ; δ0 ⊦ xs ⇒δ σ1 ; δ1, where σ0 is an input substitution, δ0 is an
        input delta problem, xs is an input list of known variables, σ1 is an
        output substitution, and δ1 is an output delta problem.

        See [Empty-Xs], [Empty-D], and [Pull] in Figure 6.
    """
    if len(xs) == 0:
        # [Empty-Xs] Figure 6
        #
        # ---------------
        # σ;δ ⊦ ϵ ⇒δ σ;δ
        return (s0, d0)
    elif len(d0) == 0:
        # [Empty-D] Figure 6
        #
        # ----------------
        # σ;ϵ ⊦ xs ⇒δ σ;ϵ
        return (s0, d0)
    else:
        # [Pull] Figure 6
        # σ0 ; xs0 ⊦ δ0(X) ⇒pull σ'0 ; xs1
        # σ'0 ; δ0\δ0(X) ⊦ xs1 ⇒δ σ1 ; δ1
        # ---------------------------------
        # σ0 ; δ0 ⊦ X :: xs0 ⇒δ σ1 ; δ1

        X = xs[0]
        xs0 = xs[1:]

        # δ0(X)
        d0X = [z for z in d0 if occursInEq(X, z)]
        # δ0\δ0(X)
        d0wod0X = [z for z in d0 if not occursInEq(X, z)]

        sp0, xs1 = pull(s0, xs0, d0X)

        return evalDelta(sp0, d0wod0X, xs1)
