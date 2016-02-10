from smache import *

from collections import namedtuple

Entity = namedtuple('Entity', ['id', 'value'])

def test_nocache():
    a = Entity(1, 10)
    b = Entity(2, 2)
    c = Entity(3, 3)

    assert f(a, b, c) == 50
    assert h(b, c) == 5

    assert False
