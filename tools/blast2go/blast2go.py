#!/usr/bin/env python
"""Galaxy wrapper for Blast2GO for pipelines, b2g4pipe v2.5.

This script takes exactly three command line arguments:
 * Input BLAST XML filename
 * Blast2GO properties filename (settings file)
 * Output tabular filename

The properties filename can be a fully qualified path, but if not
this will look next to the blast2go.jar file.

Sadly b2g4pipe (at least v2.3.5 to v2.5.0) cannot cope with current
style large BLAST XML files (e.g. from BLAST 2.2.25+), so we reformat
these to avoid it crashing with a Java heap space OutOfMemoryError.

As part of this reformatting, we check for BLASTP or BLASTX output
(otherwise raise an error), and print the query count.

It then calls the Java command line tool, and moves the output file to
the location Galaxy is expecting, and removes the tempory XML file.

This script is called from my Galaxy wrapper for Blast2GO for pipelines,
available from the Galaxy Tool Shed here:
http://toolshed.g2.bx.psu.edu/view/peterjc/blast2go

This script is under version control here:
https://github.com/peterjc/galaxy_blast/tree/master/blast2go
"""

from __future__ import print_function

import os
import subprocess
import sys

# You may need to edit this to match your local setup,
blast2go_dir = os.environ.get("B2G4PIPE", "/opt/b2g4pipe_v2.5/")
blast2go_jar = os.path.join(blast2go_dir, "blast2go.jar")


try:
    from massage_xml_for_blast2go import prepare_xml
except ImportError:
    sys.exit("Missing sister file massage_xml_for_blast2go.py")

if len(sys.argv) != 4:
    sys.exit(
        "Require three arguments: XML filename, properties filename, output tabular filename"
    )

xml_file, prop_file, tabular_file = sys.argv[1:]

# We should have write access here:
tmp_xml_file = tabular_file + ".tmp.xml"

if not os.path.isfile(blast2go_jar):
    sys.exit("Blast2GO JAR file not found: %s" % blast2go_jar)

if not os.path.isfile(xml_file):
    sys.exit("Input BLAST XML file not found: %s" % xml_file)

if not os.path.isfile(prop_file):
    tmp = os.path.join(os.path.split(blast2go_jar)[0], prop_file)
    if os.path.isfile(tmp):
        # The properties file seems to have been given relative to the JAR
        prop_file = tmp
    else:
        sys.exit("Blast2GO configuration file not found: %s" % prop_file)
    del tmp


def run(cmd):
    """Run the given command line string via subprocess."""
    # Avoid using shell=True when we call subprocess to ensure if the Python
    # script is killed, so too is the child process.
    try:
        child = subprocess.Popen(
            cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except Exception as err:
        sys.exit("Error invoking command:\n%s\n\n%s\n" % (" ".join(cmd), err))
    stdout, stderr = child.communicate()
    return_code = child.returncode

    # keep stdout minimal as shown prominently in Galaxy
    # Record it in case a silent error needs diagnosis
    if stdout:
        sys.stderr.write("Standard out:\n%s\n\n" % stdout)
    if stderr:
        sys.stderr.write("Standard error:\n%s\n\n" % stderr)

    error_msg = None
    if return_code:
        cmd_str = " ".join(cmd)
        error_msg = "Return code %i from command:\n%s" % (return_code, cmd_str)
    elif "Database or network connection (timeout) error" in stdout + stderr:
        error_msg = "Database or network connection (timeout) error"
    elif "Annotation of 0 seqs with 0 annots finished." in stdout + stderr:
        error_msg = "No sequences processed!"

    if error_msg:
        print(error_msg)
        sys.exit(error_msg)


blast2go_classpath = os.path.split(blast2go_jar)[0]
assert os.path.isdir(blast2go_classpath)
blast2go_classpath = "%s/*:%s/ext/*:" % (blast2go_classpath, blast2go_classpath)

prepare_xml(xml_file, tmp_xml_file)
# print "XML file prepared for Blast2GO"

# We will have write access wherever the output should be,
# so we'll ask Blast2GO to use that as the stem for its output
# (it will append .annot to the filename)
cmd = [
    "java",
    "-cp",
    blast2go_classpath,
    "es.blast2go.prog.B2GAnnotPipe",
    "-in",
    tmp_xml_file,
    "-prop",
    prop_file,
    "-out",
    tabular_file,  # Used as base name for output files
    "-annot",  # Generate *.annot tabular file
    # NOTE: For v2.3.5 must use -a, for v2.5 must use -annot instead
    # "-img", # Generate images, feature not in v2.3.5
]
# print " ".join(cmd)
run(cmd)

# Remove the temp XML file
os.remove(tmp_xml_file)

out_file = tabular_file + ".annot"
if not os.path.isfile(out_file):
    sys.exit("ERROR - No output annotation file from Blast2GO")

# Move the output file where Galaxy expects it to be:
os.rename(out_file, tabular_file)

print("Done")
