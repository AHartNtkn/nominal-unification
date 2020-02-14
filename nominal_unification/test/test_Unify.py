from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *
from nominal_unification.NuMachines import *
from nominal_unification.DeltaMachines import *
from nominal_unification.RhoMachines import *

def test_unify():
    expr1 = App(Var("X"), Abs("z", App("d", "z")))
    expr2 = App("x", Abs("y", Var("Y")))

    res1 = unify(expr2, expr1)
    resTest1 = ({'Y': App(Var('$X0'), Var('$X1')), '$X1': 'y', '$X0': 'd', 'X': 'x'}, [])
    #resTest1 = ({"$X0": "d", "$X1": "y", "X": "x", "Y": App(Var("$X0"), Var("$X1"))}, [])
    
    assert str(res1) == str(resTest1)