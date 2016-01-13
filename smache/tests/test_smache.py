import sys
sys.path.append('../smache')

from smache import DependenceGraph, SourceNode, computed

class DependenceGraphExample(DependenceGraph):
    number = SourceNode("Number")

    @computed(number)
    def f1(self, x):
        if x is None:
            return None
        return x + 1

    @computed(number)
    def f2(self, y):
        if y is None:
            return None
        return y + 1

    @computed(f1, f2)
    def total(self, x, y):
        if x is None or y is None:
            return None
        return y + x

def test_it_works():
    g = DependenceGraphExample()

    assert g.get_value("Number") == None

    g.set_value("Number", 5)

    assert g.get_value("total") == 12
