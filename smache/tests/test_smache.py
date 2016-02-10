from smache import *

from collections import namedtuple

Entity = namedtuple('Entity', ['id', 'value'])

def test_nocache():
    ax = Entity(1, 10)
    bx = Entity(2, 2)
    cx = Entity(3, 3)

    assert f(ax, bx, cx) == 50
    assert h(bx, cx) == 5
    assert score(ax)

    assert store.is_fresh('score/1') == True

    b.did_update(0)

    assert store.is_fresh('score/1') == False

    assert False


def test_source_deps():
    deps = DataSourceDependencies()
    deps.add_dependency('A', '1', 'hello/world')
    deps.add_dependency('A', '1', 'foo/bar')
    deps.add_dependency('A', '2', 'soo/tar')
    deps.add_dependency('B', '1', 'lalala')
    deps.add_data_source_dependency('A', 'full')

    assert deps.values_depending_on('A', '1') == set(['hello/world', 'foo/bar', 'full'])
    assert deps.values_depending_on('A', '2') == set(['soo/tar', 'full'])
    assert deps.values_depending_on('B', '1') == set(['lalala'])
