def wrap(func, lm):
    def new_func(*args, **kwargs):
        ret = func(*args, **kwargs)
        lm(ret)
        try:
            pass
        except Exception as e:
            print(e)
            pass
        return ret
    return new_func