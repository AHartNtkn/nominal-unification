def test_foldr():
    assert foldr(lambda x, y: x ** y, 2, [3,4]) == 43046721

def test_modify():
    assert modify(lambda x: 2 * x).getResult(3) == ()
    assert modify(lambda x: 2 * x).getState(3) == 6

def test_get():
    assert get().getResult(3) == 3
    assert get().getState(3) == 3

def test_mapMU():
    l = [3,4]
    def f(num):
        return State(lambda s: ((), s ** num))
    assert mapMU(f,l).getState(2) == 4096
    assert mapMU(f,l).getResult(2) == ()

def test_foldM():
    def testf(b, a):
        return State(lambda s: (b ** a, s))
    assert foldM(testf, 2, [3,4]).getState(20) == 20
    assert foldM(testf, 2, [3,4]).getResult(20) == 4096
