# HELLO

import hashlib

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


class FunctionStore:
    def fun_key(self, fun, *args):
        fun_name_key = fun.__name__
        args_key = '/'.join(str(arg.id) for arg in args)
        return '/'.join([fun_name_key, args_key])

class DataSource:
    def __init__(self, data_source_id):
        self.data_source_id = data_source_id

class CacheManager:
    def __init__(self, fun_store, store):
        self.fun_store = fun_store
        self.store     = store

    def cache_function(self, fun, *args, **kwargs):
        key = self.fun_store.fun_key(fun, *args)
        cache_result = self.store.lookup(key)
        if cache_result.is_fresh:
            print "FRESH"
            print cache_result.value
            return cache_result.value
        else:
            computed_value = fun(*args)
            self.store.store(key, computed_value)
            print "STALE"
            print computed_value
            return computed_value

store = Store()
fun_store = FunctionStore()
cache_manager = CacheManager(fun_store, store)

def computed(*deps, **kwargs):
    def _computed(fun):
        def wrapper(*args, **kwargs):
            return cache_manager.cache_function(fun, *args, **kwargs)
        wrapper.computed = True
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

@computed(b, c)
def h(b, c):
    return b.value + c.value

@computed(a, b, c, deps=(h))
def f(a, b, c):
    return a.value * h(b, c)
