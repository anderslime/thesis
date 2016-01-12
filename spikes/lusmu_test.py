from lusmu.core import Input, Node, update_inputs
from lusmu.visualization import visualize_graph

class Fragment(Node):
    def __init__(self, **kwargs):
        super(Fragment, self).__init__(
            # name=self.__class__.__name__,
            # name='hello',
            # action=self.build_and_save_fragment,
            action=self.build_fragment,
            **kwargs
        )

    def build_and_save_fragment(self, **input):
        result = self.build_fragment(**input)
        # Persist result
        return result

    def build_fragment(self, **input):
        raise NotImplementedError(
            "You need to implement build_fragment for your fragment"
        )

class Difference(Fragment):
    def build_fragment(self, x, y):
        print "diff between {} and {}".format(x, y)
        return x - y

class Addition(Fragment):
    def build_fragment(self, x, y):
        return x + y

class Power(Fragment):
    def build_fragment(self, x, p):
        return x ** p

x = Input(name='x-value')
y = Input(name='y-value')
p = Input(name='power')

difference = Difference(inputs = Node.inputs(x, y))
difference2 = Difference(inputs = Node.inputs(p, p))
addition   = Addition(inputs   = Node.inputs(difference, difference2))
power      = Power(inputs      = Node.inputs(difference, p))

update_inputs([(p, 10), (x, 5), (y, 10)])

# print power.value
print addition.value

print "changing y"
update_inputs([(y, 5)])
print addition.value
