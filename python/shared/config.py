import os.path

class Config:
    def __init__(self):
        fn = os.path.join(os.path.abspath(os.path.split(__file__)[0]), "..", "..", "config.txt")
        print "Reading configuration from %s" % fn
        for line in open(fn).readlines():
            p = line.find("#")
            if p != -1: line = line[:p]
            k, v = line.split("=", 2)
            setattr(self, k.strip(), v.strip())

    def get_bool(self, k):
        return getattr(self, k).lower() in ('1', 'true', 'yes', 'on')
