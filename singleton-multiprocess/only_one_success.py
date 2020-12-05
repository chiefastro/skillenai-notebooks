import os

class OnlyOne:
    class __OnlyOne:
        def __init__(self, arg):
            if arg is None:
                raise ValueError("Pretend empty instantiation breaks code")
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg=None):
        if not self.instance:
            if arg is None:
                # look up val from env var
                arg = os.getenv('SINGLETON_VAL')
            else:
                # set env var so all workers use the same val
                os.environ['SINGLETON_VAL'] = arg
            self.instance = self.__OnlyOne(arg)
        else:
            self.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)