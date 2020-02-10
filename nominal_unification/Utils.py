from pymonad import *

# partition : (a -> Bool) -> [a] -> ([a], [a])
def partition(f, x):
    return (filter(f, x), filter(lambda z: not f(z), x))

# foldr : (a -> b -> b) -> b -> [a] -> b
def foldr(f, e, l):
    if len(l) == 0:
        return e
    return f(l[0], foldr(f, e, l[1:]))

# modify : (s -> s) -> State s ()
def modify(f):
    return State(lambda x: ((), f(x)))

# get : State s s
def get():
    return State(lambda x: (x, x))

# mapMU : (Foldable t, Monad m) => (a -> m b) -> t a -> m ()
def mapMU(f, l):
    return foldr(lambda x, y: f(x).bind(lambda _: y), State.unit(()), l)

# foldM : (Foldable t, Monad m) => (b -> a -> m b) -> b -> t a -> m b
def foldM(f, z0, xs):
    def fp(x, k):
        return lambda z: f(z, x).bind(k)
    
    return foldr(fp, State.unit, xs)(z0)
