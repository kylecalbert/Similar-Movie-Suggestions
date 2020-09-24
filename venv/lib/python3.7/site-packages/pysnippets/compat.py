# -*- coding: utf-8 -*-

"""
pythoncompat
"""

import sys


# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

try:
    from ast import literal_eval
except (ImportError, SyntaxError):
    # See: https://docs.python.org/2/library/ast.html
    # 32.2. ast — Abstract Syntax Trees
    # New in version 2.5: The low-level _ast module containing only the node classes.
    # New in version 2.6: The high-level ast module containing all helpers.
    literal_eval = eval

# ---------
# Specifics
# ---------

if is_py2:
    range = xrange

    builtin_str = str
    bytes = str
    str = unicode
    basestring = basestring
    numeric_types = (int, long, float)

    import __builtin__
    builtins = __builtin__

    from cgi import escape as html_escape

elif is_py3:
    range = range

    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    numeric_types = (int, float)

    import builtins
    builtins = builtins

    from html import escape as html_escape
