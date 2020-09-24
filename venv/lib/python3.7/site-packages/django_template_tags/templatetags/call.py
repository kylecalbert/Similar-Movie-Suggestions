from django.template import Library, Node, TemplateSyntaxError, VariableDoesNotExist
from cgi import escape

# Author: Jonathan Slenders, CityLive

# "Call" template tag
# Calls a function with given parameters, and place result in context
# Note that the function itself is also resolved from the context.

# If the context looks like:
#    from django_template_tags.template_callable import template_callable
#    context = [ 'func': template_callable(lambda x,y: x+y), 'arg1': 4, 'arg2': 5 ]

# The following will print '9' in the template
#    {% call result = func arg1 arg2 %}
#    {{ result }}

# Instead of assignment to a variable also the following can be done.

# {% call func arg1 arg2 %}


register = Library()

class CallNode(Node):
    def __init__(self, method, params, result=None):
        self.method = method
        self.result = result
        self.params = params

    def render(self, context):
        try:
            # Resolve function name and parameters
            method = self.method.resolve(context, True)
            params = [ p.resolve(context, True) for p in self.params ]

            # Call method
            if method:
                # If
                result = method(*params) if callable(method) else method.call(*params)
            else:
                result = None

            if self.result:
                # Place result in context
                context[self.result] = result
                return ''
            else:
                # Return result (will be printed in template node)
                return escape(result) if result else ''

        except VariableDoesNotExist:
            return 'VariableDoesNotExist error while calling function %s' % str(self.method)


@register.tag(name='call')
def call_node(parser, token):
    bits = token.contents.split()
    if '=' in bits:
        if len(bits) <= 3:
            raise TemplateSyntaxError, "call tag least argument error"
        if bits[2] != '=':
            raise TemplateSyntaxError, "second argument shoud be '='"

        return CallNode(
            result=bits[1],
            method=parser.compile_filter(bits[3]),
            params=[ parser.compile_filter(x) for x in  bits[4:] ])
    else:
        if len(bits) <= 2:
            raise TemplateSyntaxError, "call tag least argument error"

        return CallNode(
            method=parser.compile_filter(bits[1]),
            params=[ parser.compile_filter(x) for x in  bits[2:] ])
