import unittest

from nominal_unification.Syntax import *
from nominal_unification.Constraints import *
from nominal_unification.RhoMachines import *

class TestRhoMachines(unittest.TestCase):
    def test_newVar(self):
        assert RhoMachine(fresh=20).newVar() == Var("$X20")
        rm = RhoMachine(fresh=20)
        rm.newVar()
        assert rm.newVar() == Var("$X21")
        rm = RhoMachine(fresh=20)
        rm.newName()
        assert rm.newVar() == Var("$X21")

    def test_newName(self):
        assert RhoMachine(fresh=20).newName() == "$a20"
        rm = RhoMachine(fresh=20)
        rm.newName()
        assert rm.newName() == "$a21"
        rm = RhoMachine(fresh=20)
        rm.newVar()
        assert rm.newName() == "$a21"

    def test_stepRho(self):
        rm = RhoMachine()
        rm.step(MultiEquation(Closure("X", emptyScope()), Closure(Var("x"), emptyScope())))
        res1 = (rm.p, rm.d, rm.s)
        testRes1 = ([NuEquation(Closure("X", emptyScope()), Closure(Var("x"), emptyScope()))], [], dict([]))
        assert str(res1) == str(testRes1)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure("X", emptyScope()), Closure("Y", emptyScope())))
        res2 = (rm.p, rm.d, rm.s)
        testRes2 = ([NuEquation(Closure("X", emptyScope()), Closure("Y", emptyScope()))], [], dict([]))
        assert str(res2) == str(testRes2)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(Var("x"), emptyScope()), Closure(Var("y"), emptyScope())))
        res3 = (rm.p, rm.d, rm.s)
        testRes3 = ([], [DeltaEquation(Closure(Var("x"), emptyScope()), Closure(Var("y"), emptyScope()))], dict([]))
        assert str(res3) == str(testRes3)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(Var("x"), emptyScope()), Closure("X", emptyScope())))
        res4 = (rm.p, rm.d, rm.s)
        testRes4 = ([NuEquation(Closure("X", emptyScope()), Closure(Var("x"), emptyScope()))], [], dict([]))
        assert str(res4) == str(testRes4)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(("X", Var("y")), emptyScope()), Closure((Var("x"), Var("Y")), emptyScope())))
        res5 = (rm.p, rm.d, rm.s)
        testRes5 = ([NuEquation(Closure("X", emptyScope()), Closure(Var("x"), emptyScope()))],
                    [DeltaEquation(Closure(Var("y"), emptyScope()), Closure(Var("Y"), emptyScope()))], dict([]))
        assert str(res5) == str(testRes5)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(("X", Var("y")), emptyScope()), Closure((Var("x"), "Y"), emptyScope())))
        res6 = (rm.p, rm.d, rm.s)
        testRes6 = ([NuEquation(Closure("Y", emptyScope()), Closure(Var("y"), emptyScope())),
                     NuEquation(Closure("X", emptyScope()), Closure(Var("x"), emptyScope()))],
                    [], dict([]))
        assert str(res6) == str(testRes6)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(("X", Var("y")), emptyScope()), Closure(Var("Y"), emptyScope())))
        res7 = (rm.p, rm.d, rm.s)
        testRes7 = ([NuEquation(Closure("X", emptyScope()), Closure(Var("$X0"), emptyScope()))],
                    [DeltaEquation(Closure(Var("$X1"), emptyScope()), Closure(Var("y"), emptyScope()))],
                    {"Y":(Var("$X0"),Var("$X1"))})
        assert str(res7) == str(testRes7)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(("X", "y"), emptyScope()), Closure(Var("Y"), emptyScope())))
        res8 = (rm.p, rm.d, rm.s)
        testRes8 = ([NuEquation(Closure("y", emptyScope()), Closure(Var("$X1"), emptyScope())),
                     NuEquation(Closure("X", emptyScope()), Closure(Var("$X0"), emptyScope()))],
                    [],
                    {"Y":(Var("$X0"),Var("$X1"))})
        assert str(res8) == str(testRes8)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(("X", "y"), emptyScope()), Closure(("x", "Y"), emptyScope())))
        res9 = (rm.p, rm.d, rm.s)
        testRes9 = ([NuEquation(Closure("y", emptyScope()), Closure("Y", emptyScope())),
                     NuEquation(Closure("X", emptyScope()), Closure("x", emptyScope()))],
                    [], dict([]))
        assert str(res9) == str(testRes9)
        
        try:
            rm = RhoMachine()
            rm.step(MultiEquation(Closure(("X", "y"), emptyScope()), Closure("Y", emptyScope())))
            assert False
        except Exception:
            assert True
        
        try:
            rm = RhoMachine()
            rm.step(MultiEquation(Closure(Abs("X", "y"), emptyScope()), Closure("Y", emptyScope())))
            assert False
        except Exception:
            assert True

        try:
            rm = RhoMachine()
            rm.step(MultiEquation(Closure("Y", emptyScope()), Closure(("X", "y"), emptyScope())))
            assert False
        except Exception:
            assert True

        try:
            rm = RhoMachine()
            rm.step(MultiEquation(Closure("Y", emptyScope()), Closure(Abs("X", "y"), emptyScope())))
            assert False
        except Exception:
            assert True

        try:
            rm = RhoMachine()
            rm.step(MultiEquation(Closure(Abs("X", "y"), emptyScope()), Closure(("X", "y"), emptyScope())))
            assert False
        except Exception:
            assert True

        try:
            rm = RhoMachine()
            rm.step(MultiEquation(Closure(("X", "y"), emptyScope()), Closure(Abs("X", "y"), emptyScope())))
            assert False
        except Exception:
            assert True
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(Abs("X", Var("y")), emptyScope()), Closure(Abs("X", "Y"), emptyScope())))
        res10 = (rm.p, rm.d, rm.s)
        testRes10 = ([NuEquation(Closure("Y", Scope({"X":0}, {0:"X"})),
                                 Closure(Var("y"), Scope({"X":0}, {0:"X"})))],
                    [], dict([]))
        assert str(res10) == str(testRes10)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(Abs("X", Var("y")), emptyScope()), Closure(Abs("x", "Y"), emptyScope())))
        res11 = (rm.p, rm.d, rm.s)
        testRes11 = ([NuEquation(Closure("Y", Scope({"x":0}, {0:"x"})),
                                 Closure(Var("y"), Scope({"X":0}, {0:"X"})))],
                    [], dict([]))
        assert str(res11) == str(testRes11)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(Abs("X", "y"), emptyScope()), Closure(Abs("x", "Y"), emptyScope())))
        res12 = (rm.p, rm.d, rm.s)
        testRes12 = ([NuEquation(Closure("y", Scope({"X":0}, {0:"X"})),
                                 Closure("Y", Scope({"x":0}, {0:"x"})))],
                    [], dict([]))
        assert str(res12) == str(testRes12)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(Abs("X", Var("y")), emptyScope()), Closure(Var("Y"), emptyScope())))
        res13 = (rm.p, rm.d, rm.s)
        testRes13 = ([],
                    [DeltaEquation(Closure(Var("$X1"), Scope({"$a0":0}, {0:"$a0"})),
                                   Closure(Var("y"), Scope({"X":0}, {0:"X"})))],
                    {"Y":Abs("$a0",Var("$X1"))})
        assert str(res13) == str(testRes13)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(Abs("X", "y"), emptyScope()), Closure(Var("Y"), emptyScope())))
        res14 = (rm.p, rm.d, rm.s)
        testRes14 = ([NuEquation(Closure("y", Scope({"X":0}, {0:"X"})),
                                 Closure(Var("$X1"), Scope({"$a0":0}, {0:"$a0"})))],
                    [],
                    {"Y":Abs("$a0",Var("$X1"))})
        assert str(res14) == str(testRes14)
        
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(Abs("X", Var("y")), emptyScope()), Closure(Abs("X", Var("Y")), emptyScope())))
        res15 = (rm.p, rm.d, rm.s)
        testRes15 = ([],
                     [DeltaEquation(Closure(Var("y"), Scope({"X":0}, {0:"X"})),
                                    Closure(Var("Y"), Scope({"X":0}, {0:"X"})))],
                     dict([]))
        assert str(res15) == str(testRes15)
        
        expr161 = ("x", Abs("z", "w"))
        expr162 = ("x", Abs("y", "w"))
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(expr161, emptyScope()), Closure(expr162, emptyScope())))
        res16 = (rm.p, rm.d, rm.s)
        resTest16 = ([NuEquation(Closure("w", Scope({"z":0}, {0:"z"})),
                               Closure("w", Scope({"y":0}, {0:"y"}))),
                      NuEquation(Closure("x", emptyScope()),
                               Closure("x", emptyScope()))],
                      [], dict([]))
        assert str(res16) == str(resTest16)

    def test_evalRho(self):
        expr1 = (Var("X"), Abs("z", ("d", "z")))
        expr2 = (Var("Y"), Abs("y", Var("Y")))

        rm = RhoMachine()
        rm.eval([MultiEquation(Closure(expr1, emptyScope()),
                               Closure(expr2, emptyScope()))])

        res1 = (rm.p, rm.d, rm.s)
        resTest1 = (
         [NuEquation(Closure("z", Scope({"z":0}, {0:"z"})),
                     Closure(Var("$X1"), Scope({"y":0}, {0:"y"}))),
          NuEquation(Closure("d", Scope({"z":0}, {0:"z"})),
                     Closure(Var("$X0"), Scope({"y":0}, {0:"y"})))],
         [DeltaEquation(Closure(Var("X"), emptyScope()),
                        Closure(Var("Y"), emptyScope()))],
         {"Y": (Var("$X0"), Var("$X1"))}
         )
        
        assert str(res1) == str(resTest1)
        
        expr1 = (Var("X"), Abs("z", ("d", "z")))
        expr2 = ("x", Abs("y", Var("Y")))

        rm = RhoMachine()
        rm.eval([MultiEquation(Closure(expr1, emptyScope()),
                               Closure(expr2, emptyScope()))])

        res2 = (rm.p, rm.d, rm.s)
        resTest2 = (
         [NuEquation(Closure("z", Scope({"z":0}, {0:"z"})),
                     Closure(Var("$X1"), Scope({"y":0}, {0:"y"}))),
          NuEquation(Closure("d", Scope({"z":0}, {0:"z"})),
                     Closure(Var("$X0"), Scope({"y":0}, {0:"y"}))),
          NuEquation(Closure("x", emptyScope()),
                     Closure(Var("X"), emptyScope()))],
         [],
         {"Y": (Var("$X0"), Var("$X1"))}
         )
        
        assert str(res2) == str(resTest2)
        
        l = (Var("X"), Abs("z", "x"))
        r = (Var("Y"), Abs("y", Var("Y")))

        rm = RhoMachine()
        rm.eval([MultiEquation(Closure(l, emptyScope()),
                               Closure(r, emptyScope()))])
        
        res3 = (rm.p, rm.d, rm.s)
        resTest3 = (
            [NuEquation(Closure("x", Scope({"z":0}, {0:"z"})),
                        Closure(Var("Y"), Scope({"y":0}, {0:"y"})))],
            [DeltaEquation(Closure(Var("X"), emptyScope()),
                           Closure(Var("Y"), emptyScope()))],
            {}
        )
        
        assert str(res3) == str(resTest3)
        
        l = (Var("X"), Abs("z", "x"))
        r = (Var("Y"), Abs("y", Var("Y")))

        rm = RhoMachine()
        rm.eval([MultiEquation(Closure(r, emptyScope()),
                               Closure(l, emptyScope()))])
        
        res4 = (rm.p, rm.d, rm.s)
        resTest4 = (
            [NuEquation(Closure("x", Scope({"z":0}, {0:"z"})),
                        Closure(Var("Y"), Scope({"y":0}, {0:"y"})))],
            [DeltaEquation(Closure(Var("Y"), emptyScope()),
                           Closure(Var("X"), emptyScope()))],
            {}
        )
        
        assert str(res4) == str(resTest4)
