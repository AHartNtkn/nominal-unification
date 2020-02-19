import unittest

from nominal_unification.Syntax import *
from nominal_unification.Constraints import *
from nominal_unification.DeltaMachines import *

class TestDeltaMachines(unittest.TestCase):
    def test_occursInEq(self):
        bm2 = extend("neat", extend("stuff", emptyScope()))
        bm3 = extend("neat", extend("stuff", extend("too", emptyScope())))
        
        cl1v = Closure(Var("stuff"), bm2)
        cl2v = Closure(Var("stuff"), bm3)
        cl3v = Closure(Var("new"), bm2)
        
        eq1 = DeltaEquation(cl1v, cl1v)
        eq2 = DeltaEquation(cl1v, cl2v)
        eq3 = DeltaEquation(cl1v, cl3v)
        eq4 = DeltaEquation(cl2v, cl2v)
        eq5 = DeltaEquation(cl2v, cl3v)
        eq6 = DeltaEquation(cl3v, cl3v)
        
        assert occursInEq(Var("stuff"), eq1) == True
        assert occursInEq(Var("new"), eq1) == False
        assert occursInEq(Var("stuff"), eq2) == True
        assert occursInEq(Var("new"), eq2) == False
        assert occursInEq(Var("stuff"), eq3) == True
        assert occursInEq(Var("new"), eq3) == True
        assert occursInEq(Var("stuff"), eq4) == True
        assert occursInEq(Var("new"), eq4) == False
        assert occursInEq(Var("stuff"), eq5) == True
        assert occursInEq(Var("new"), eq5) == True
        assert occursInEq(Var("stuff"), eq6) == False
        assert occursInEq(Var("new"), eq6) == True

    def test_evalDelta(self):
        dp = [DeltaEquation(Closure(Var("X"), emptyScope()),
                            Closure(Var("Y"), emptyScope()))]
        s2 = {"$X0":"d", "$X1":"y", "Y":(Var("$X0"),Var("$X1"))}
        
        res = evalDelta(s2, dp, list(map(Var, s2.keys())))
        resTest = ({"$X0":"d","$X1":"y","X":(Var("$X0"),Var("$X1")),"Y":(Var("$X0"), Var("$X1"))},[])

        assert res == resTest
        
        dp = []
        s2 = {"$X0":"d", "$X1":"y", "X":"x", "Y":(Var("$X0"),Var("$X1"))}
        res2 = evalDelta(s2, dp, list(map(Var, s2.keys())))
        resTest2 = ({"$X0":"d","$X1":"y","X":"x","Y":(Var("$X0"), Var("$X1"))},[])
        
        assert str(res2) == str(resTest2)
        
        s = {'Y': 'x'}
        d = [DeltaEquation(Closure(Var("Y"), emptyScope()),
                           Closure(Var("X"), emptyScope()))]
        
        res3 = evalDelta(s, d, list(map(Var, s.keys())))
        resTest3 = ({"X":"x", "Y":"x"},[])
        
        assert res3 == resTest3
        
        s = {'Y': 'x'}
        d = [DeltaEquation(Closure(Var("X"), emptyScope()),
                           Closure(Var("Y"), emptyScope()))]
        
        res4 = evalDelta(s, d, list(map(Var, s.keys())))
        resTest4 = ({"X":"x", "Y":"x"}, [])
        
        assert res4 == resTest4

    def test_pull(self):
        s = {'Y': 'x'}
        d = [DeltaEquation(Closure(Var("Y"), emptyScope()),
                           Closure(Var("X"), emptyScope()))]
        
        res1 = pull(s, [], d)
        resTest1 = ({"X":"x", "Y":"x"}, [Var("X")])
        
        assert res1 == resTest1

        s = {'Y': 'x', 'X':'x'}
        d = [DeltaEquation(Closure(Var("Y"), emptyScope()),
                           Closure(Var("X"), emptyScope()))]
        
        res2 = pull(s, [], d)
        resTest2 = ({"X":"x", "Y":"x"}, [])
        
        assert res2 == resTest2

        s = {'X': 'x'}
        d = [DeltaEquation(Closure(Var("Y"), emptyScope()),
                           Closure(Var("X"), emptyScope()))]
        
        res3 = pull(s, [], d)
        resTest3 = ({"X":"x", "Y":"x"}, [Var("Y")])
        
        assert res3 == resTest3

        try:
            s = {}
            d = [DeltaEquation(Closure(Var("Y"), emptyScope()),
                               Closure(Var("X"), emptyScope()))]
            
            pull(s, [], d)
            assert False
        except UnificationError:
            assert True

        try:
            s = {"X":"x", "Y":"y"}
            d = [DeltaEquation(Closure(Var("Y"), emptyScope()),
                               Closure(Var("X"), emptyScope()))]
            
            pull(s, [], d)
            assert False
        except UnificationError:
            assert True
