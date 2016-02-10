from smache import smache

from collections import namedtuple

# Definitions
a = smache.data_source('A')
b = smache.data_source('B')
c = smache.data_source('C')

@smache.computed(a, sources=(b, c))
def score(a):
    return a.value + 5 + 10

@smache.computed(b, c)
def h(b, c):
    return b.value + c.value

@smache.computed(a, b, c)
def f(a, b, c):
    return a.value * h(b, c)

# Tests

Entity = namedtuple('Entity', ['id', 'value'])

def test_cache():
    ax = Entity(1, 10)
    bx = Entity(2, 2)
    cx = Entity(3, 3)

    assert f(ax, bx, cx) == 50
    assert h(bx, cx) == 5
    assert score(ax)

    assert smache.is_fun_fresh(score, ax) == True
    assert smache.is_fun_fresh(f, ax, bx, cx) == True
    assert smache.is_fun_fresh(h, bx, cx) == True

    b.did_update(0)

    assert smache.is_fun_fresh(score, ax) == False
    assert smache.is_fun_fresh(f, ax, bx, cx) == True
    assert smache.is_fun_fresh(h, bx, cx) == True

    a.did_update(1)

    assert smache.is_fun_fresh(score, ax) == False
    assert smache.is_fun_fresh(f, ax, bx, cx) == False
    assert smache.is_fun_fresh(h, bx, cx) == True

    b.did_update(2)

    assert smache.is_fun_fresh(score, ax) == False
    assert smache.is_fun_fresh(f, ax, bx, cx) == False
    assert smache.is_fun_fresh(h, bx, cx) == False
