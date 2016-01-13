import dagger
from subprocess import call

def draw(graph, filename):
    dag = dagger.dagger()
    _recursive_add(dag, graph.sources)
    dag.run()
    dotfile = "{}.dot".format(filename)
    dag.dot(dotfile)

def _recursive_add(dag, nodes):
    for node in nodes:
        parent_values = [parent.id for parent in node._parents]
        dag.add(node.id, parent_values)
        _recursive_add(dag, node._parents)
