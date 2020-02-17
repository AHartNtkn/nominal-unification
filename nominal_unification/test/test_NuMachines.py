import unittest

from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *
from nominal_unification.NuMachines import *

class TestNuMachines(unittest.TestCase):
    def test_stepNu(self):
        bm1 = extend("cool", extend("stuff", emptyScope()))
        bm2 = extend("neat", extend("stuff", emptyScope()))
        bm3 = extend("neat", extend("stuff", extend("too", emptyScope())))

        cl1s = Closure("stuff", bm1)
        cl2s = Closure("stuff", bm2)
        cl3s = Closure("stuff", bm3)

        cl1c = Closure("cool", bm1)
        cl2c = Closure("cool", bm2)

        cl1n = Closure("new", bm1)
        cl2n = Closure("new", bm2)
        
        cl1v = Closure(Var("stuff"), bm2)
        cl2v = Closure(Var("stuff"), bm3)
        cl3v = Closure(Var("new"), bm2)
        
        nm = NuMachine()
        nm.step(NuEquation(cl1s, cl1s))
        assert nm.subst == dict([])
        nm = NuMachine()
        nm.step(NuEquation(cl1s, cl2s))
        assert nm.subst == dict([])
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl1s, cl3s))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl1s, cl1c))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl1s, cl2c))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl1s, cl1n))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl1s, cl2n))
            assert False
        except NNMismatchError:
            assert True
        nm = NuMachine()
        nm.step(NuEquation(cl1s, cl1v))
        assert nm.subst == {'stuff':'stuff'}
        nm = NuMachine()
        nm.step(NuEquation(cl1s, cl2v))
        assert nm.subst == {'stuff':'too'}
        nm = NuMachine()
        nm.step(NuEquation(cl1s, cl3v))
        assert nm.subst == {'new':'stuff'}
        
        nm = NuMachine()
        nm.step(NuEquation(cl2s, cl2s))
        assert nm.subst == dict([])
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl2s, cl3s))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl2s, cl1c))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl2s, cl2c))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl2s, cl1n))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl2s, cl2n))
            assert False
        except NNMismatchError:
            assert True
        nm = NuMachine()
        nm.step(NuEquation(cl2s, cl1v))
        assert nm.subst == {'stuff':'stuff'}
        nm = NuMachine()
        nm.step(NuEquation(cl2s, cl2v))
        assert nm.subst == {'stuff':'too'}
        nm = NuMachine()
        nm.step(NuEquation(cl2s, cl3v))
        assert nm.subst == {'new':'stuff'}

        nm = NuMachine()
        nm.step(NuEquation(cl3s, cl3s))
        assert nm.subst == dict([])
        nm = NuMachine()
        nm.step(NuEquation(cl3s, cl1c))
        assert nm.subst == dict([])
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl3s, cl2c))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl3s, cl1n))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl3s, cl2n))
            assert False
        except NNMismatchError:
            assert True
        nm = NuMachine()
        nm.step(NuEquation(cl3s, cl1v))
        assert nm.subst == {'stuff':'neat'}
        nm = NuMachine()
        nm.step(NuEquation(cl3s, cl2v))
        assert nm.subst == {'stuff':'stuff'}
        nm = NuMachine()
        nm.step(NuEquation(cl3s, cl3v))
        assert nm.subst == {'new':'neat'}

        nm = NuMachine()
        nm.step(NuEquation(cl1c, cl1c))
        assert nm.subst == dict([])
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl1c, cl2c))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl1c, cl1n))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl1c, cl2n))
            assert False
        except NNMismatchError:
            assert True
        nm = NuMachine()
        nm.step(NuEquation(cl1c, cl1v))
        assert nm.subst == {'stuff':'neat'}
        nm = NuMachine()
        nm.step(NuEquation(cl1c, cl2v))
        assert nm.subst == {'stuff':'stuff'}
        nm = NuMachine()
        nm.step(NuEquation(cl1c, cl3v))
        assert nm.subst == {'new':'neat'}

        nm = NuMachine()
        nm.step(NuEquation(cl2c, cl2c))
        assert nm.subst == dict([])
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl2c, cl1n))
            assert False
        except NNMismatchError:
            assert True
        try:
            nm = NuMachine()
            nm.step(NuEquation(cl2c, cl2n))
            assert False
        except NNMismatchError:
            assert True
        nm = NuMachine()
        nm.step(NuEquation(cl2c, cl1v))
        assert nm.subst == {'stuff':'cool'}
        nm = NuMachine()
        nm.step(NuEquation(cl2c, cl2v))
        assert nm.subst == {'stuff':'cool'}
        nm = NuMachine()
        nm.step(NuEquation(cl2c, cl3v))
        assert nm.subst == {'new':'cool'}

        nm = NuMachine()
        nm.step(NuEquation(cl1n, cl1n))
        assert nm.subst == dict([])
        nm = NuMachine()
        nm.step(NuEquation(cl1n, cl2n))
        assert nm.subst == dict([])
        nm = NuMachine()
        nm.step(NuEquation(cl1n, cl1v))
        assert nm.subst == {'stuff':'new'}
        nm = NuMachine()
        nm.step(NuEquation(cl1n, cl2v))
        assert nm.subst == {'stuff':'new'}
        nm = NuMachine()
        nm.step(NuEquation(cl1n, cl3v))
        assert nm.subst == {'new':'new'}

        nm = NuMachine()
        nm.step(NuEquation(cl2n, cl2n))
        assert nm.subst == dict([])
        nm = NuMachine()
        nm.step(NuEquation(cl2n, cl1v))
        assert nm.subst == {'stuff':'new'}
        nm = NuMachine()
        nm.step(NuEquation(cl2n, cl2v))
        assert nm.subst == {'stuff':'new'}
        nm = NuMachine()
        nm.step(NuEquation(cl2n, cl3v))
        assert nm.subst == {'new':'new'}

    def test_evalNu(self):
        bm1 = extend("cool", extend("stuff", emptyScope()))
        bm2 = extend("neat", extend("stuff", emptyScope()))
        bm3 = extend("neat", extend("stuff", extend("too", emptyScope())))

        cl2s = Closure("stuff", bm2)

        cl1n = Closure("new", bm1)
        cl2n = Closure("new", bm2)
        
        cl1v = Closure(Var("stuff"), bm2)
        cl2v = Closure(Var("stuff"), bm3)
        cl3v = Closure(Var("new"), bm2)
        
        nprob = [NuEquation(cl1n, cl1n),
                 NuEquation(cl1n, cl2n),
                 NuEquation(cl1n, cl1v),
                 NuEquation(cl1n, cl2v),
                 NuEquation(cl2s, cl2v),
                 NuEquation(cl1n, cl3v)]
        
        nm = NuMachine()
        nm.eval(nprob)
        
        assert nm.subst == {"new":"new", "stuff":"too"}
        
        s1 = {"Y": (Var("$X0"), Var("$X1"))}
        np = [NuEquation(Closure("z", Scope({"z":0}, {0:"z"})),
                     Closure(Var("$X1"), Scope({"y":0}, {0:"y"}))),
              NuEquation(Closure("d", Scope({"z":0}, {0:"z"})),
                         Closure(Var("$X0"), Scope({"y":0}, {0:"y"})))]
        
        nu = NuMachine(s1)
        nu.eval(np)
        assert nu.subst == {"$X0":"d", "$X1":"y", "Y":(Var("$X0"),Var("$X1"))}
        
        s1 = {"Y": (Var("$X0"), Var("$X1"))}
        np = [NuEquation(Closure("z", Scope({"z":0}, {0:"z"})),
                     Closure(Var("$X1"), Scope({"y":0}, {0:"y"}))),
              NuEquation(Closure("d", Scope({"z":0}, {0:"z"})),
                         Closure(Var("$X0"), Scope({"y":0}, {0:"y"}))),
              NuEquation(Closure("x", emptyScope()),
                         Closure(Var("X"), emptyScope()))]
        
        nu = NuMachine(s1)
        nu.eval(np)
        assert nu.subst == {"$X0":"d", "$X1":"y", "X":"x", "Y":(Var("$X0"),Var("$X1"))}
        
        s1 = {}
        np = [NuEquation(Closure("x", Scope({"z":0}, {0:"z"})),
                         Closure(Var("Y"), Scope({"y":0}, {0:"y"})))]
        
        nu = NuMachine(s1)
        nu.eval(np)
        assert nu.subst == {"Y":"x"}

