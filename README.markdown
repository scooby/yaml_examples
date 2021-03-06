What is it
----------

I'm using YAML in another project, and I originally thought I'd just
put some snippets together.

But I wound up doing a number of short tests to see what the basic
yaml module in Python thinks. As this is getting a bit long to be a
gist, I'm just putting it up in a repo.

Helpful tools
-------------

I'm using yaml_mode in emacs to edit; it's reasonably good, but
doesn't give you much help.

I've also done a few tests with Perl; if you have YAML::XS, try:

    cat | perl -MYAML::XS -MData::Dumper \
    -e 'print Dumper(Load(join("", <STDIN>)))'

Or install ysh from libyaml-shell-perl on debian derived systems.

TODOs
-----

Pull the Unicode linebreak tests out into a separate file so they
don't confuse every tool (which is almost all of them) that doesn't
grok Unicode linebreaks.

PROBABLY NOT GOING TODOs
------------------------

Put together an actual makefile to test that stuff works with
different combinations of language, test and whatever. After all,
someone must have done this, right?

Caveats / broken promises
-------------------------

In many cases, YAML will happily let you express things that are
perfectly valid YAML, but that make no sense.

Much of the specs are like this, and in fairness, there were only a
few things that didn't parse.

My big annoyance is that YAML allows mappings to have complex keys and
python does too, so this should work, right?

    [ foo, bar ] : stuff

Not a chance. The sequence is translated to a Python list, not a
Python tuple. A Python dict can't have a modifiable object as a
key. In fact, if you're using the dominant heap-centric view of
objects, it is pretty much impossible to have a mapping data-type
whose keys are modifiable.

There's an issue attached to this that claims it's not a bug. The docs
show that you can create complex keys by demonstrating:

    ? !!python/tuple [ foo, bar ] : stuff

But once you've got !!python in there, you may as well use pickle.

Before we try to fix this, how do we handle:

    - &test [ 1, 2, 3, 4 ]
    - ? *test
      : *test

I'm perfectly happy, the way I work, for the loader to recast this as:

    - &test [ 1, 2, 3, 4 ]
    - ? !!python/tuple [ 1, 2, 3, 4]
      : *test

But that might not suit others. YAML doesn't make strong guarantees
that, after loading, different YAML nodes represent different objects
in the heap.
