import redis

class Smache:
    def __init__(self):
        self.rediscon = redis.from_url('redis://localhost:6379')
        self.underlying_data_nodes = {}

    def add_underlying_data(self, ud_node):
        self.underlying_data_nodes[ud_node.id] = ud_node

    def add_dependency(self, ud_node_id, cache_object):
        try:
            ud = self.underlying_data_nodes[ud_node_id]
            ud.add_parent(cache_object)
            cache_object.add_dependency(ud)
        except KeyError:
            print "Underlying data %s does not exist" % ud_node_id

    def underlying_data_changed(self, ud_node_id):
        self.underlying_data_nodes[ud_node_id].update()

class SmacheNode:
    def __init__(self, id, update_func):
        self.id = id
        self.update_func = update_func
        self.parent_nodes = []
        self.dependency_nodes = []

    def depends_on(self, other_nodes):
        for other_node in other_nodes:
            self.add_dependency(other_node)
            other_node.add_parent(self)
        return self

    def add_parent(self, parent_node):
        self.parent_nodes.append(parent_node)

    def add_dependency(self, dependency_node):
        self.dependency_nodes.append(dependency_node)

    def update(self):
        print "Updating myself %s" % self.id
        for parent in self.parent_nodes:
            print "Updating parent %s" % parent.id
            parent.update()

def ass_json_func(**deps):
    return ' - '.join(deps["Assignment"], deps["Course"])

if __name__ == '__main__':
    smache = Smache()
    assignment = SmacheNode("Assignment", lambda x: x)
    course = SmacheNode("Course", lambda x: x)

    smache.add_underlying_data(assignment)
    smache.add_underlying_data(course)

    ass_json = SmacheNode("AssJSON", ass_json_func)
    ass_json.depends_on([assignment, course])
    ass_json_list = SmacheNode(
        "AssJSONList",
        lambda **deps: [deps["AssJSON"]]
    ).depends_on([ass_json])
    SmacheNode("AssXML", lambda x: "<xml>{0}</xml>".format(x)).depends_on([assignment])

    smache.underlying_data_changed("Course")
