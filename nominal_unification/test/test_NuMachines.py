from pymonad import *

from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

def test_bind():
    sub = extendSubst(Var('X'), '3', extendSubst(Var('Y'), '2', dict([])))
    
    nm = NuMachine(sub)
    nm.bind(Var('T'), 'Z')
    assert nm.subst == {'T':'Z', 'X':'3', 'Y':'2'}
    
    nm = NuMachine(sub)
    nm.bind(Var('X'), '4')
    assert nm.subst == {'X':'4', 'Y':'2'}

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
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl1s, cl1c))
        assert False
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl1s, cl2c))
        assert False
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl1s, cl1n))
        assert False
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl1s, cl2n))
        assert False
    except AAMismatchError:
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
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl2s, cl1c))
        assert False
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl2s, cl2c))
        assert False
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl2s, cl1n))
        assert False
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl2s, cl2n))
        assert False
    except AAMismatchError:
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
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl3s, cl1n))
        assert False
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl3s, cl2n))
        assert False
    except AAMismatchError:
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
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl1c, cl1n))
        assert False
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl1c, cl2n))
        assert False
    except AAMismatchError:
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
    except AAMismatchError:
        assert True
    try:
        nm = NuMachine()
        nm.step(NuEquation(cl2c, cl2n))
        assert False
    except AAMismatchError:
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
    
    nm = NuMachine()
    nm.eval(nprob)
    
    assert nm.subst == {"new":"new", "stuff":"too"}
