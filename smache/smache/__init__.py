# HELLO

import hashlib
from topological_sort import topological_sort

class CacheResult:
    def __init__(self, value, is_fresh):
        self.value    = value
        self.is_fresh = is_fresh


class Store:
    def __init__(self):
        self._data = {}

    def store(self, key, value):
        self._data[key] = {'is_fresh': True, 'value': value}

    def lookup(self, key):
        raw_cache_result = self._data.get(key, {})
        return CacheResult(
            raw_cache_result.get('value', None),
            raw_cache_result.get('is_fresh', False)
        )

    def mark_as_dirty(self, key):
        old_value = self._data.get(key, None)
        if old_value is not None:
            old_value['is_fresh'] = True
            self._data[key] = old_value


class FunctionStore:
    def fun_key(self, fun, *args):
        fun_name_key = fun.__name__
        args_key = '/'.join(str(arg.id) for arg in args)
        return '/'.join([fun_name_key, args_key])

class DataSource:
    def __init__(self, data_source_id):
        self.data_source_id = data_source_id
        self.subscriber = lambda x: x

    def subscribe(self, fun):
        self.subscriber = fun

    def did_update(self):
        self.subscriber(self)


class Node:
    def __init__(self, node_id, parents = []):
        self.node_id = node_id
        self.parents = parents

    def add_parent(self, parent_node):
        self.parents.append(parent_node)

class DependencyGraph:
    def __init__(self):
        self._nodes = {}

    def add_node(self, node_id, dependency_node_ids):
        node = Node(node_id, [])
        self._set_node(node_id, node)
        for dependency_node_id in dependency_node_ids:
            self._get_node(dependency_node_id).add_parent(node)

    def parents(self, node_id):
        return self._get_node(node_id).parents

    def _get_node(self, node_id):
        return self._nodes[node_id]

    def _set_node(self, node_id, node):
        self._nodes[node_id] = node


class CacheManager:
    def __init__(self, fun_store, store, dep_graph):
        self.fun_store      = fun_store
        self.store          = store
        self.dep_graph       = dep_graph
        self._data_sources  = []
        # self._computed_funs = []

    def cache_function(self, fun, *args, **kwargs):
        key = self.fun_store.fun_key(fun, *args)
        cache_result = self.store.lookup(key)
        if cache_result.is_fresh:
            return cache_result.value
        else:
            computed_value = fun(*args)
            self.store.store(key, computed_value)
            return computed_value

    def add_sources(self, *data_sources):
        for data_source in data_sources:
            self._data_sources.append(data_source)
            self.dep_graph.add_node(data_source.data_source_id, [])
            data_source.subscribe(self._on_data_source_update)

    def add_computed(self, fun, data_source_deps, kwargs):
        computed_deps = self.parse_deps(kwargs.get('deps', ()))
        computed_dep_ids = [f.__name__ for f in computed_deps]
        data_source_dep_ids = [node.data_source_id for node in data_source_deps]
        dependency_ids = computed_dep_ids + data_source_dep_ids
        self.dep_graph.add_node(fun.__name__, dependency_ids)

    def parse_deps(self, value):
        if isinstance(value, tuple):
            return value
        else:
            return (value,)

    def _on_data_source_update(self, data_source):
        pass
        # TODO:
        #   1. Get get key for all parents of the data source instance
        #   2. Mark the parent instances as dirty


dep_graph = DependencyGraph()
store = Store()
fun_store = FunctionStore()
cache_manager = CacheManager(fun_store, store, dep_graph)

def computed(*deps, **kwargs):
    def _computed(fun):
        def wrapper(*args, **kwargs):
            return cache_manager.cache_function(fun, *args, **kwargs)
        cache_manager.add_computed(fun, deps, kwargs)
        wrapper.__name__ = fun.__name__
        return wrapper
    return _computed

# a ----------\
#              f
# b ----\     /
#        h --/
# c ----/

a = DataSource('A')
b = DataSource('B')
c = DataSource('C')

cache_manager.add_sources(a, b, c)

@computed(b, c)
def h(b, c):
    return b.value + c.value

@computed(a, b, c, deps=(h))
def f(a, b, c):
    return a.value * h(b, c)
