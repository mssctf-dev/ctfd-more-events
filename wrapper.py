import logging


def wrap(func, lm):
    def new_func(*args, **kwargs):
        ret = func(*args, **kwargs)
        try:
            lm(ret)
        except Exception as e:
            logging.exception(e)
            pass
        return ret
    return new_func
