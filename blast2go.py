#!/usr/bin/env python
"""Galaxy wrapper for Blast2GO for pipelines, b2g4pipe v2.3.5.

This script takes exactly three command line arguments:
 * Input BLAST XML filename
 * Blast2GO properties filename (settings file)
 * Output tabular filename

It then calls the Java command line tool, and moves the output file to
the location Galaxy is expecting.
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

if not os.path.isfile(xml_file):
   stop_err("Input BLAST XML file not found: %s" % xml_file)

if not os.path.isfile(prop_file):
   stop_err("Blast2GO configuration file not found: %s" % prop_file)

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
        if stderr and stdout:
            stop_err("Return code %i from command:\n%s\n\n%s\n\n%s" % (return_code, err, stdout, stderr))
        else:
            stop_err("Return code %i from command:\n%s\n%s" % (return_code, err, stderr))
    #For early diagnostics,
    else:
       print stdout
       print stderr

if not os.path.isfile(blast2go_jar):
   stop_err("Blast2GO JAR file not found: %s" % blast2go_jar)

#We will have write access whereever the output should be,
#so we'll ask Blast2GO to use that as the stem for its output
#(it will append .annot to the filename)
cmd = ["java", "-jar", blast2go_jar,
       "-in", xml_file,
       "-prop", prop_file,
       "-out", tabular_file, #Used as base name for output files
       "-a", # Generate *.annot tabular file
       "-img", # Generate images
       ]
print " ".join(cmd)
run(cmd)

out_file = tabular_file + ".annot"
if not os.path.isfile(out_file):
   stop_err("ERROR - No output annotation file from Blast2GO")

#Move the output file where Galaxy expects it to be:
os.rename(out_file, tabular_file)

print "Done"
