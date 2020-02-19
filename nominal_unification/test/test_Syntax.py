import unittest

from nominal_unification.Syntax import *

class TestSyntax(unittest.TestCase):
    def test_extend(self):
        sc = extend('cool', extend('stuff', emptyScope()))
        
        assert sc.n2i["cool"] == 1
        assert sc.n2i["stuff"] == 0

        assert sc.i2n[0] == "stuff"
        assert sc.i2n[1] == "cool"

    def test_lookupName(self):
        sc = extend('cool', extend('stuff', emptyScope()))

        assert lookupName("cool", sc) == Bound("cool", 1)
        assert lookupName("stuff", sc) == Bound("stuff", 0)
        assert lookupName("new", sc) == Free("new")

    def test_lookupIdx(self):
        sc = extend('cool', extend('stuff', emptyScope()))

        assert lookupIdx(0, sc) == "stuff"
        assert lookupIdx(1, sc) == "cool"

        try:
            lookupIdx(2, sc)
            assert False
        except Exception:
            assert True
