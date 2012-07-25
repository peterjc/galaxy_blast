#!/usr/bin/env python
"""Convert a BLAST XML file to a top hits description table.

Takes three command line options, input BLAST XML filename, output tabular
BLAST filename, number of hits to collect the descriptions of.
"""
import sys
import re

if sys.version_info[:2] >= ( 2, 5 ):
    import xml.etree.cElementTree as ElementTree
else:
    from galaxy import eggs
    import pkg_resources; pkg_resources.require( "elementtree" )
    from elementtree import ElementTree

def stop_err( msg ):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)

#Parse Command Line
try:
    in_file, out_file, topN = sys.argv[1:]
except:
    stop_err("Expect 3 arguments: input BLAST XML file, output tabular file, number of hits")


try:
    topN = int(topN)
except ValueError:
    stop_err("Number of hits  argument should be an integer (at least 1)")
if topN < 1:
    stop_err("Number of hits  argument should be an integer (at least 1)")

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
        hit_descrs = hit_descrs[:topN]
        while len(hit_descrs) < topN:
            hit_descrs.append("")
        outfile.write("%s\t%s\n" % (qseqid, "\t".join(hit_descrs)))
        count += 1
        # prevents ElementTree from growing large datastructure
        root.clear()
        elem.clear()
outfile.close()
print "%i BLAST results" % count
