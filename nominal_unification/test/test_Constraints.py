import unittest

from nominal_unification.Syntax import *
from nominal_unification.Constraints import *

class TestConstraints(unittest.TestCase):
    def test_alphaEq(self):
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
        
        assert alphaEq(cl1s, cl1s) == True
        assert alphaEq(cl1s, cl2s) == True
        assert alphaEq(cl1s, cl3s) == False
        assert alphaEq(cl1s, cl1c) == False
        assert alphaEq(cl1s, cl2c) == False
        assert alphaEq(cl1s, cl1n) == False
        assert alphaEq(cl1s, cl2n) == False
        
        assert alphaEq(cl2s, cl2s) == True
        assert alphaEq(cl2s, cl3s) == False
        assert alphaEq(cl2s, cl1c) == False
        assert alphaEq(cl2s, cl2c) == False
        assert alphaEq(cl2s, cl1n) == False
        assert alphaEq(cl2s, cl2n) == False
        
        assert alphaEq(cl3s, cl3s) == True
        assert alphaEq(cl3s, cl1c) == True
        assert alphaEq(cl3s, cl2c) == False
        assert alphaEq(cl3s, cl1n) == False
        assert alphaEq(cl3s, cl2n) == False
        
        assert alphaEq(cl1c, cl1c) == True
        assert alphaEq(cl1c, cl2c) == False
        assert alphaEq(cl1c, cl1n) == False
        assert alphaEq(cl1c, cl2n) == False
        
        assert alphaEq(cl2c, cl2c) == True
        assert alphaEq(cl2c, cl1n) == False
        assert alphaEq(cl2c, cl2n) == False
                     
        assert alphaEq(cl1n, cl1n) == True
        assert alphaEq(cl1n, cl2n) == True
                     
        assert alphaEq(cl2n, cl2n) == True

    def test_extendSubst(self):
        sub = extendSubst(Var('X'), '3',
              extendSubst(Var('Y'), '2',
              extendSubst(Var('X'), '1', dict([]))))
        
        assert sub == {'X':'3', 'Y':'2'}
