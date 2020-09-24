# Author: Jonathan Slenders

from django.template import Node, NodeList, Variable
from django.template import TemplateSyntaxError, VariableDoesNotExist
from django.template import Library

register = Library()

#
# The macro tag avoids the need of unnecessarily having to repeat template code.
# Similar to methods:
#
# e.g.
# {% load macro %}
# {% macro "macroname" %}
#     {% trans "this is code inside the macro" %}
# {% endmacro %}

# Later on:
# {% callmacro "macroname" %}


class MacroNode(Node):
    def __init__(self, name, nodelist):
        self.name = name
        self.nodelist = nodelist

    def render(self, context):
        # When the macro node is 'rendered',
        # don't output anything, but place the macro
        # node itself in the context

        name = Variable(self.name).resolve(context)
        context[name] = self

        return ''

@register.tag(name='macro')
def macro(parser, token):
    """
    {% macro "name" %} content nodes {% endmacro %}
    """
    # Parameters
    args = token.split_contents()

    # Read nodelist
    nodelist = parser.parse(('endmacro',))
    parser.delete_first_token()

    # Return meta node
    return MacroNode(args[1], nodelist)


class CallMacroNode(Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        # Look for the macro in the context
        # and render it now in the current context

        name = Variable(self.name).resolve(context)
        macro = context[name]

        if not isinstance(macro, MacroNode):
            return '<strong>{% callmacro %} ERROR: What you called is not a macro</strong>'

        return macro.nodelist.render(context)


@register.tag(name='callmacro')
def call_macro(parser, token):
    """
    {% callmacro "name" %}
    """
    # Parameters
    args = token.split_contents()

    # Return meta node
    return CallMacroNode(args[1])
