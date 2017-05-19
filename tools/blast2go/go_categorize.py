from __future__ import print_function

import gzip
import sys

_gzip_magic = '\x1f\x8b'


def gzip_open(filename, mode="rb"):
    assert mode == "rb", mode
    h = open(filename, "rb")
    magic = h.read(2)
    h.seek(0)
    if magic == _gzip_magic:
        h.close()
        sys.stderr.write("%s is gzipped\n" % filename)
        return gzip.open(filename, "rb")
    else:
        sys.stderr.write("%s isn't compressed\n" % filename)
        return h


def get_term_class(go, alias, is_a):
    x = alias.get(go, go)
    while x:
        if x in ["GO:0008150", "obsolete_biological_process"]:
            return "BP"
        elif x in ["GO:0005575", "obsolete_cellular_component"]:
            return "CC"
        elif x in ["GO:0003674", "obsolete_molecular_function"]:
            return "MF"
        try:
            x = is_a[x]
        except KeyError:
            return "??"


def load_go_mapping(rdf_xml):
    """Quick and dirty GO RDF-XML parser."""
    sys.stderr.write("Loading %s\n" % rdf_xml)
    h = gzip_open(rdf_xml, "rb")

    names = dict()
    alias = dict()
    is_a = dict()

    go = None
    for line in h:
        # sys.stderr.write("... %r\n" % line)
        if "<go:accession>" in line:
            assert go is None, line
            go = line[line.find("<go:accession>") + 14:]
            assert "</go:accession>" in line, line
            go = go[:go.find("</go:accession>")]
        elif "<go:name>" in line:
            assert go is not None
            name = line[line.find("<go:name>") + 9:]
            assert "</go:name>" in name, name
            name = name[:name.find("</go:name>")]
            names[go] = name
        elif "<go:synonym>GO:" in line:
            assert go is not None
            go2 = line[line.find("<go:synonym>GO:") + 12:]
            assert "</go:synonym>" in line, line
            go2 = go2[:go2.find("</go:synonym>")]
            alias[go2] = go
        elif '<go:is_a rdf:resource="http://www.geneontology.org/go#GO:' in line and go:
            assert go is not None
            # e.g. <go:is_a rdf:resource="http://www.geneontology.org/go#GO:0008150" />
            thing = line[line.find('<go:is_a rdf:resource="http://www.geneontology.org/go#GO:') + 54:]
            thing = thing[:thing.find('"')]
            is_a[go] = thing
        elif '<go:is_a rdf:resource="http://www.geneontology.org/go#obsolete_' in line and go:
            # i.e. <go:is_a rdf:resource="http://www.geneontology.org/go#obsolete_molecular_function" />
            # or   <go:is_a rdf:resource="http://www.geneontology.org/go#obsolete_biological_process" />
            thing = line[line.find('<go:is_a rdf:resource="http://www.geneontology.org/go#') + 54:]
            thing = thing[:thing.find('"')]
            is_a[go] = thing
        elif "</go:term>" in line:
            go = None
    h.close()
    sys.stderr.write("%i names, %i aliases, %i parents\n" % (len(names), len(alias), len(is_a)))

    if "all" in names:
        del names["all"]

    for go in names:
        yield go, names[go], get_term_class(go, alias, is_a)


for go, name, term_class, in load_go_mapping(sys.argv[1]):
    print(go, term_class, name)
