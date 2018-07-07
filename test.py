from contextlib import contextmanager

class MyResource:
    # def __enter__(self):
    #     print('connect to resource')
    #     return self
    # def __exit__(self,exc_type,exc_value,tb):
    #     print('close resource connection')
    def query(self):
        print('query data')
# with MyResource() as r:
#     r.query()


@contextmanager
def make_myresource():
    print('connect to resource')
    yield MyResource()
    print('close resource connection')
with make_myresource() as r:
    r.query()