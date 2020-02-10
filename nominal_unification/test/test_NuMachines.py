from pymonad import *

from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

def test_runNuMachine():
    sub = extendSubst(Var('X'), Atom('3'), extendSubst(Var('Y'), Atom('2'), dict([])))
    nuM = State.unit(12142)
    
    assert runNuMachine(sub, nuM) == sub

def test_bind():
    sub = extendSubst(Var('X'), Atom('3'), extendSubst(Var('Y'), Atom('2'), dict([])))
    
    assert runNuMachine(sub, bind(Var('T'), Atom('Z'))) == {'T':Atom('Z'), 'X':Atom('3'), 'Y':Atom('2')}
    assert runNuMachine(sub, bind(Var('X'), Atom('4'))) == {'X':Atom('4'), 'Y':Atom('2')}

def test_stepNu():
    bm1 = extend(Atom("cool"), extend(Atom("stuff"), emptyBinderMap()))
    bm2 = extend(Atom("neat"), extend(Atom("stuff"), emptyBinderMap()))
    bm3 = extend(Atom("neat"), extend(Atom("stuff"), extend(Atom("too"), emptyBinderMap())))

    cl1s = Closure(Atom("stuff"), bm1)
    cl2s = Closure(Atom("stuff"), bm2)
    cl3s = Closure(Atom("stuff"), bm3)

    cl1c = Closure(Atom("cool"), bm1)
    cl2c = Closure(Atom("cool"), bm2)

    cl1n = Closure(Atom("new"), bm1)
    cl2n = Closure(Atom("new"), bm2)
    
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
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl1v))) == {'stuff':Atom('stuff')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl2v))) == {'stuff':Atom('too')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1s, cl3v))) == {'new':Atom('stuff')}
    
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
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl1v))) == {'stuff':Atom('stuff')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl2v))) == {'stuff':Atom('too')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2s, cl3v))) == {'new':Atom('stuff')}

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
    assert runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl1v))) == {'stuff':Atom('neat')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl2v))) == {'stuff':Atom('stuff')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl3s, cl3v))) == {'new':Atom('neat')}

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
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1c, cl1v))) == {'stuff':Atom('neat')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1c, cl2v))) == {'stuff':Atom('stuff')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1c, cl3v))) == {'new':Atom('neat')}

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
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2c, cl1v))) == {'stuff':Atom('cool')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2c, cl2v))) == {'stuff':Atom('cool')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2c, cl3v))) == {'new':Atom('cool')}

    assert runNuMachine(dict([]), stepNu(NuEquation(cl1n, cl1n))) == dict([])
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1n, cl2n))) == dict([])
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1n, cl1v))) == {'stuff':Atom('new')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1n, cl2v))) == {'stuff':Atom('new')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl1n, cl3v))) == {'new':Atom('new')}

    assert runNuMachine(dict([]), stepNu(NuEquation(cl2n, cl2n))) == dict([])
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2n, cl1v))) == {'stuff':Atom('new')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2n, cl2v))) == {'stuff':Atom('new')}
    assert runNuMachine(dict([]), stepNu(NuEquation(cl2n, cl3v))) == {'new':Atom('new')}

def test_evalNu():
    bm1 = extend(Atom("cool"), extend(Atom("stuff"), emptyBinderMap()))
    bm2 = extend(Atom("neat"), extend(Atom("stuff"), emptyBinderMap()))
    bm3 = extend(Atom("neat"), extend(Atom("stuff"), extend(Atom("too"), emptyBinderMap())))

    cl2s = Closure(Atom("stuff"), bm2)

    cl1n = Closure(Atom("new"), bm1)
    cl2n = Closure(Atom("new"), bm2)
    
    cl1v = Closure(Var("stuff"), bm2)
    cl2v = Closure(Var("stuff"), bm3)
    cl3v = Closure(Var("new"), bm2)
    
    nprob = [NuEquation(cl1n, cl1n),
             NuEquation(cl1n, cl2n),
             NuEquation(cl1n, cl1v),
             NuEquation(cl1n, cl2v),
             NuEquation(cl2s, cl2v),
             NuEquation(cl1n, cl3v)]
    
    assert runNuMachine(dict([]), evalNu(nprob)) == {"new":Atom("new"), "stuff":Atom("too")}
