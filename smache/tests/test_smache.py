from smache import *

from collections import namedtuple

Entity = namedtuple('Entity', ['id', 'value'])

def test_nocache():
    ax = Entity(1, 10)
    bx = Entity(2, 2)
    cx = Entity(3, 3)

    assert f(ax, bx, cx) == 50
    assert h(bx, cx) == 5

    a.did_update(1)

    assert store.is_fresh('f/1/2/3') == False
    assert store.is_fresh('h/2/3') == True



# def test_source_deps():
#     deps = DataSourceDependencies()
#     deps.add_dependency('A', '1', 'hello/world')
#     deps.add_dependency('A', '1', 'foo/bar')
#     deps.add_dependency('A', '2', 'soo/tar')
#     deps.add_dependency('B', '1', 'lalala')
#
#     assert deps.values_depending_on('A', '1') == set(['hello/world', 'foo/bar'])
#     assert deps.values_depending_on('A', '2') == set(['soo/tar'])
#     assert deps.values_depending_on('B', '1') == set(['lalala'])
