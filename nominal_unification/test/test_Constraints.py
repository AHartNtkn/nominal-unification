from nominal_unification.Exceptions import *
from nominal_unification.Syntax import *

def test_sameClo():
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
    
    assert sameClo(cl1s, cl1s) == True
    assert sameClo(cl1s, cl2s) == True
    assert sameClo(cl1s, cl3s) == False
    assert sameClo(cl1s, cl1c) == False
    assert sameClo(cl1s, cl2c) == False
    assert sameClo(cl1s, cl1n) == False
    assert sameClo(cl1s, cl2n) == False
    
    assert sameClo(cl2s, cl2s) == True
    assert sameClo(cl2s, cl3s) == False
    assert sameClo(cl2s, cl1c) == False
    assert sameClo(cl2s, cl2c) == False
    assert sameClo(cl2s, cl1n) == False
    assert sameClo(cl2s, cl2n) == False
    
    assert sameClo(cl3s, cl3s) == True
    assert sameClo(cl3s, cl1c) == True
    assert sameClo(cl3s, cl2c) == False
    assert sameClo(cl3s, cl1n) == False
    assert sameClo(cl3s, cl2n) == False
    
    assert sameClo(cl1c, cl1c) == True
    assert sameClo(cl1c, cl2c) == False
    assert sameClo(cl1c, cl1n) == False
    assert sameClo(cl1c, cl2n) == False
    
    assert sameClo(cl2c, cl2c) == True
    assert sameClo(cl2c, cl1n) == False
    assert sameClo(cl2c, cl2n) == False
                 
    assert sameClo(cl1n, cl1n) == True
    assert sameClo(cl1n, cl2n) == True
                 
    assert sameClo(cl2n, cl2n) == True

def test_extendSubst():
    sub = extendSubst(Var('X'), Atom('3'),
          extendSubst(Var('Y'), Atom('2'),
          extendSubst(Var('X'), Atom('1'), dict([]))))
    
    assert sub == {'X':Atom('3'), 'Y':Atom('2')}

def test_subst():
    sub = extendSubst(Var('X'), Atom('3'), extendSubst(Var('Y'), Atom('2'), dict([])))
    
    expr0 = App(Var('X'), App(Var('Y'), Abs('X', App(Var('X'), Var('Y')))))
    expr1 = Var('X')
    expr2 = Var('Z')
    expr3 = Abs('X', Var('X'))
    expr4 = Abs('X', Var('Z'))
    expr5 = Abs('Y', Var('X'))

    assert subst(expr0, sub) == expr0
    assert subst(expr1, sub) == Atom('3')
    assert subst(expr2, sub) == Var('Z')
    assert subst(expr3, sub) == Abs('X', Atom('3'))
    assert subst(expr4, sub) == Abs('X', Var('Z'))
    assert subst(expr5, sub) == Abs('Y', Atom('3'))
