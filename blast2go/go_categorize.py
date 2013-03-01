import sys
import gzip

_gzip_magic = '\x1f\x8b'

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

def load_go_mapping(rdf_xml):
    """Quick and dirty GO RDF-XML parser."""
    sys.stderr.write("Loading %s\n" % rdf_xml)
    h = gzip_open(rdf_xml, "rb")

    go = None
    for line in h:
        #sys.stderr.write("... %r\n" % line)
        if "<go:accession>" in line:
            go = line[line.find("<go:accession>")+14:]
            assert "</go:accession>" in line, line
            go = go[:go.find("</go:accession>")]
        elif "<go:name>" in line:            
            assert go is not None
            name = line[line.find("<go:name>")+9:]
            assert "</go:name>" in name, name
            name = name[:name.find("</go:name>")]
            yield go, name
            go = None
        # On some files this was near the end and a good break
        # point, but on others it is at the start instead
        #elif "<go:accession>all</go:accession>" in line:
        #    break
    h.close()

for go, name in load_go_mapping(sys.argv[1]):
    print go, name
