from hacksync.threaded_function import ThreadedFunction


def hacksync():
    def decorator(func):
        def runner(*args, **kwargs):
                wrapped_func = ThreadedFunction(func)
                wrapped_func.start()
                return wrapped_func(*args, **kwargs)
        return runner
    return decorator
