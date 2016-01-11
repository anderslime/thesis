# def observe(*deps):
#     def wrap(f):
#         def wrapped_f(self, *args):
#             Observer.did_change(getattr(self, deps[0]))
#             f(self, *args)
#         return wrapped_f
#     return wrap
#
#
# class Hello:
#     def __init__(self, lol):
#         self.lol = lol
#
#     @obs.observe("lol")
#     def save(self):
#         pass
#
# h = Hello("hihi")
# h.hello()



