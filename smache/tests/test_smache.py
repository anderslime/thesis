from smache import cm

from collections import namedtuple

# Definitions

a = cm.data_source('A')
b = cm.data_source('B')
c = cm.data_source('C')

@cm.computed(a, sources=(b, c))
def score(a):
    return a.value + 5 + 10

@cm.computed(b, c)
def h(b, c):
    return b.value + c.value

@cm.computed(a, b, c)
def f(a, b, c):
    return a.value * h(b, c)

# Tests

Entity = namedtuple('Entity', ['id', 'value'])

def test_nocache():
    ax = Entity(1, 10)
    bx = Entity(2, 2)
    cx = Entity(3, 3)

    assert f(ax, bx, cx) == 50
    assert h(bx, cx) == 5
    assert score(ax)

    assert cm.is_fresh('score/1') == True

    b.did_update(0)

    assert cm.is_fresh('score/1') == False
