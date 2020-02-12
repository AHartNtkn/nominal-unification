from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

def test_freshVar():
    assert RhoMachine(fresh=20).freshVar() == Var("$X20")
    rm = RhoMachine(fresh=20)
    rm.freshVar()
    assert rm.freshVar() == Var("$X21")
    rm = RhoMachine(fresh=20)
    rm.freshAtom()
    assert rm.freshVar() == Var("$X21")

def test_freshAtom():
    assert RhoMachine(fresh=20).freshAtom() == "$a20"
    rm = RhoMachine(fresh=20)
    rm.freshAtom()
    assert rm.freshAtom() == "$a21"
    rm = RhoMachine(fresh=20)
    rm.freshVar()
    assert rm.freshAtom() == "$a21"

def test_stepRho():
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure("X", emptyBinderMap()), Closure(Var("x"), emptyBinderMap())))
    res1 = (rm.np, rm.dp, rm.s)
    testRes1 = ([NuEquation(Closure("X", emptyBinderMap()), Closure(Var("x"), emptyBinderMap()))], [], dict([]))
    assert str(res1) == str(testRes1)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure("X", emptyBinderMap()), Closure("Y", emptyBinderMap())))
    res2 = (rm.np, rm.dp, rm.s)
    testRes2 = ([NuEquation(Closure("X", emptyBinderMap()), Closure("Y", emptyBinderMap()))], [], dict([]))
    assert str(res2) == str(testRes2)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(Var("x"), emptyBinderMap()), Closure(Var("y"), emptyBinderMap())))
    res3 = (rm.np, rm.dp, rm.s)
    testRes3 = ([], [DeltaEquation(Closure(Var("x"), emptyBinderMap()), Closure(Var("y"), emptyBinderMap()))], dict([]))
    assert str(res3) == str(testRes3)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(Var("x"), emptyBinderMap()), Closure("X", emptyBinderMap())))
    res4 = (rm.np, rm.dp, rm.s)
    testRes4 = ([NuEquation(Closure("X", emptyBinderMap()), Closure(Var("x"), emptyBinderMap()))], [], dict([]))
    assert str(res4) == str(testRes4)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(App("X", Var("y")), emptyBinderMap()), Closure(App(Var("x"), Var("Y")), emptyBinderMap())))
    res5 = (rm.np, rm.dp, rm.s)
    testRes5 = ([NuEquation(Closure("X", emptyBinderMap()), Closure(Var("x"), emptyBinderMap()))],
                [DeltaEquation(Closure(Var("y"), emptyBinderMap()), Closure(Var("Y"), emptyBinderMap()))], dict([]))
    assert str(res5) == str(testRes5)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(App("X", Var("y")), emptyBinderMap()), Closure(App(Var("x"), "Y"), emptyBinderMap())))
    res6 = (rm.np, rm.dp, rm.s)
    testRes6 = ([NuEquation(Closure("Y", emptyBinderMap()), Closure(Var("y"), emptyBinderMap())),
                 NuEquation(Closure("X", emptyBinderMap()), Closure(Var("x"), emptyBinderMap()))],
                [], dict([]))
    assert str(res6) == str(testRes6)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(App("X", Var("y")), emptyBinderMap()), Closure(Var("Y"), emptyBinderMap())))
    res7 = (rm.np, rm.dp, rm.s)
    testRes7 = ([NuEquation(Closure("X", emptyBinderMap()), Closure(Var("$X0"), emptyBinderMap()))],
                [DeltaEquation(Closure(Var("$X1"), emptyBinderMap()), Closure(Var("y"), emptyBinderMap()))],
                {"Y":App(Var("$X0"),Var("$X1"))})
    assert str(res7) == str(testRes7)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(App("X", "y"), emptyBinderMap()), Closure(Var("Y"), emptyBinderMap())))
    res8 = (rm.np, rm.dp, rm.s)
    testRes8 = ([NuEquation(Closure("y", emptyBinderMap()), Closure(Var("$X1"), emptyBinderMap())),
                 NuEquation(Closure("X", emptyBinderMap()), Closure(Var("$X0"), emptyBinderMap()))],
                [],
                {"Y":App(Var("$X0"),Var("$X1"))})
    assert str(res8) == str(testRes8)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(App("X", "y"), emptyBinderMap()), Closure(App("x", "Y"), emptyBinderMap())))
    res9 = (rm.np, rm.dp, rm.s)
    testRes9 = ([NuEquation(Closure("y", emptyBinderMap()), Closure("Y", emptyBinderMap())),
                 NuEquation(Closure("X", emptyBinderMap()), Closure("x", emptyBinderMap()))],
                [], dict([]))
    assert str(res9) == str(testRes9)
    
    try:
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(App("X", "y"), emptyBinderMap()), Closure("Y", emptyBinderMap())))
        assert False
    except EEMismatchError:
        assert True
    
    try:
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(Abs("X", "y"), emptyBinderMap()), Closure("Y", emptyBinderMap())))
        assert False
    except EEMismatchError:
        assert True

    try:
        rm = RhoMachine()
        rm.step(MultiEquation(Closure("Y", emptyBinderMap()), Closure(App("X", "y"), emptyBinderMap())))
        assert False
    except EEMismatchError:
        assert True

    try:
        rm = RhoMachine()
        rm.step(MultiEquation(Closure("Y", emptyBinderMap()), Closure(Abs("X", "y"), emptyBinderMap())))
        assert False
    except EEMismatchError:
        assert True

    try:
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(Abs("X", "y"), emptyBinderMap()), Closure(App("X", "y"), emptyBinderMap())))
        assert False
    except EEMismatchError:
        assert True

    try:
        rm = RhoMachine()
        rm.step(MultiEquation(Closure(App("X", "y"), emptyBinderMap()), Closure(Abs("X", "y"), emptyBinderMap())))
        assert False
    except EEMismatchError:
        assert True
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(Abs("X", Var("y")), emptyBinderMap()), Closure(Abs("X", "Y"), emptyBinderMap())))
    res10 = (rm.np, rm.dp, rm.s)
    testRes10 = ([NuEquation(Closure("Y", BinderMap({"X":0}, {0:"X"})),
                             Closure(Var("y"), BinderMap({"X":0}, {0:"X"})))],
                [], dict([]))
    assert str(res10) == str(testRes10)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(Abs("X", Var("y")), emptyBinderMap()), Closure(Abs("x", "Y"), emptyBinderMap())))
    res11 = (rm.np, rm.dp, rm.s)
    testRes11 = ([NuEquation(Closure("Y", BinderMap({"x":0}, {0:"x"})),
                             Closure(Var("y"), BinderMap({"X":0}, {0:"X"})))],
                [], dict([]))
    assert str(res11) == str(testRes11)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(Abs("X", "y"), emptyBinderMap()), Closure(Abs("x", "Y"), emptyBinderMap())))
    res12 = (rm.np, rm.dp, rm.s)
    testRes12 = ([NuEquation(Closure("y", BinderMap({"X":0}, {0:"X"})),
                             Closure("Y", BinderMap({"x":0}, {0:"x"})))],
                [], dict([]))
    assert str(res12) == str(testRes12)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(Abs("X", Var("y")), emptyBinderMap()), Closure(Var("Y"), emptyBinderMap())))
    res13 = (rm.np, rm.dp, rm.s)
    testRes13 = ([],
                [DeltaEquation(Closure(Var("$X1"), BinderMap({"$a0":0}, {0:"$a0"})),
                               Closure(Var("y"), BinderMap({"X":0}, {0:"X"})))],
                {"Y":Abs("$a0",Var("$X1"))})
    assert str(res13) == str(testRes13)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(Abs("X", "y"), emptyBinderMap()), Closure(Var("Y"), emptyBinderMap())))
    res14 = (rm.np, rm.dp, rm.s)
    testRes14 = ([NuEquation(Closure("y", BinderMap({"X":0}, {0:"X"})),
                             Closure(Var("$X1"), BinderMap({"$a0":0}, {0:"$a0"})))],
                [],
                {"Y":Abs("$a0",Var("$X1"))})
    assert str(res14) == str(testRes14)
    
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(Abs("X", Var("y")), emptyBinderMap()), Closure(Abs("X", Var("Y")), emptyBinderMap())))
    res15 = (rm.np, rm.dp, rm.s)
    testRes15 = ([],
                 [DeltaEquation(Closure(Var("y"), BinderMap({"X":0}, {0:"X"})),
                                Closure(Var("Y"), BinderMap({"X":0}, {0:"X"})))],
                 dict([]))
    assert str(res15) == str(testRes15)
    
    expr161 = App("x", Abs("z", "w"))
    expr162 = App("x", Abs("y", "w"))
    rm = RhoMachine()
    rm.step(MultiEquation(Closure(expr161, emptyBinderMap()), Closure(expr162, emptyBinderMap())))
    res16 = (rm.np, rm.dp, rm.s)
    resTest16 = ([NuEquation(Closure("w", BinderMap({"z":0}, {0:"z"})),
                           Closure("w", BinderMap({"y":0}, {0:"y"}))),
                  NuEquation(Closure("x", emptyBinderMap()),
                           Closure("x", emptyBinderMap()))],
                [], dict([]))
    assert str(res16) == str(resTest16)

def test_evalRho():
    # To Do

    # expr1 = App(Var("X"), Abs("z", App("d", "z")))
    # expr2 = App("x", Abs("y", Var("Y")))
    
    pass
