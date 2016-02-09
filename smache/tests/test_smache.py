from smache import *

def test_nocache():
    a = 10
    b = 2
    c = 3
    assert f(a, b, c) == 50
    assert h(b, c) == 5

    assert False
