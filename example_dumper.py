import yaml

class GenericScalar(yaml.YAMLObject):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.value,)
    @classmethod
    def from_yaml(cls, loader, node):
        return cls(loader.construct_scalar(node))

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

yaml.add_constructor(u'tag:yaml.org,2002:str,', lambda l, n: None)

class BunchOShapes(yaml.YAMLObject):
    """ You can figure out the tag from the error message:
    yaml.constructor.ConstructorError: could not determine a
    constructor for the tag 'tag:clarkevans.com,2002:shape'"""
    yaml_tag = u'tag:clarkevans.com,2002:shape'
    def __init__(self, *shapes):
        self.shapes = shapes
    def __repr__(self):
        return "BunchOShapes(%r)" % (self.shapes,)
    @classmethod
    def from_yaml(cls, loader, node):
        return cls(*loader.construct_sequence(node))

class Circle(yaml.YAMLObject):
    yaml_tag=u'tag:clarkevans.com,2002:circle'
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    def __repr__(self):
        return "Circle(%r, %r)" % (self.center, self.radius)
class Line(yaml.YAMLObject):
    yaml_tag=u'tag:clarkevans.com,2002:line'
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish
    def __repr__(self):
        return "Line(%r, %r)" % (self.start, self.finish)
class Label(yaml.YAMLObject):
    yaml_tag=u'tag:clarkevans.com,2002:label'
    def __init__(self, start, color, text):
        self.start = start
        self.color = color
        self.text = text
    def __repr__(self):
        return "Label(%r, %r, %r)" % (self.start, self.color, self.text)

class Invoice(yaml.YAMLObject):
    yaml_tag=u'tag:clarkevans.com,2002:invoice'
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
    for doc in yaml.load_all(yaml_fh):
        print(repr(doc))
