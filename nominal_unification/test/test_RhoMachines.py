from pymonad import *

from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

def test_freshVar():
    assert freshVar().getResult(20) == Var("$X20")

def test_freshAtom():
    assert freshAtom().getResult(20) == "$a20"

def test_stepRho():
    res1 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure("X", emptyBinderMap()), Closure(Var("x"), emptyBinderMap()))))

    testRes1 = ([NuEquation(Closure("X", emptyBinderMap()), Closure(Var("x"), emptyBinderMap()))], [], dict([]))
    
    assert str(res1) == str(testRes1)
    
    res2 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure("X", emptyBinderMap()), Closure("Y", emptyBinderMap()))))

    testRes2 = ([NuEquation(Closure("X", emptyBinderMap()), Closure("Y", emptyBinderMap()))], [], dict([]))
    
    assert str(res2) == str(testRes2)
    
    res3 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(Var("x"), emptyBinderMap()), Closure(Var("y"), emptyBinderMap()))))

    testRes3 = ([], [DeltaEquation(Closure(Var("x"), emptyBinderMap()), Closure(Var("y"), emptyBinderMap()))], dict([]))
    
    assert str(res3) == str(testRes3)
    
    res4 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(Var("x"), emptyBinderMap()), Closure("X", emptyBinderMap()))))

    testRes4 = ([NuEquation(Closure("X", emptyBinderMap()), Closure(Var("x"), emptyBinderMap()))], [], dict([]))
    
    assert str(res4) == str(testRes4)
    
    res5 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(App("X", Var("y")), emptyBinderMap()), Closure(App(Var("x"), Var("Y")), emptyBinderMap()))))

    testRes5 = ([NuEquation(Closure("X", emptyBinderMap()), Closure(Var("x"), emptyBinderMap()))],
                [DeltaEquation(Closure(Var("y"), emptyBinderMap()), Closure(Var("Y"), emptyBinderMap()))], dict([]))
    
    assert str(res5) == str(testRes5)
    
    res6 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(App("X", Var("y")), emptyBinderMap()), Closure(App(Var("x"), "Y"), emptyBinderMap()))))

    testRes6 = ([NuEquation(Closure("Y", emptyBinderMap()), Closure(Var("y"), emptyBinderMap())),
                 NuEquation(Closure("X", emptyBinderMap()), Closure(Var("x"), emptyBinderMap()))],
                [], dict([]))
    
    assert str(res6) == str(testRes6)
    
    res7 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(App("X", Var("y")), emptyBinderMap()), Closure(Var("Y"), emptyBinderMap()))))

    testRes7 = ([NuEquation(Closure("X", emptyBinderMap()), Closure(Var("$X0"), emptyBinderMap()))],
                [DeltaEquation(Closure(Var("$X1"), emptyBinderMap()), Closure(Var("y"), emptyBinderMap()))],
                {"Y":App(Var("$X0"),Var("$X1"))})
    
    assert str(res7) == str(testRes7)
    
    res8 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(App("X", "y"), emptyBinderMap()), Closure(Var("Y"), emptyBinderMap()))))

    testRes8 = ([NuEquation(Closure("y", emptyBinderMap()), Closure(Var("$X1"), emptyBinderMap())),
                 NuEquation(Closure("X", emptyBinderMap()), Closure(Var("$X0"), emptyBinderMap()))],
                [],
                {"Y":App(Var("$X0"),Var("$X1"))})
    
    assert str(res8) == str(testRes8)
    
    res9 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(App("X", "y"), emptyBinderMap()), Closure(App("x", "Y"), emptyBinderMap()))))

    testRes9 = ([NuEquation(Closure("y", emptyBinderMap()), Closure("Y", emptyBinderMap())),
                 NuEquation(Closure("X", emptyBinderMap()), Closure("x", emptyBinderMap()))],
                [], dict([]))
    
    assert str(res9) == str(testRes9)
    
    try:
        runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(App("X", "y"), emptyBinderMap()), Closure("Y", emptyBinderMap()))))
        assert False
    except EEMismatchError:
        assert True

    try:
        runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(Abs("X", "y"), emptyBinderMap()), Closure("Y", emptyBinderMap()))))
        assert False
    except EEMismatchError:
        assert True

    try:
        runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure("Y", emptyBinderMap()), Closure(App("X", "y"), emptyBinderMap()))))
        assert False
    except EEMismatchError:
        assert True

    try:
        runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure("Y", emptyBinderMap()), Closure(Abs("X", "y"), emptyBinderMap()))))
        assert False
    except EEMismatchError:
        assert True

    try:
        runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(Abs("X", "y"), emptyBinderMap()), Closure(App("X", "y"), emptyBinderMap()))))
        assert False
    except EEMismatchError:
        assert True

    try:
        runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(App("X", "y"), emptyBinderMap()), Closure(Abs("X", "y"), emptyBinderMap()))))
        assert False
    except EEMismatchError:
        assert True
    
    # Note: none of the testRes from here on are properly made.
    
    res10 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(Abs("X", Var("y")), emptyBinderMap()), Closure(Abs("X", "Y"), emptyBinderMap()))))

    testRes10 = ([NuEquation(Closure("Y", BinderMap({"X":0}, {0:"X"})),
                             Closure(Var("y"), BinderMap({"X":0}, {0:"X"})))],
                [], dict([]))
    
    assert str(res10) == str(testRes10)
    
    res11 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(Abs("X", Var("y")), emptyBinderMap()), Closure(Abs("x", "Y"), emptyBinderMap()))))

    testRes11 = ([NuEquation(Closure("Y", BinderMap({"x":0}, {0:"x"})),
                             Closure(Var("y"), BinderMap({"X":0}, {0:"X"})))],
                [], dict([]))
    
    assert str(res11) == str(testRes11)
    
    res12 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(Abs("X", "y"), emptyBinderMap()), Closure(Abs("x", "Y"), emptyBinderMap()))))

    testRes12 = ([NuEquation(Closure("y", BinderMap({"X":0}, {0:"X"})),
                             Closure("Y", BinderMap({"x":0}, {0:"x"})))],
                [], dict([]))
    
    assert str(res12) == str(testRes12)
    
    res13 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(Abs("X", Var("y")), emptyBinderMap()), Closure(Var("Y"), emptyBinderMap()))))

    testRes13 = ([],
                [DeltaEquation(Closure(Var("$X1"), BinderMap({"$a0":0}, {0:"$a0"})),
                               Closure(Var("y"), BinderMap({"X":0}, {0:"X"})))],
                {"Y":Abs("$a0",Var("$X1"))})
    
    assert str(res13) == str(testRes13)
    
    res14 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(Abs("X", "y"), emptyBinderMap()), Closure(Var("Y"), emptyBinderMap()))))

    testRes14 = ([NuEquation(Closure("y", BinderMap({"X":0}, {0:"X"})),
                             Closure(Var("$X1"), BinderMap({"$a0":0}, {0:"$a0"})))],
                [],
                {"Y":Abs("$a0",Var("$X1"))})
    
    assert str(res14) == str(testRes14)
    
    res15 = runRhoMachine(
            stepRho(
                ([], [], dict([])), 
                MultiEquation(Closure(Abs("X", Var("y")), emptyBinderMap()), Closure(Abs("X", Var("Y")), emptyBinderMap()))))

    testRes15 = ([],
                 [DeltaEquation(Closure(Var("y"), BinderMap({"X":0}, {0:"X"})),
                                Closure(Var("Y"), BinderMap({"X":0}, {0:"X"})))],
                 dict([]))
    
    assert str(res15) == str(testRes15)

    expr161 = App("x", Abs("z", "w"))
    expr162 = App("x", Abs("y", "w"))
    
    res16 = runRhoMachine(stepRho(([], [], dict([])), 
            MultiEquation(Closure(expr161, emptyBinderMap()), Closure(expr162, emptyBinderMap()))))

    resTest16 = ([NuEquation(Closure("w", BinderMap({"z":0}, {0:"z"})),
                           Closure("w", BinderMap({"y":0}, {0:"y"}))),
                  NuEquation(Closure("x", emptyBinderMap()),
                           Closure("x", emptyBinderMap()))],
                [], dict([]))
    
    # [AA(Clo(0, BM({'z': 0}, {0: 'z'})), Clo(0, BM({'y': 0}, {0: 'y'}))),
    #  AA(Clo(x, BM({'z': 0}, {0: 'z'})), Clo(x, BM({'y': 0}, {0: 'y'})))],
    
    assert str(res16) == str(resTest16)

def test_evalRho():
    # To Do

    # expr1 = App(Var("X"), Abs("z", App("d", "z")))
    # expr2 = App("x", Abs("y", Var("Y")))
    
    pass
