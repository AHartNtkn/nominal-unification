import unittest

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
        resTest1 = {"$X0": "d", "$X1": "y", "X": "x", "Y": (Var("$X0"), Var("$X1"))}
        
        assert res1 == resTest1

        expr1 = ((Var("X"), "y"), Var("Z"), "w")
        expr2 = (("x", Var("Y")), "z", Var("W"))

        res2 = unify(expr1, expr2)
        resTest2 = {'W': 'w', 'X': 'x', 'Y': 'y', 'Z': 'z'}

        assert res2 == resTest2
        
        expr1 = (Var("X"), Abs("z", "x"))
        expr2 = (Var("Y"), Abs("y", Var("Y")))

        res3 = unify(expr1, expr2)
        resTest3 = {'X': 'x', 'Y': 'x'}
        
        assert res3 == resTest3
        
        res4 = unify(expr2, expr1)
        resTest4 = {'X': 'x', 'Y': 'x'}
        
        assert res4 == resTest4

        assert unify(Var('x'), 1) == {'x':1}

        assert unify((Var('x'), Var('y')), (1, 2)) == {'x':1, 'y':2}

        assert unify((1, Var('x')), (1, 2)) == {'x':2}

        assert unify((Var('x'), Var('x')), (1, 2)) == False

        assert unify(1, 1) == {}

        assert unify(1, 2) == False
