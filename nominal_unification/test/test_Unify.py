import unittest

from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *
from nominal_unification.NuMachines import *
from nominal_unification.DeltaMachines import *
from nominal_unification.RhoMachines import *
from nominal_unification.Unify import *

class TestUnift(unittest.TestCase):
    def test_unify(self):
        expr1 = (Var("X"), Abs("z", ("d", "z")))
        expr2 = ("x", Abs("y", Var("Y")))

        res1 = unify(expr2, expr1)
        resTest1 = ({"$X0": "d", "$X1": "y", "X": "x", "Y": (Var("$X0"), Var("$X1"))}, [])
        
        assert res1 == resTest1