import yaml
from yaml import CLoader as Loader

def construct_mapping_kludge(loader, node):
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
yaml.add_constructor(u'tag:yaml.org,2002:map', construct_mapping_safely, Loader=Loader)

tricky=u""" !!map { [ New York Yankees, Atlanta Braves ]: [ 2001-07-02, 2001-08-12, 2001-08-14 ] } """

print(repr(yaml.load(tricky, Loader=Loader)))
