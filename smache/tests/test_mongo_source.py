import sys
sys.path.append('../smache')

from smache import DependenceGraph, SourceNode, computed

from mongoengine import Document, connect, signals, StringField

db = connect('testdb', host='localhost', port=27017,)

class User(Document):
    student_id = StringField()
    name = StringField()

import redis
import json
from datadiff import diff

rediscon = redis.from_url('redis://localhost:6379')

def user_modified(sender, document, **kwargs):
    json_doc = json.loads(document.to_json())
    redis_id = "Assignment/%s" % json_doc['_id']['$oid']
    old_doc = rediscon.get(redis_id)
    if old_doc:
        old_doc = json.loads(redis_result)
        non_equal_diffs = filter(lambda x: x[0] == 'insert', diff(old_doc, json_doc).diffs)
        for _, mydiff in non_equal_diffs:
            key = mydiff[0][0]
            new_value = mydiff[0][1]
            print "Assignment changed %s from '%s' to '%s'" % (key, str(json_doc[key]), new_value)
    rediscon.set(redis_id, json.dumps(json_doc))


class MongoSourceNode(SourceNode):
    def __init__(self, document_class, id_attribute):
        SourceNode.__init__(self, document_class.__name__)
        self.document_class = document_class
        self.id_attribute   = id_attribute
        self._hook_into_mongoengine(document_class)

    def _hook_into_mongoengine(self, document_class):
        signals.post_save.connect(self._after_save, sender=document_class)

    def _after_save(self, sender, document, **kwargs):
        print "AFTER SAVE"
        print kwargs
        print document[self.id_attribute]
        # if 'created' in kwargs:
            # smache.repo.add_graph(

class DependenceGraphExample(DependenceGraph):
    def _sources(self):
        return {
            'user': MongoSourceNode(User, 'id')
        }

    def lookup_key(self):
        return '/'.join([self.__class__.__name__, self.user.id])

    @computed(user)
    def name(self, user):
        if user is None:
            return None
        return user.name

def test_it_works():
    dg = DependenceGraphExample()

    user = User(name='Hello')
    user.save()

    assert dg.lookup(user.id).get_value("name") == "Hello"

    user.name = 'Hello2'
    user.save()

    assert dg.lookup(user.id).get_value("name") == "Hello2"

    assert False
