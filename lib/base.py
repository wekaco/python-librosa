import logging
logging.getLogger().setLevel(logging.DEBUG)

def autostart(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next(cr)
        return cr
    return start


def generator(name: str, size:int=1):
    def _generator(func):
        logger = logging.getLogger(name)
        @autostart
        def _wrapper(*args, targets=[], **kwargs):
            logger.debug('start')
            try:
                while True:
                    if size == 1:
                        _in = (yield)
                    else:
                        _in = []
                        for i in range(size):
                            _in.append((yield))

                    _out = func(_in, *args, **kwargs)
                    for t in targets:
                        t.send(_out)
            except GeneratorExit:
                logger.debug('exit')
                for t in targets:
                    t.close()

        return _wrapper
    return _generator
