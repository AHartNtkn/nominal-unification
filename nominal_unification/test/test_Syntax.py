from nominal_unification.Exceptions import *

def test_expElim():
    def atomFun(e):
        return str(e)
    testAtom = 2
    
    def varFun(e):
        return e+2
    testVar = Var(2)

    def appFun(e1, e2):
        return e1 - e2
    testApp = App(2, 3)

    def absFun(e1, e2):
        return len(e1 + e2)
    testAbs = Abs("cool ", "stuff")

    assert expElim(testAtom, atomFun, varFun, appFun, absFun) == "2"
    assert expElim(testVar, atomFun, varFun, appFun, absFun) == 4
    assert expElim(testApp, atomFun, varFun, appFun, absFun) == -1
    assert expElim(testAbs, atomFun, varFun, appFun, absFun) == 10

def test_extend():
    bm = extend('cool', extend('stuff', emptyBinderMap()))
    
    assert bm.a2i["cool"] == 1
    assert bm.a2i["stuff"] == 0

    assert bm.i2a[0] == "stuff"
    assert bm.i2a[1] == "cool"

def test_lookupAtom():
    bm = extend('cool', extend('stuff', emptyBinderMap()))

    assert lookupAtom("cool", bm) == Bound("cool", 1)
    assert lookupAtom("stuff", bm) == Bound("stuff", 0)
    assert lookupAtom("new", bm) == Free("new")

def test_lookupIdx():
    bm = extend('cool', extend('stuff', emptyBinderMap()))

    assert lookupIdx(0, bm) == "stuff"
    assert lookupIdx(1, bm) == "cool"

    try:
        lookupIdx(2, bm)
        assert False
    except NoMatchingBinderError:
        assert True
