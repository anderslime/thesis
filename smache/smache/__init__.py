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

    def is_fresh(self, key):
        return self._data.get(key, {}).get('is_fresh', None)

    def mark_as_stale(self, key):
        old_value = self._data.get(key, None)
        if old_value is not None:
            old_value['is_fresh'] = False
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

    def did_update(self, entity_id):
        self.subscriber(self, entity_id)


class Node:
    def __init__(self, node_id, parents = []):
        self.node_id = node_id
        self.parents = parents

    def add_parent(self, parent_node):
        self.parents.append(parent_node)

class DataSourceDependencies:
    def __init__(self):
        self._dependencies= {}

    def add_dependency(self, data_source_id, entity_id, dep_key):
        data_source_deps = self._dependencies.get(data_source_id, {})
        entity_deps = data_source_deps.get(entity_id, set())
        entity_deps.add(dep_key)
        data_source_deps[entity_id] = entity_deps
        self._dependencies[data_source_id] = data_source_deps

    def add_data_source_dependency(self, data_source_id, dep_key):
        self.add_dependency(data_source_id, 'all', dep_key)

    def values_depending_on(self, data_source_id, entity_id):
        data_source_deps = self._dependencies[data_source_id]
        return data_source_deps.get('all', set()) | data_source_deps.get(entity_id, set())

    def _entity_key(self, data_source_id, entity_id):
        return '/'.join([data_source_id, str(entity_id)])

class CacheManager:
    def __init__(self, fun_store, store, data_source_deps):
        self.fun_store        = fun_store
        self.store            = store
        self.data_source_deps = data_source_deps
        self._data_sources    = []
        self._computed_funs   = {}

    def cache_function(self, fun, *args, **kwargs):
        key = self.fun_store.fun_key(fun, *args)
        self._add_entity_dependencies(fun, args, key)
        self._add_data_source_dependencies(fun, key)
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
            data_source.subscribe(self._on_data_source_update)

    def add_computed(self, fun, entity_deps, kwargs):
        data_source_deps = kwargs.get('sources', ())
        self._computed_funs[fun.__name__] = (fun.__name__, entity_deps, data_source_deps)

    def _add_data_source_dependencies(self, fun, key):
        data_source_deps = self._computed_funs[fun.__name__][2]
        for data_source_dep in data_source_deps:
            self.data_source_deps.add_data_source_dependency(
                data_source_dep.data_source_id,
                key
            )

    def _add_entity_dependencies(self, fun, args, key):
        entity_deps = self._computed_funs[fun.__name__][1]
        for data_source, data_source_entity in zip(entity_deps, args):
            self.data_source_deps.add_dependency(
                data_source.data_source_id,
                data_source_entity.id,
                key
            )

    def parse_deps(self, value):
        if isinstance(value, tuple):
            return value
        else:
            return (value,)

    def _on_data_source_update(self, data_source, entity_id):
        depending_keys = self.data_source_deps.values_depending_on(data_source.data_source_id, entity_id)
        print depending_keys
        for key in depending_keys:
            self.store.mark_as_stale(key)


data_source_deps = DataSourceDependencies()
store            = Store()
fun_store        = FunctionStore()
cache_manager    = CacheManager(fun_store, store, data_source_deps)

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

@computed(a, sources=(b, c))
def score(a):
    print "UPDATE SCORE"
    return a.value + 5 + 10

@computed(b, c)
def h(b, c):
    return b.value + c.value

@computed(a, b, c)
def f(a, b, c):
    return a.value * h(b, c)
