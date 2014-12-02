#!/usr/bin/env python
"""Script for reformatting Blast XML to suit Blast2GO.

This script takes exactly two command line arguments:
 * Input BLAST XML filename
 * Output BLAST XML filename

Sadly b2g4pipe (at least v2.3.5 to v2.5.0) cannot cope with current
style large BLAST XML files (e.g. from BLAST 2.2.25+), so we reformat
these to avoid it crashing with a Java heap space OutOfMemoryError.

As part of this reformatting, we check for BLASTP or BLASTX output
(otherwise raise an error), and print the query count.

This script is called from my Galaxy wrapper for Blast2GO for pipelines,
available from the Galaxy Tool Shed here:
http://toolshed.g2.bx.psu.edu/view/peterjc/blast2go 

This script is under version control here:
https://github.com/peterjc/galaxy_blast/tree/master/blast2go
"""
import sys
import os

def stop_err(msg, error_level=1):
    """Print error message to stdout and quit with given error level."""
    sys.stderr.write("%s\n" % msg)
    sys.exit(error_level)

def prepare_xml(original_xml, mangled_xml):
    """Reformat BLAST XML to suit Blast2GO.

    Blast2GO can't cope with 1000s of <Iteration> tags within a
    single <BlastResult> tag, so instead split this into one
    full XML record per interation (i.e. per query). This gives
    a concatenated XML file mimicing old versions of BLAST.

    This also checks for BLASTP or BLASTX output, and outputs
    the number of queries. Galaxy will show this as "info".
    """
    in_handle = open(original_xml)
    footer = "  </BlastOutput_iterations>\n</BlastOutput>\n"
    header = ""
    while True:
        line = in_handle.readline()
        if not line:
            #No hits?
            stop_err("Problem with XML file?")
        if line.strip() == "<Iteration>":
            break
        header += line

    if "<BlastOutput_program>blastx</BlastOutput_program>" in header:
        print "BLASTX output identified"
    elif "<BlastOutput_program>blastp</BlastOutput_program>" in header:
        print "BLASTP output identified"
    else:
        in_handle.close()
        stop_err("Expect BLASTP or BLASTX output")

    out_handle = open(mangled_xml, "w")
    out_handle.write(header)
    out_handle.write(line)
    count = 1
    while True:
        line = in_handle.readline()
        if not line:
            break
        elif line.strip() == "<Iteration>":
           #Insert footer/header
           out_handle.write(footer)
           out_handle.write(header)
           count += 1
        out_handle.write(line)

    out_handle.close()
    in_handle.close()
    print "Input has %i queries" % count


if __name__ == "__main__":
    # Run the conversion...
    if len(sys.argv) != 3:
        stop_err("Require two arguments: XML input filename, XML output filename")

    xml_file, out_xml_file = sys.argv[1:]

    if not os.path.isfile(xml_file):
        stop_err("Input BLAST XML file not found: %s" % xml_file)

    prepare_xml(xml_file, out_xml_file)
