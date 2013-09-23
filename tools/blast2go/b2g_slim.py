#!/usr/bin/env python
"""Send Blast2GO Annotation Table to map2slim for GO Slim."""

import sys
import gzip

_gzip_magic = '\x1f\x8b'

try:
    term_file = sys.argv[1]
    b2g_annot_file = sys.argv[2]
    gaf_file = sys.argv[3]
except ValueError:
    print "Bad args"
    sys.exit(1)

def gzip_open(filename, mode="rb"):
    assert mode=="rb", mode
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
            return "P"
        elif x in ["GO:0005575", "obsolete_cellular_component"]:
            return "C"
        elif x in ["GO:0003674", "obsolete_molecular_function"]:
            return "F"
        try:
            x = is_a[x]
        except KeyError:
            return "?"


def load_go_mapping(rdf_xml):
    """Quick and dirty GO RDF-XML parser."""
    sys.stderr.write("Loading %s\n" % rdf_xml)
    h = gzip_open(rdf_xml, "rb")

    names = dict()
    alias = dict()
    is_a = dict()

    go = None
    for line in h:
        #sys.stderr.write("... %r\n" % line)
        if "<go:accession>" in line:
            assert go is None, line
            go = line[line.find("<go:accession>")+14:]
            assert "</go:accession>" in line, line
            go = go[:go.find("</go:accession>")]
        elif "<go:name>" in line:            
            assert go is not None
            name = line[line.find("<go:name>")+9:]
            assert "</go:name>" in name, name
            name = name[:name.find("</go:name>")]
            names[go] = name
        elif "<go:synonym>GO:" in line:
            assert go is not None
            go2 = line[line.find("<go:synonym>GO:")+12:]
            assert "</go:synonym>" in line, line
            go2 = go2[:go2.find("</go:synonym>")]
            alias[go2] = go
        elif '<go:is_a rdf:resource="http://www.geneontology.org/go#GO:' in line and go:
            assert go is not None
            #e.g. <go:is_a rdf:resource="http://www.geneontology.org/go#GO:0008150" />
            thing = line[line.find('<go:is_a rdf:resource="http://www.geneontology.org/go#GO:')+54:]
            thing = thing[:thing.find('"')]
            is_a[go] = thing
        elif '<go:is_a rdf:resource="http://www.geneontology.org/go#obsolete_' in line and go:
            #i.e. <go:is_a rdf:resource="http://www.geneontology.org/go#obsolete_molecular_function" />
            #or   <go:is_a rdf:resource="http://www.geneontology.org/go#obsolete_biological_process" />
            thing = line[line.find('<go:is_a rdf:resource="http://www.geneontology.org/go#')+54:]
            thing = thing[:thing.find('"')]
            is_a[go] = thing
        elif "</go:term>" in line:
            go = None
    h.close()
    sys.stderr.write("%i names, %i aliases, %i parents\n" % (len(names), len(alias), len(is_a)))

    if "all" in names: del names["all"]
    
    for go in names:
        yield go, names[go], get_term_class(go, alias, is_a)
    for go in alias:
        if go not in names:
            go2 = alias[go]
            yield go, names[go2], get_term_class(go2, alias, is_a)


def b2g_annot_to_gaf(in_handle, out_handle):
    db = "LOCAL"
    qualifier = "NOT"
    db_ref = ""
    evidence_code = "ISA" # Inferred from Sequence Alignment
    with_or_from = ""
    taxon = ""
    date = "19700101" # Today?
    assigned_by = "LOCAL"
    annot_ext = ""
    gene_product_form_id = ""
    out_handle.write("!gaf-version: 2.0\n")
    for line in in_handle:
        identifier, go, descr = line.rstrip("\n").split("\t")
        go_name, term_class = go_terms[go]
        assert term_class in ["P", "F", "C"]
        fields = [db, identifier, identifier, qualifier, go,
                  db_ref, evidence_code, with_or_from, term_class,
                  taxon, date, assigned_by, annot_ext, gene_product_form_id]
        out_handle.write("\t".join(fields) + "\n")


go_terms = dict((go, (name, term_class)) for go, name, term_class, in load_go_mapping(term_file))

#Turn the Blast2GO Annotation Table into a minimal GAF file,
in_handle = open(b2g_annot_file)
out_handle = open(gaf_file, "w")
b2g_annot_to_gaf(in_handle, out_handle)
in_handle.close()
out_handle.close()

#Now, should be able call map2slim, ...
