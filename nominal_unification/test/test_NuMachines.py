from pymonad import *

from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

def test_runNuMachine():
    sub = extendSubst(Var('X'), '3', extendSubst(Var('Y'), '2', dict([])))
    nuM = State.unit(12142)
    
    assert runNuMachine(sub, nuM) == sub

def test_bind():
    sub = extendSubst(Var('X'), '3', extendSubst(Var('Y'), '2', dict([])))
    
    assert runNuMachine(sub, bind(Var('T'), 'Z')) == {'T':'Z', 'X':'3', 'Y':'2'}
    assert runNuMachine(sub, bind(Var('X'), '4')) == {'X':'4', 'Y':'2'}

def test_stepNu():
    bm1 = extend("cool", extend("stuff", emptyBinderMap()))
    bm2 = extend("neat", extend("stuff", emptyBinderMap()))
    bm3 = extend("neat", extend("stuff", extend("too", emptyBinderMap())))

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
    
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl1s))) == dict([])
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl2s))) == dict([])
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl3s)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl1c)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl2c)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl1n)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl2n)))
        assert False
    except AAMismatchError:
        assert True
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl1v))) == {'stuff':'stuff'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl2v))) == {'stuff':'too'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl3v))) == {'new':'stuff'}
    
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl2s))) == dict([])
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl3s)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl1c)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl2c)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl1n)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl2n)))
        assert False
    except AAMismatchError:
        assert True
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl1v))) == {'stuff':'stuff'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl2v))) == {'stuff':'too'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl3v))) == {'new':'stuff'}

    assert runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl3s))) == dict([])
    assert runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl1c))) == dict([])
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl2c)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl1n)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl2n)))
        assert False
    except AAMismatchError:
        assert True
    assert runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl1v))) == {'stuff':'neat'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl2v))) == {'stuff':'stuff'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl3v))) == {'new':'neat'}

    assert runNuMachine(dict([]), stepNu(NuEquation(cl1c, cl1c))) == dict([])
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl1c, cl2c)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl1c, cl1n)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl1c, cl2n)))
        assert False
    except AAMismatchError:
        assert True
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1c, cl1v))) == {'stuff':'neat'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1c, cl2v))) == {'stuff':'stuff'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1c, cl3v))) == {'new':'neat'}

    assert runNuMachine(dict([]), stepNu(NuEquation(cl2c, cl2c))) == dict([])
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl2c, cl1n)))
        assert False
    except AAMismatchError:
        assert True
    try:
        runNuMachine(dict([]), stepNu(NuEquation(cl2c, cl2n)))
        assert False
    except AAMismatchError:
        assert True
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2c, cl1v))) == {'stuff':'cool'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2c, cl2v))) == {'stuff':'cool'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2c, cl3v))) == {'new':'cool'}

    assert runNuMachine(dict([]), stepNu(NuEquation(cl1n, cl1n))) == dict([])
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1n, cl2n))) == dict([])
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1n, cl1v))) == {'stuff':'new'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1n, cl2v))) == {'stuff':'new'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1n, cl3v))) == {'new':'new'}

    assert runNuMachine(dict([]), stepNu(NuEquation(cl2n, cl2n))) == dict([])
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2n, cl1v))) == {'stuff':'new'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2n, cl2v))) == {'stuff':'new'}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2n, cl3v))) == {'new':'new'}

def test_evalNu():
    bm1 = extend("cool", extend("stuff", emptyBinderMap()))
    bm2 = extend("neat", extend("stuff", emptyBinderMap()))
    bm3 = extend("neat", extend("stuff", extend("too", emptyBinderMap())))

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
    
    assert runNuMachine(dict([]), evalNu(nprob)) == {"new":"new", "stuff":"too"}
