

class FunctionCache(object):

    _cache = {}

    @staticmethod
    def run(func, parameters):
        key = '{}{}'.format(func, parameters)
        if key in FunctionCache._cache.keys():
            return FunctionCache._cache[key]
        else:
            value = func(*parameters)
            FunctionCache._cache[key] = value
            return value


if __name__ == '__main__':
    def add(num1, num2):
        print 'run add function'
        return num1 + num2
    def foo():
        print 'run foo'
        return 'foo'
    print FunctionCache.run(add, (5, 1))
    print FunctionCache.run(add, (5, 1))
    print FunctionCache.run(foo, ())
    print FunctionCache.run(foo, ())

