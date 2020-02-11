from nominal_unification.Exceptions import *

# Define basic syntax terms.

# Expressions, made up of atoms, variables, applications, and abstractions.
# An atom is just a string.

class Var():
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return "V(" + str(self.string) + ")"
    __repr__ = __str__

    def __eq__(self, other):
        return type(self) == type(other) and self.string == other.string

    def __lt__(self, other):
        return type(self) == type(other) and self.string < other.string
    
    def __hash__(self):
        return hash((type(self), self.string))
    

class App():
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def __str__(self):
        return "App(" + str(self.expr1) + ", " + str(self.expr2) + ")"
    __repr__ = __str__

    def __eq__(self, other):
        return type(self) == type(other) and self.expr1 == other.expr1 and self.expr2 == other.expr2
    
    def __hash__(self):
        return hash((type(self), self.expr1, self.expr2))

class Abs():
    def __init__(self, string, expr):
        self.string = string
        self.expr = expr

    def __str__(self):
        return "Abs(" + str(self.string) + ", " + str(self.expr) + ")"
    __repr__ = __str__

    def __eq__(self, other):
        return type(self) == type(other) and self.expr == other.expr and self.expr == other.expr
    
    def __hash__(self):
        return hash((type(self), self.expr1, self.expr2))

# expElim : Expr -> (String -> a) -> (String -> a) -> (Expr -> Expr -> a) -> 
def expElim(expr, atomElim, varElim, appElim, absElim):
    if type(expr) == str or type(expr) == int:
        return atomElim(expr)
    elif type(expr) == Var:
        return varElim(expr.string)
    elif type(expr) == App:
        return appElim(expr.expr1, expr.expr2)
    elif type(expr) == Abs:
        return absElim(expr.string, expr.expr)
    else:
        raise Exception(str(expr) + 'is not an expression')

# Equations
class Eq():
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def __str__(self):
        return "(" + str(self.expr1) + " = " + str(self.expr2) + ")"
    __repr__ = __str__

# Bound and free terms
class Bound():
    def __init__(self, string, index):
        self.string = string
        self.index = index

    def __str__(self):
        return "Bound(" + self.string + ", " + str(self.index) + ")"
    __repr__ = __str__

    def __eq__(self, other):
        return type(self) == type(other) and self.string == other.string and self.index == other.index

class Free():
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return "Free(" + self.string + ")"
    __repr__ = __str__

    def __eq__(self, other):
        return type(self) == type(other) and self.string == other.string

# Maps of binders.
class BinderMap():
    def __init__(self, a2i, i2a):
        self.a2i = a2i # Dict Atom Int
        self.i2a = i2a # Dict Int Atom

    def __str__(self):
        return "BM(" + str(self.a2i) + ", " + str(self.i2a) + ")"
    __repr__ = __str__

# extend : Atom -> BinderMap -> BinderMap
def extend(atom, binderMap):
    """ Add atom to map of binders.
    """
    size = len(binderMap.a2i)
    binderMap.a2i[atom] = size
    binderMap.i2a[size] = atom
    
    return binderMap

# lookupAtom : Atom -> BinderMap -> Boundness
def lookupAtom(atom, binderMap):
    index = binderMap.a2i.get(atom, -1)
    
    if index == -1:
        return Free(atom)
    
    return Bound(atom, index)

# lookupIdx : Int -> BinderMap -> Maybe Atom
def lookupIdx(index, binderMap):
    # j = len(binderMap.a2i) - index
    a = binderMap.i2a.get(index, -1)
    indexp = binderMap.a2i.get(a, -2)
    if index == indexp:
        return a
    
    raise NoMatchingBinderError(str(index) + "\n" + str(binderMap))

def emptyBinderMap():
    return BinderMap(dict([]), dict([]))