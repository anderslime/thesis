import copy

DEBUG = False

def debug(message):
    if DEBUG == True:
        print message

class SourceNode:
    def __init__(self, id, value = None):
        self.id       = id
        self._parents = []
        self.value    = value

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        debug("Updating source value {}".format(new_value))
        self.value = new_value
        for parent in self._parents:
            debug("Cascaded updating parent {}".format(parent.id))
            parent.update()

    def set_parent(self, new_parent):
        self._parents.append(new_parent)

class ComputedNode:
    def __init__(self, id, action, *dependencies):
        self.id            = id
        self._value        = None
        self._dependencies = []
        self._parents      = []
        self._action       = action

        self._set_dependencies(dependencies)
        self.update()

    def update(self):
        debug("Updating myself %s" % self.id)
        values = [node.value for node in self._dependencies]
        self.value = self.evaluate(*values)
        for parent in self._parents:
            debug("Cascaded updating parent {}".format(parent.id))
            parent.update()

    def evaluate(self, *input):
        if self._action:
            return self._action(*input)
        raise NotImplementedError(
            "{} does not implement evaluate".format(self.__class__.__name__)
        )

    def _set_dependencies(self, dependencies):
        self._dependencies = dependencies
        for dependency in dependencies:
            dependency.set_parent(self)

    def set_parent(self, new_parent):
        self._parents.append(new_parent)

def computed_functions(cls):
    return [(name, thing) for name, thing in cls.__dict__.iteritems()
            if hasattr(thing, 'computed') and getattr(thing, 'computed') == True]

def is_source(obj):
    return type(obj).__name__ == 'instance' and obj.__class__.__name__ == 'SourceNode'

def find_sources(cls):
    return [thing for name, thing in cls.__dict__.iteritems() if is_source(thing)]

def dependency(computed_nodes, dependency):
    if is_source(dependency):
        return dependency
    else:
        return next(node for node in computed_nodes if dependency.__name__ == node.id)


# def cached_graph(init):
#     def new_init(self, *args):
#         sources = find_sources(self.__class__)
#         computed_funs = computed_functions(self.__class__)
#         computed_nodes = []
#         self.sources = [copy.deepcopy(source) for source in sources]
#         for name, computed_fun in computed_funs:
#             dependencies = [dependency(computed_nodes, obj) for obj in computed_fun.dependencies]
#             computed_nodes.append(ComputedNode(name, computed_fun, *dependencies))
#         init(self, *args)
#     return new_init

def computed(*deps):
    def _computed(f):
        f.computed = True
        f.dependencies = deps
        return f
    return _computed

class Graph:
    def __init__(self):
        sources = find_sources(self.__class__)
        computed_funs = computed_functions(self.__class__)
        computed_nodes = []
        self.sources = [copy.deepcopy(source) for source in sources]
        for name, computed_fun in computed_funs:
            dependencies = [dependency(computed_nodes, obj) for obj in computed_fun.dependencies]
            computed_nodes.append(ComputedNode(name, computed_fun, *dependencies))

    def set_value(self, source_id, value):
        source = next(source for source in self.sources if source.id == source_id)
        source.set_value(value)

    def get_value(self, source_id):
        source = next(source for source in self.sources if source.id == source_id)
        return source.value


class Hello(Graph):
    number = SourceNode("Number")

    @computed(number)
    def computed_function(x):
        if x is None:
            return None
        return x + 1

    @computed(computed_function)
    def another_computed_function(y):
        if y is None:
            return None
        return y + 1

if __name__ == '__main__':
    g = Hello()

    g.set_value("Number", 5)
    print Hello.number.value
    print g.get_value("Number")
