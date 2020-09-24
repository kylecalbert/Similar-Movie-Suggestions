# -*- coding: utf-8 -*-


from .compat import literal_eval


class DictSnippets(object):
    def __init__(self):
        self.separtor = ':'

    def eval_string(self, string):
        try:
            return literal_eval(string)
        except (SyntaxError, ValueError):
            return string

    def filter(self, obj, kvlist, exec_eval=True):
        _obj = {}
        for kv in kvlist:
            k, v = kv.split(self.separtor) if self.separtor in kv else [kv, '']
            _obj[k] = obj.get(k, self.eval_string(v) if exec_eval else v)
        return _obj

    def gets(self, obj, kvlist, exec_eval=True):
        """
        Get Multiple Values
        See: http://stackoverflow.com/questions/18453566/python-dictionary-get-list-of-values-for-list-of-keys
        :param obj:
        :param kvlist:
        :param exec_eval:
        :return:
        """
        _val = []
        for kv in kvlist:
            k, v = kv.split(self.separtor) if self.separtor in kv else [kv, '']
            _val.append(obj.get(k, self.eval_string(v) if exec_eval else v))
        return _val


_global_instance = DictSnippets()
filter = _global_instance.filter
gets = _global_instance.gets
