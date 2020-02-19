class UnificationError(Exception):
    pass

def isName(x):
    """ Check if the input is a valid name.

        Names should consist of any constant, e.g. strings or integers.
    """
    return isinstance(x, str) or isinstance(x, int)


class Var():
    """ Metavariables used for unification.
    """

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return "V(" + str(self.string) + ")"
    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.string == other.string

    def __lt__(self, other):
        return isinstance(self, type(other)) and self.string < other.string

    def __hash__(self):
        return hash((type(self), self.string))


class Abs():
    """ Represents abstractions used to indicate when a variable is being
        bound. For example, we might represent a lamdba expression
        "lam x . f x" as ("lam", Abs(x, f(x))), or a universal quantification
        "forall x . P(x)" as ("all", Abs(x, P(x))).
    """

    def __init__(self, string, expr):
        self.string = string
        self.expr = expr

    def __str__(self):
        return "(" + str(self.string) + " . " + str(self.expr) + ")"
    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(
            self, type(other)) and self.string == other.string and self.expr == other.expr

    def __hash__(self):
        return hash((type(self), self.expr1, self.expr2))

# Bound and free terms


class Bound():
    """ Represents a bound term. When a variable "x" is bound by the most recent
        abstraction it will be cast as Bound("x", 0), for example.
    """

    def __init__(self, string, index):
        self.string = string
        self.index = index

    def __str__(self):
        return "Bound(" + self.string + ", " + str(self.index) + ")"
    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(
            self,
            type(other)) and self.string == other.string and self.index == other.index


class Free():
    """ Represents a free variable. Comes up in contexts where variables might
        be bound.
    """

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return "Free(" + self.string + ")"
    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.string == other.string

# Maps of binders.


class Scope():
    """ A scope is a list of bound variables, denoting mappings from variables
        to indices, and from indices back into variables.
    """

    def __init__(self, n2i, i2n):
        self.n2i = n2i  # Dict Name Int
        self.i2n = i2n  # Dict Int Name

    def __str__(self):
        return "S(" + str(self.n2i) + ", " + str(self.i2n) + ")"
    __repr__ = __str__

# extend : Name -> Scope -> Scope


def extend(name, scope):
    """ Add a name to a scope.
    """
    size = len(scope.n2i)
    bmp = Scope(scope.n2i.copy(), scope.i2n.copy())

    bmp.n2i[name] = size
    bmp.i2n[size] = name

    return bmp

# lookupName : Name -> Scope -> Boundness


def lookupName(name, scope):
    """ Given a scope, try finding a name in that scope. If the name is bound,
        it's cast as a bound variable, if it's not bound its cast as a free
        variable.

        See [Free] and [Bound] in Figure 1.
    """

    # [Free] Figure 2
    # a ∉ Φ
    # --------
    # Φ ⊦ Fr a
    index = scope.n2i.get(name, -1)
    if index == -1:
        return Free(name)

    # [Bound] Figure 2
    # (Φ.n2i[a]) = i
    # (Φ.i2n[i]) = a
    # --------------
    # Φ ⊦ Bd a i
    if scope.i2n[index] == name:
        return Bound(name, index)

    raise UnificationError("Scope " + str(scope) + " is not well-formed.")

# lookupIdx : Int -> Scope -> Maybe Name


def lookupIdx(index, scope):
    """ Given an index and a scope, attempt to find the name matching that
        scope.

        Takes an integer index and a scope as input.
    """
    a = scope.i2n.get(index, -1)
    indexp = scope.n2i.get(a, -2)
    if index == indexp:
        return a

    raise UnificationError(str(index) + "\n" + str(scope))


def emptyScope():
    """ Generate a scope without any bindings.
    """
    return Scope(dict([]), dict([]))
