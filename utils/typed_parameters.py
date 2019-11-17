from functools import wraps

class OptionalDefaultParameter(object):
    def __init__(self, *types):
        assert types

        # Ensure all types are of type 'type'
        for idx, t in enumerate(types):
            assert isinstance(t, type), \
                "Argument {} is not of type 'type', but is of type '{}'".format(
                    idx, type(t))
        self.types = tuple(types)
        
    def __str__(self):
        if len(self.types) == 1:
            return self.types[0].__name__
        return 'something else'
        # return '{}, or {}'.format(
            # ', '.join(t.__name__ for t in self.types[:-1])
            # self.types[-1].__name__)

class OptionalParameter(OptionalDefaultParameter):
    def __init__(self, *types):
        assert isinstance(types, (list, tuple)) and len(types) > 1
        super().__init__(*types)

    # def __str__(self):
        # return '{}, or {}'.format(
            # ', '.join(t.__name__ for t in self.types[:-1])
            # self.types[-1].__name__)

class DefaultParameter(OptionalDefaultParameter):
    pass

def typed_parameters(*types):
    '''
    Type checks method parameters

    types: a tuple of types expected as the method parameters
    '''
    def makewrapper(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Typed_parameters decorator only does not support kwargs
            assert not kwargs, 'typed_parameters decorator does not support keyword arguments'

            # Verify the correct number of args were supplied.  If a parameter is a default parameter,
            # ignore it from our count
            expected_type_count = len(types) - len([o for o in types if isinstance(o, DefaultParameter)])

            if expected_type_count > len(args):
                raise ValueError('Incorrect number of expected arguments.  ' \
                    'Received {1} argument(s) but expected {0} arguments.'.format(expected_type_count, len(args))
                )

            for idx, arg in enumerate(zip(args, types)):
                argument, expected_type = arg

                expected_types = expected_type.types \
                    if isinstance(expected_type, OptionalDefaultParameter) \
                    else (expected_type,)

                if not isinstance(argument, expected_types):

                    expected_type_name = expected_type.__name__ if not \
                        isinstance(expected_type, OptionalDefaultParameter) \
                        else str(expected_type)
               
                    raise TypeError(
                        "Argument {idx} is not of type '{expected_type}', " \
                            "but was of type '{actual_type}'".format(
                                idx=idx,
                                expected_type=expected_type_name,
                                actual_type=argument.__name__
                            )
                        )

            return func(*args)
        return wrapper
    return makewrapper


def tuple_parameter(index, types):
    '''
    Type checks the objects contained inside a tuple parameter

    index: the index in the args array of the tuple
    types: a tuple of types expected in the tuple parameter
    '''
    def makewrapper(func):
        @wraps(func)
        def wrapper(*args):
            if index > len(args):
                raise ValueError("Index %s is not a valid index" % index)
            items = args[index]
            if not isinstance(items, tuple):
                raise TypeError("Argument %s is not of type tuple" % index)
            if (len(items) != len(types)):
                if (len(items) % len(types) == 0):
                    real_types = types * int(len(items) / len(types))
                else:
                    raise ValueError("Incorrect number of expected types. Expected: {}  Actual: {}".format(len(types), len(items)))

            for i, arg in enumerate(zip(items, real_types)):
                if not isinstance(arg[0], arg[1]):
                    # This is not the most meaningful error
                    raise TypeError("Argument %s, in the tuple, is not of type '%s', but was of type '%s'" %
                                        (i, arg[1].__name__, type(arg[0]).__name__))
            return func(*args)
        return wrapper
    return makewrapper