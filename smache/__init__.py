# HELLO

import hashlib

class Store:
    def __init__(self):
        self._data = {}

    def store(self, key, value):
        self._data[key] = value

    def lookup(self, key):
        return self._data.get(key, None)


class FunctionStore:
    def __init__(self, store):
        self.store = store

    def upsert(self, fun, *args, **kwargs):
        fun_key = self._fun_key(fun, *args)
        result = store.lookup(fun_key)
        if result is not None:
            print "CACHE HIT"
            return result
        else:
            print "CACHE MISS"
            computed_value = fun(*args)
            store.store(fun_key, computed_value)
            return computed_value

    def _fun_key(self, fun, *args):
        fun_name_key = fun.__name__
        args_key = '/'.join(str(arg) for arg in args)
        return '/'.join([fun_name_key, args_key])


store = Store()
fun_store = FunctionStore(store)

def computed(*deps, **kwargs):
    def _computed(fun):
        def wrapper(*args, **kwargs):
            return fun_store.upsert(fun, *args, **kwargs)
        wrapper.computed = True
        return wrapper
    return _computed

# a ----------\
#              f
# b ----\     /
#        h --/
# c ----/

@computed()
def h(b, c):
    print "CALLING H"
    return b + c

@computed(deps=(h))
def f(a, b, c):
    print "CALLING F"
    return a * h(b, c)



