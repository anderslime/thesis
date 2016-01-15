from mongoengine import signals

import redis
import json
from datadiff import diff
from source_node import SourceNode

rediscon = redis.from_url('redis://localhost:6379')

# def user_modified(sender, document, **kwargs):
#     json_doc = json.loads(document.to_json())
#     redis_id = "Assignment/%s" % json_doc['_id']['$oid']
#     old_doc = rediscon.get(redis_id)
#     if old_doc:
#         old_doc = json.loads(redis_result)
#         non_equal_diffs = filter(lambda x: x[0] == 'insert', diff(old_doc, json_doc).diffs)
#         for _, mydiff in non_equal_diffs:
#             key = mydiff[0][0]
#             new_value = mydiff[0][1]
#             print "Assignment changed %s from '%s' to '%s'" % (key, str(json_doc[key]), new_value)
#     rediscon.set(redis_id, json.dumps(json_doc))

class MongoSourceNode(SourceNode):
    def __init__(self, document_class, **kwargs):
        SourceNode.__init__(self, document_class.__name__)
        self.document_class = document_class
        self.graph          = None
        self.kwargs         = kwargs

    def set_graph(self, graph):
        self.graph = graph
        self._hook_into_mongoengine()

    def _hook_into_mongoengine(self):
        signals.post_save.connect(self._after_save, sender=self.document_class)

    def _after_save(self, sender, document, **kwargs):
        self.set_value(document)
