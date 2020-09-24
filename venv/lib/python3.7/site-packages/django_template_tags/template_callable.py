# Author: Jonathan Slenders, City Live


class template_callable(object):
    """
    Decorator for passing callables into the template.

    This decorator avoids the callables to be called
    directly when resolved from the template.
    The {% call %} template tag will call the proper function
    when required.
    (A change in Django 1.3 requires the use of this decorator.)
    """
    def __init__(self, func):
        self.func = func

    def call(self, *args, **kwargs):
        return self.func(*args, **kwargs)
