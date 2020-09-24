# -*- coding: utf-8 -*-

from .compat import builtins


class ListSnippets(object):
    def all(self, list_, eles):
        return builtins.all([ele in list_ for ele in eles])

    def any(self, list_, eles):
        return builtins.any([ele in list_ for ele in eles])


_global_instance = ListSnippets()
all = _global_instance.all
any = _global_instance.any
