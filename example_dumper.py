import yaml
# Other ways to set Loader:
#from yaml import Loader as Loader
from yaml import CLoader as Loader
# from yaml import CSafeLoader as Loader
# from yaml import SafeLoader as Loader

# If you *don't* specify your loader in some places, you'll
# break. Always pass the Loader=Loader parameter, and set the
# yaml_loader=Loader class variable.

class GenericScalar(yaml.YAMLObject):
    yaml_loader=Loader
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.value,)
    @classmethod
    def from_yaml(cls, loader, node):
        return cls(loader.construct_scalar(node))

# A bunch of scalar based classes to get the examples in the spec loading correctly.
class Something(GenericScalar):
    yaml_tag = u'!something'

class Local(GenericScalar):
    yaml_tag = u'!local'

class Bar(GenericScalar):
    yaml_tag = u'!bar'

class Huh(GenericScalar):
    yaml_tag = u'tag:ben-kiki.org,2000:type'

class Stringy(GenericScalar):
    yaml_tag = u'!str'

# Not sure the parser is getting this right. Should !!str, really pick up this tag?
yaml.add_constructor(u'tag:yaml.org,2002:str,', lambda l, n: "")

def construct_mapping_kludge(loader, node):
    """ This constructor painfully steps through the node and checks
    that each key is hashable.  Actually, what it does is checks
    whether it knows how to *make* it hashable, and if so, does that.
    If not it just lets it through and hopes for the best. But the
    common problem cases are handled here.  If you're constructing
    objects directly from YAML, just make them immutable and hashable!
    """
    def anything(node):
        if isinstance(node, yaml.ScalarNode):
            return loader.construct_scalar(node)
        elif isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node)
        elif isinstance(node, yaml.MappingNode):
            return loader.construct_sequence(node)
    def make_hashable(value):
        if isinstance(value, list):
            return tuple(value)
        elif isinstance(value, set):
            return frozenset(value)
        elif isinstance(value, dict):
            return tuple(sorted(value.items()))
        else:
            return value
    def new_items():
        for k, v in node.value:
            yield (make_hashable(anything(k)), anything(v))
    return dict(new_items())
yaml.add_constructor(u'tag:yaml.org,2002:map', construct_mapping_kludge, Loader=Loader)

class BunchOShapes(yaml.YAMLObject):
    """ You can figure out the tag from the error message:
    yaml.constructor.ConstructorError: could not determine a
    constructor for the tag 'tag:clarkevans.com,2002:shape'"""
    yaml_tag = u'tag:clarkevans.com,2002:shape'
    yaml_loader=Loader
    def __init__(self, *shapes):
        self.shapes = shapes
    def __repr__(self):
        return "BunchOShapes(%r)" % (self.shapes,)
    @classmethod
    def from_yaml(cls, loader, node):
        return cls(*loader.construct_sequence(node))

class Circle(yaml.YAMLObject):
    yaml_tag=u'tag:clarkevans.com,2002:circle'
    yaml_loader=Loader
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    def __repr__(self):
        return "Circle(%r, %r)" % (self.center, self.radius)
class Line(yaml.YAMLObject):
    yaml_tag=u'tag:clarkevans.com,2002:line'
    yaml_loader=Loader
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish
    def __repr__(self):
        return "Line(%r, %r)" % (self.start, self.finish)
class Label(yaml.YAMLObject):
    yaml_tag=u'tag:clarkevans.com,2002:label'
    yaml_loader=Loader
    def __init__(self, start, color, text):
        self.start = start
        self.color = color
        self.text = text
    def __repr__(self):
        return "Label(%r, %r, %r)" % (self.start, self.color, self.text)

class Invoice(yaml.YAMLObject):
    yaml_tag=u'tag:clarkevans.com,2002:invoice'
    yaml_loader=Loader
    def __init__(self, **args):
        self.data = args
        print repr(args)
    def __repr__(self):
        data = getattr(self, 'data', {})
        return "Invoice(%s)" % (', '.join("%s=%r" % (k, v) for k, v in data.items()),)
    @classmethod
    def from_yaml(cls, loader, node):
        """ I suspect the default won't work with invoices (it doesn't
        call the __init__ method) because there are -'s in some of the
        keys. """
        value = loader.construct_mapping(node)
        args = dict((k.replace('-', '_'), v) for k, v in value.items())
        return cls(**args)

with open("yaml_examples.yml", "r") as yaml_fh:
    for doc in yaml.load_all(yaml_fh, Loader=Loader):
        print(repr(doc))
