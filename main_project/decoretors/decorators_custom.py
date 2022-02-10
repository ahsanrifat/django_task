import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        time_taken = te - ts
        print(
            f"Method: {method.__name__}, Args: {args}, Kwargs: {kw}, Time Taken: {time_taken} sec"
        )
        return result

    return timed
