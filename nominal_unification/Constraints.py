from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *


class Closure():
    """ A closure represents an expression within a context with bindings.
        Variables within said expression may or may not be captured by the
        scope.
    """

    def __init__(self, expr, scope):
        self.expr = expr
        self.scope = scope

    def __str__(self):
        return "〈" + str(self.expr) + "; " + str(self.scope) + "〉"
    __repr__ = __str__


def alphaEq(clo1, clo2):
    """ Test if two closures are equivalent. Determines the alpha-equivalence
        of two expressions with respect to their scopes.

        1. If both terms are free in their respective scopes and have the same
        string, then the closures are equivalent.

        2. If both are bound by their respective scopes at the same index then
        they are also the same closure, even if the terms have different
        strings.

        3. They are not the same closure, otherwise.

        See [Same-Free] and [Same-Bound] in Figure 1.
    """

    l1 = lookupName(clo1.expr, clo1.scope)
    l2 = lookupName(clo2.expr, clo2.scope)

    # [Same-Free] Figure 3
    # a1 = a2
    # Φ1 ⊦ Fr a1
    # Φ2 ⊦ Fr a2
    # -------------------
    # 〈a1; Φ1〉≈〈a2; Φ2〉
    if isinstance(l1, Free) and isinstance(l2, Free):
        return clo1.expr == clo2.expr

    # [Same-Bound] Figure 3
    # i1 = i2
    # Φ1 ⊦ Bd a1 i1
    # Φ2 ⊦ Bd a2 i2
    # -------------------
    # 〈a1; Φ1〉≈〈a2; Φ2〉
    elif isinstance(l1, Bound) and isinstance(l2, Bound):
        return l1.index == l2.index

    else:
        return False


class NuEquation():
    """ Represents constraint equations between expressions which are either
        names or variables. The first term in the equation should always be a
        name, while the second is either a name (an NN problem) or a variable
        (an NV problem).

        These equations are used by nu machines to derive maps from variables
        to names.

        A "Nu Problem" is a list of Nu Equations.

        See Figure 4.
    """

    def __init__(self, clo1, clo2):
        if not isName(clo1.expr):
            raise Exception(
                "First argument, " +
                str(clo1) +
                ", of Nu Equation must be a name.")

        if not isName(clo2.expr) and not isinstance(clo2.expr, Var):
            raise Exception(
                "Second argument, " +
                str(clo2) +
                ", of Nu Equation must be a name or a variable.")

        self.clo1 = clo1  # Clo Name
        self.clo2 = clo2
        self.var = isinstance(clo2.expr, Var)
        # If self.var is true, then self.clo2 will be a closure over
        # a Var, otherwise it's a closure over an Name.

    def __str__(self):
        if self.var:
            return "(" + str(self.clo1) + " ≈NV " + str(self.clo2) + ")"
        else:
            return "(" + str(self.clo1) + " ≈NN " + str(self.clo2) + ")"
    __repr__ = __str__


class DeltaEquation():
    """ Represents constraint equations between expressions which are variables
        (a VV problem).

        These equations are used by delta machines to derive unifiers between
        sets of variables.

        A "Delta Problem" is a list of Delta Equations.

        See Figure 4.
    """

    def __init__(self, clo1, clo2):
        if not isinstance(clo1.expr, Var):
            raise Exception(
                "First argument, " +
                str(clo1) +
                ", of Delta Equation must be a variable.")

        if not isinstance(clo2.expr, Var):
            raise Exception(
                "Second argument, " +
                str(clo2) +
                ", of Delta Equation must be a variable.")

        self.clo1 = clo1  # Clo Var
        self.clo2 = clo2  # Clo Var

    def __str__(self):
        return "(" + str(self.clo1) + " ≈VV " + str(self.clo2) + ")"
    __repr__ = __str__


class MultiEquation():
    """ Represents a constraint equation between two expressions.

        Used by rho machines to compute the nu problems and delta problems to
        be fed into the nu and delta machines.

        A "Rho Problem" is a list of MultiEquations.

        See Figure 7.
    """

    def __init__(self, clo1, clo2):
        self.clo1 = clo1  # Clo Expr
        self.clo2 = clo2  # Clo Expr

    def __str__(self):
        return "(" + str(self.clo1) + " ≈ " + str(self.clo2) + ")"
    __repr__ = __str__


def extendSubst(var, expr, sub):
    """ Given a variable and an expression it should be substituted for, extend
        the substitution with that mapping.

        This exists as a non-stateful way to extend substitutions. That is,
        this creates a new substitution, rather than modifying an existing one.
    """
    subp = sub.copy()
    subp[var.string] = expr
    return subp
