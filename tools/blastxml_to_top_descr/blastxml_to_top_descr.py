#!/usr/bin/env python
"""Convert a BLAST XML file to a top hits description table.

Takes three command line options, input BLAST XML filename, output tabular
BLAST filename, number of hits to collect the descriptions of.
"""
import sys
import re
from optparse import OptionParser

if "-v" in sys.argv or "--version" in sys.argv:
    print "v0.1.0"
    sys.exit(0)

if sys.version_info[:2] >= ( 2, 5 ):
    import xml.etree.cElementTree as ElementTree
else:
    from galaxy import eggs
    import pkg_resources; pkg_resources.require( "elementtree" )
    from elementtree import ElementTree

def stop_err( msg ):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)

usage = """Use as follows:

$ blastxml_to_top_descr.py [-t 3] -o example.tabular input.xml

Or,

$ blastxml_to_top_descr.py [--topN 3] --output example.tabular input.xml

This will take the top 3 BLAST descriptions from the input BLAST XML file,
writing them to the specified output file in tabular format.
"""

parser = OptionParser(usage=usage)
parser.add_option("-t", "--topN", dest="topN", default=3,
                  help="Number of descriptions to collect")
parser.add_option("-o", "--output", dest="out_file", default=None,
                  help="Output filename for tabular file",
                  metavar="FILE")
parser.add_option("-f", "--format", dest="format", default="blastxml",
                  help="Input format (blastxml or tabular)")
parser.add_option("-q", "--qseqid", dest="qseqid", default="1",
                  help="Column for query 'qseqid' (for tabular input; default 1)")
parser.add_option("-s", "--sseqid", dest="sseqid", default="2",
                  help="Column for subject 'sseqid' (for tabular input; default 2)")
parser.add_option("-b", "--bitscore", dest="bitscore", default="12",
                  help="Column for bitscore (for tabular input; default 12)")
parser.add_option("-d", "--salltitles", dest="salltitles", default="25",
                  help="Column for descriptions 'salltitles' (for tabular input; default 25)")
(options, args) = parser.parse_args()

if len(sys.argv) == 4 and len(args) == 3 and not options.out_file:
    stop_err("""The API has changed, replace this:

$ python blastxml_to_top_descr.py input.xml output.tab 3

with:

$ python blastxml_to_top_descr.py -o output.tab -t 3 input.xml

Sorry.
""")

if not args:
    stop_err("Input filename missing, try -h")
if len(args) > 1:
    stop_err("Expects a single argument, one input filename")
in_file = args[0]
out_file = options.out_file
topN = options.topN

try:
    topN = int(topN)
except ValueError:
    stop_err("Number of hits  argument should be an integer (at least 1)")
if topN < 1:
    stop_err("Number of hits  argument should be an integer (at least 1)")


if options.format != "blastxml":
    stop_err("Not implemented yet.")

# get an iterable
try: 
    context = ElementTree.iterparse(in_file, events=("start", "end"))
except:
    stop_err("Invalid data format.")
# turn it into an iterator
context = iter(context)
# get the root element
try:
    event, root = context.next()
except:
    stop_err( "Invalid data format." )


re_default_query_id = re.compile("^Query_\d+$")
assert re_default_query_id.match("Query_101")
assert not re_default_query_id.match("Query_101a")
assert not re_default_query_id.match("MyQuery_101")
re_default_subject_id = re.compile("^Subject_\d+$")
assert re_default_subject_id.match("Subject_1")
assert not re_default_subject_id.match("Subject_")
assert not re_default_subject_id.match("Subject_12a")
assert not re_default_subject_id.match("TheSubject_1")


count = 0
pos_count = 0
if out_file is None:
    outfile = sys.stdout
else:
    outfile = open(out_file, 'w')
outfile.write("#Query\t%s\n" % "\t".join("BLAST hit %i" % (i+1) for i in range(topN)))
for event, elem in context:
    # for every <Iteration> tag
    if event == "end" and elem.tag == "Iteration":
        #Expecting either this, from BLAST 2.2.25+ using FASTA vs FASTA
        # <Iteration_query-ID>sp|Q9BS26|ERP44_HUMAN</Iteration_query-ID>
        # <Iteration_query-def>Endoplasmic reticulum resident protein 44 OS=Homo sapiens GN=ERP44 PE=1 SV=1</Iteration_query-def>
        # <Iteration_query-len>406</Iteration_query-len>
        # <Iteration_hits></Iteration_hits>
        #
        #Or, from BLAST 2.2.24+ run online
        # <Iteration_query-ID>Query_1</Iteration_query-ID>
        # <Iteration_query-def>Sample</Iteration_query-def>
        # <Iteration_query-len>516</Iteration_query-len>
        # <Iteration_hits>...
        qseqid = elem.findtext("Iteration_query-ID")
        if qseqid is None:
            stop_err("Missing <Iteration_query-ID> (could be really old BLAST XML data?)")
        if re_default_query_id.match(qseqid):
            #Place holder ID, take the first word of the query definition
            qseqid = elem.findtext("Iteration_query-def").split(None,1)[0]
        # for every <Hit> within <Iteration>
        hit_descrs = []
        for hit in elem.findall("Iteration_hits/Hit"):
            #Expecting either this,
            # <Hit_id>gi|3024260|sp|P56514.1|OPSD_BUFBU</Hit_id>
            # <Hit_def>RecName: Full=Rhodopsin</Hit_def>
            # <Hit_accession>P56514</Hit_accession>
            #or,
            # <Hit_id>Subject_1</Hit_id>
            # <Hit_def>gi|57163783|ref|NP_001009242.1| rhodopsin [Felis catus]</Hit_def>
            # <Hit_accession>Subject_1</Hit_accession>
            #
            #apparently depending on the parse_deflines switch
            sseqid = hit.findtext("Hit_id").split(None,1)[0]
            hit_def = sseqid + " " + hit.findtext("Hit_def")
            if re_default_subject_id.match(sseqid) \
            and sseqid == hit.findtext("Hit_accession"):
                #Place holder ID, take the first word of the subject definition
                hit_def = hit.findtext("Hit_def")
                sseqid = hit_def.split(None,1)[0]
            assert hit_def not in hit_descrs
            hit_descrs.append(hit_def)
        #print "%r has %i hits" % (qseqid, len(hit_descrs))
        if hit_descrs:
            pos_count += 1
        hit_descrs = hit_descrs[:topN]
        while len(hit_descrs) < topN:
            hit_descrs.append("")
        outfile.write("%s\t%s\n" % (qseqid, "\t".join(hit_descrs)))
        count += 1
        # prevents ElementTree from growing large datastructure
        root.clear()
        elem.clear()
if out_file is not None:
    outfile.close()
print "Of %i queries, %i had BLAST results" % (count, pos_count)
