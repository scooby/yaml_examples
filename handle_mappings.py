import yaml
from yaml import CLoader as Loader

def construct_mapping_kludge(loader, node):
    """ This constructor painfully steps through the node and checks
    that each key is hashable.  Actually, what it does is checks
    whether it knows how to *make* it hashable, and if so, does that.
    If not it just lets it through and hopes for the best. But the
    common problem cases are handled here.  If you're constructing
    objects directly from YAML, just make them immutable and hashable! """
    def anything(node):
        if isinstance(node, yaml.ScalarNode):
            return loader.construct_scalar(node)
        elif isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node)
        elif isinstance(node, yaml.MappingNode):
            return construct_mapping_kludge(loader, node)
    def make_hashable(value):
        """ Reconstructs a non-hashable value. """
        if isinstance(value, list):
            return tuple(map(make_hashable, value))
        elif isinstance(value, set):
            return frozenset(map(make_hashable, value))
        elif isinstance(value, dict):
            return tuple(sorted((make_hashable(key), val) for key, val in value.items()))
        else:
            return value
    def new_items():
        for k, v in node.value:
            yield (make_hashable(anything(k)), anything(v))
    return dict(new_items())
yaml.add_constructor(u'tag:yaml.org,2002:map', construct_mapping_kludge, Loader=Loader)

tricky=u""" !!map { [ New York Yankees, Atlanta Braves ]: [ 2001-07-02, 2001-08-12, 2001-08-14 ] } """

print(repr(yaml.load(tricky, Loader=Loader)))
