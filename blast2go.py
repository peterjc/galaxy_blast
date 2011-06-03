#!/usr/bin/env python
"""Galaxy wrapper for Blast2GO for pipelines, b2g4pipe v2.3.5.

This script takes exactly three command line arguments:
 * Input BLAST XML filename
 * Blast2GO properties filename (settings file)
 * Output tabular filename

Sadly b2g4pipe v2.3.5 cannot cope with current style large BLAST XML
files (e.g. from BLAST 2.2.25+), so we have to reformat these to
avoid it crashing with a Java heap space OutOfMemoryError.

As part of this reformatting, we check for BLASTP or BLASTX output
(otherwise raise an error), and print the query count.

It then calls the Java command line tool, and moves the output file to
the location Galaxy is expecting, and removes the tempory XML file.
"""
import sys
import os
import subprocess

#You may need to edit this to match your local setup,
blast2go_jar = "/opt/b2g4pipe/blast2go.jar"


def stop_err(msg, error_level=1):
   """Print error message to stdout and quit with given error level."""
   sys.stderr.write("%s\n" % msg)
   sys.exit(error_level)

if len(sys.argv) != 4:
   stop_err("Require three arguments: XML filename, properties filename, output tabular filename")

xml_file, prop_file, tabular_file = sys.argv[1:]

#We should have write access here:
tmp_xml_file = tabular_file + ".tmp.xml"

if not os.path.isfile(xml_file):
   stop_err("Input BLAST XML file not found: %s" % xml_file)

if not os.path.isfile(prop_file):
   stop_err("Blast2GO configuration file not found: %s" % prop_file)

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


def run(cmd):
    #Avoid using shell=True when we call subprocess to ensure if the Python
    #script is killed, so too is the child process.
    try:
        child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception, err:
        stop_err("Error invoking command:\n%s\n\n%s\n" % (" ".join(cmd), err))
    #Use .communicate as can get deadlocks with .wait(),
    stdout, stderr = child.communicate()
    return_code = child.returncode
    if return_code:
        cmd_str = " ".join(cmd)
        if stderr and stdout:
            stop_err("Return code %i from command:\n%s\n\n%s\n\n%s" % (return_code, cmd_str, stdout, stderr))
        else:
            stop_err("Return code %i from command:\n%s\n%s" % (return_code, cmd_str, stderr))
    #For early diagnostics,
    else:
       print stdout
       print stderr

if not os.path.isfile(blast2go_jar):
   stop_err("Blast2GO JAR file not found: %s" % blast2go_jar)

prepare_xml(xml_file, tmp_xml_file)
#print "XML file prepared for Blast2GO"

#We will have write access wherever the output should be,
#so we'll ask Blast2GO to use that as the stem for its output
#(it will append .annot to the filename)
cmd = ["java", "-jar", blast2go_jar,
       "-in", tmp_xml_file,
       "-prop", prop_file,
       "-out", tabular_file, #Used as base name for output files
       "-a", # Generate *.annot tabular file
       #"-img", # Generate images, feature not in v2.3.5
       ]
#print " ".join(cmd)
run(cmd)

#Remove the temp XML file
os.remove(tmp_xml_file)

out_file = tabular_file + ".annot"
if not os.path.isfile(out_file):
   stop_err("ERROR - No output annotation file from Blast2GO")

#Move the output file where Galaxy expects it to be:
os.rename(out_file, tabular_file)

print "Done"
