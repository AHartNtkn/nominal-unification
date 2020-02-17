from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *


class NuMachine():
    """ This machine interacts with a list of name-name and name-variable
        constraint equations for the purpose of building up a substitution
        map unifying them.
    """

    def __init__(self, subst=None):
        if subst is None:
            self.subst = dict([])
        else:
            self.subst = subst

    def step(self, nuEq):
        """ Given a nu equation, this will generate the appropriate
            substitution satisfying them.

            If it gets an NN equation, it checks that the names match. If they
            don't the constraint is unsatisfyable, otherwise the equation is
            discharged without changing anything (since nothing has to be
            substituted to satisfy the constraint.)

            If it gets an NV equation, it must find some name which is equal to
            the name in the first closure while not being captured in the scope
            of the second closure. It searches for such a name. If the name in
            the first closure is bound its scope, an appropriate bound variable
            at the same index in the second scope is selected. If the name in
            the first scope isn't bound, a new free variable with the same name
            is selected.

            In the original white paper, this machine is denoted by the
            judgement σ0 ⊦ ν ⇒ν σ1, where σ0 is an input substitution, ν is an
            input nu problem, and σ1 is an ouput substitution.

            See [N-V] and [N-N] in Figure 5.
        """
        clo1 = nuEq.clo1
        clo2 = nuEq.clo2

        a1 = clo1.expr
        Phi1 = clo1.scope

        if nuEq.var:
            # [N-V] Figure 5
            # 〈a1; Φ1〉≈〈a2; Φ2〉
            # {X2 / a2} ∪ σ0 ⊦ p ⇒ν σ1
            # ------------------------------------
            # σ0 ⊦〈a1; Φ1〉=NV〈X2; Φ2〉, p ⇒ν σ1

            X2 = clo2.expr
            Phi2 = clo2.scope

            res = lookupName(a1, Phi1)
            if isinstance(res, Free):
                a2 = lookupName(a1, Phi2)
                if isinstance(a2, Free):
                    # {X2 / a2} ∪ σ0
                    self.subst[X2.string] = a2.string
                else:
                    # Perhapse there's an implementation that avoids this?
                    # Fresh variable names?
                    raise NameCaptureError(str(a1) + "\n" + str(Phi1))
            elif isinstance(res, Bound):
                a2 = lookupIdx(res.index, Phi2)
                # {X2 / a2} ∪ σ0
                self.subst[X2.string] = a2
        else:
            # [N-N] Figure 5
            # 〈a1; Φ1〉≈〈a2; Φ2〉
            # σ0 ⊦ p ⇒ν σ1
            # ------------------------------------
            # σ0 ⊦〈a1; Φ1〉=NN〈a2; Φ2〉, p ⇒ν σ1
            if alphaEq(clo1, clo2):
                pass
            else:
                raise NNMismatchError(str(clo1) + "\n" + str(clo2))

    def eval(self, nuProb):
        """ Given a nu problem, it goes through each in sequence, making
            appropriate additions to the substitution its building.

            In the original white paper, this machine is denoted by the
            judgment σ0 ⊦ ν ⇒ν σ1, where σ0 is an input substitution, ν is an
            input nu problem, and σ1 is an ouput substitution.

            See [Empty] in Figure 5
        """
        # [Empty] Figure 5
        #
        # -------------
        # σ0 ⊦ ϵ ⇒ν σ0
        for eq in nuProb:
            self.step(eq)
