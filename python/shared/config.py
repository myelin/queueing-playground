import os.path

class Config:

    TYPES = {
        'port': 'int',
        'durable': 'bool',
        'ssl': 'bool',
        }
    
    def __init__(self):
        fn = os.path.join(os.path.abspath(os.path.split(__file__)[0]), "..", "..", "config.txt")
        print "Reading configuration from %s" % fn
        for line in open(fn).readlines():
            p = line.find("#")
            if p != -1: line = line[:p]
            line = line.strip()
            if not line: continue
            
            k, v = [_.strip() for _ in line.split("=", 2)]
            typ = Config.TYPES.get(k)
            if typ == 'int':
                v = int(v)
            elif typ == 'bool':
                v = (v.lower() in ('1', 'true', 'yes', 'on'))
            setattr(self, k, v)
