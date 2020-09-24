# -- coding: utf-8 --

from __future__ import division

import monetary
import screen
from django import template
from django.utils.encoding import force_text
from pysnippets import strsnippets as ssn


register = template.Library()


###################
# Formats         #
###################
def googol_number_format(value, dividend, ndigits='auto'):
    if ndigits == 'auto':
        ndigits = 0 if value % dividend == 0 else 2
    if ndigits == 0:
        return int(value / dividend)
    return round(value / dividend, ndigits)


def __googolformat(value, ndigits='auto', suffix=True):
    value = value or 0

    negative = value < 0

    if negative:
        value = -value

    if value < 10000:
        pass
    elif value < 100000000:
        value = '%s %s' % (googol_number_format(value, 10000, ndigits=ndigits), u'万' if suffix else '')
    else:
        value = '%s %s' % (googol_number_format(value, 100000000, ndigits=ndigits), u'亿' if suffix else '')

    if negative:
        value = "-%s" % value

    return value


@register.filter(is_safe=True)
def googolformat(value, ndigits='auto'):
    return __googolformat(value, ndigits=ndigits, suffix=True)


@register.filter(is_safe=True)
def googolformat2(value, ndigits='auto'):
    return __googolformat(value, ndigits=ndigits, suffix=False)


###################
# Monetary        #
###################
@register.filter(is_safe=True)
def fen2yuan(value, ndigits='auto'):
    """
    分 => 元，保留 ndigits 位小数

    :value|fen2yuan
    :value|fen2yuan:ndigits
    """
    value = value or 0
    if ndigits == 'auto':
        ndigits = 0 if value % 100 == 0 else 2
    if ndigits == 0:
        return int(value / 100)
    return monetary.Fen2Yuan(value, ndigits=ndigits)


###################
# Truncate        #
###################
@register.filter(is_safe=True)
def truncatechars2(value, arg):
    """
    :value|truncatechars2:length
    :value|truncatechars2:'length,truncate'
    """
    if not value:
        return ''
    truncate = '...'
    if isinstance(arg, int):
        length, truncate = arg, truncate
    else:
        bits = arg.split(',')
        try:
            length, truncate = bits
        except ValueError:
            length, truncate = bits[0], truncate
    try:
        length = int(length)
    except ValueError:
        return value
    value = force_text(value)
    if len(value) <= length:
        return value
    return '%s%s' % (value[:length], truncate)


@register.filter(is_safe=True)
def truncatewidth(value, arg):
    """
    :value|truncatewidth:length
    :value|truncatewidth:'length,truncate'
    """
    if not value:
        return ''
    truncate = '...'
    if isinstance(arg, int):
        length, truncate = arg, truncate
    else:
        bits = arg.split(',')
        try:
            length, truncate = bits
        except ValueError:
            length, truncate = bits[0], truncate
    try:
        length = int(length)
    except ValueError:
        return value
    value = force_text(value)
    if len(value) <= length:
        return value
    truncated = value[:screen.calc_text_pos(value, 0, len(value), length * 2)[0]]
    if value != truncated:
        truncated = '%s%s' % (truncated, truncate)
    return truncated


###################
# Line Break      #
###################
@register.filter(is_safe=True)
def remove_line_break(value, repl=' '):
    """
    :value|remove_line_break
    :value|remove_line_break:repl
    """
    if not value:
        return ''
    value = force_text(value)
    return ssn.removeLineBreak(value, repl=repl)
