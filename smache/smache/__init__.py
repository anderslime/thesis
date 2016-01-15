import copy
import graph_drawer
from mongo_source import *
from source_node import SourceNode


class ComputedNode:
    def __init__(self, id, action, graph, *dependencies):
        self.id            = id
        self._value        = None
        self._dependencies = []
        self._parents      = []
        self._action       = action
        self._graph        = graph

        self._set_dependencies(dependencies)
        self.update()

    def update(self):
        values = [node.value for node in self._dependencies]
        self.value = self.evaluate(*values)
        self._update_parents()

    def evaluate(self, *input):
        if self._action:
            return self._action(self._graph, *input)
        raise NotImplementedError(
            "{} does not implement evaluate".format(self.__class__.__name__)
        )

    def _set_dependencies(self, dependencies):
        self._dependencies = dependencies
        for dependency in dependencies:
            dependency.add_parent(self)

    def add_parent(self, new_parent):
        self._parents.append(new_parent)

    def _update_parents(self):
        for parent in self._parents:
            parent.update()

def computed_functions(cls):
    return [(name, thing) for name, thing in cls.__dict__.iteritems()
            if hasattr(thing, 'computed') and getattr(thing, 'computed') == True]

def is_source(obj):
    return type(obj).__name__ == 'instance' and issubclass(obj.__class__, SourceNode)

def find_sources(cls):
    return [thing for name, thing in cls.__dict__.iteritems() if is_source(thing)]

def dependency(graph, computed_nodes, dependency):
    if is_source(dependency):
        return next(source for source in graph.sources if dependency.id == source.id)
    else:
        return next(node for node in computed_nodes if dependency.__name__ == node.id)

def computed(*deps):
    def _computed(f):
        def wrapper(self, *args):
            return f(self, *args)
        wrapper.computed = True
        wrapper.dependencies = deps
        wrapper.__name__ = f.__name__
        return wrapper
    return _computed

class GraphRepository:
    def __init__(self):
        self.repository = {}

    def add_graph(self, graph):
        self.repository[graph.lookup_key()] = graph

repo = GraphRepository()

class DependenceGraph:
    def __init__(self):
        sources = find_sources(self.__class__)
        computed_funs = computed_functions(self.__class__)
        computed_nodes = []
        self.sources = [copy.deepcopy(source) for source in sources]
        for source in self.sources:
            source.set_graph(self)
        for name, computed_fun in computed_funs:
            dependencies = [dependency(self, computed_nodes, obj) for obj in computed_fun.dependencies]
            computed_nodes.append(ComputedNode(name, computed_fun, self, *dependencies))
        self.nodes = tuple(self.sources) + tuple(computed_nodes)

    def set_value(self, source_id, value):
        self.source(source_id).set_value(value)

    def get_value(self, source_id):
        source = next(source for source in self.nodes if source.id == source_id)
        return source.value

    def source(self, source_id):
        return next(source for source in self.sources if source.id == source_id)

    def draw(self, filename):
        graph_drawer.draw(self, filename)

if __name__ == '__main__':
    g = DependenceGraphExample()
    g.draw('hello')
