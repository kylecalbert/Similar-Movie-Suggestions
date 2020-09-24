# Author: Jonathan Slenders, City Live

from django.template import Node, NodeList, Variable
from django.template import TemplateSyntaxError, VariableDoesNotExist
from django.template import Library
from django.conf import settings
from django.template.loader import get_template

import copy

"""
Decorator Pattern for Django Templates.


    In template.html:
        <p>
            {% decorate "decorator.html" %}
                example
            {% endifdebug %}
        </p>

    In decorator.html:
        <span>
            {{ decorator.content }}
        </span>

    Result:
        <p>
            <span>
                example
            </span>
        </p>
"""

register = Library()

class DecorateNode(Node):
    def __init__(self, template_name, nodelist):
        self.template_name = Variable(template_name)
        self.nodelist = nodelist

    def __repr__(self):
        return "<Decorate node>"

    def __iter__(self):
        for node in self.nodelist:
            yield node

    def get_nodes_by_type(self, nodetype):
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        nodes.extend(self.nodelist.get_nodes_by_type(nodetype))
        return nodes

    def render(self, context):
        # Decorator template
        template_name = self.template_name.resolve(context)
        t = get_template(template_name)

        # Helper method for copying context
        def copy_context(context):
            """
            Create copy of django.template.context.BaseContext
            Don't use the push/pop mechanism, because we need the old context
            and new context at the same time. Making a deep copy of the context
            does not work (and would be slow.) But creating a copy of the dicts
            list is required.
            """
            new_context = copy.copy(context)
            new_context.dicts = copy.copy(context.dicts)
            return new_context

        # In order to render the decorator node,
        # All we have to do is render the decorator file.
        # but lazy-add the rendered nodelist to decorator.content.

        # Create lazy nodelist object
        class decorator(object):
            @property
            def content(self_2):
                result = self.nodelist.render(context)
                return result

        # Create new context to render the decorator into.
        new_context = copy_context(context)
        new_context.render_context = copy_context(context.render_context)
        new_context['decorator'] = decorator()

            # NOTE: we really need to copy the render_context as well, because
            #       Django's implementation of block inheritance will change
            #       the render context

        # Render the decorator template in the new context
        return t.render(new_context)


@register.tag
def decorate(parser, token):
    # Template name parameter
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError, '{% decorate "template.html" %} tag requires a template name as arguments'
    path = bits[1]

    # Content
    nodelist = parser.parse(('enddecorate', ))
    parser.delete_first_token()

    return DecorateNode(path, nodelist)

