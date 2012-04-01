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
