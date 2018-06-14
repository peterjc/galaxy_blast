#!/usr/bin/env python
"""BLAST Heterozygosity plot (RBH) from one or more FASTA input files.

Run "blast_heterozygosity_plot.py -h" to see the help text, or read
the associated blast_heterozygosity_plot.xml and README.rst files
which are available on GitHub at:

https://github.com/peterjc/galaxy_blast/tree/master/tools/blast_heterozygosity_plot.py

This requires Python and the NCBI BLAST+ tools to be installed
and on the $PATH.

You can also run this via Galaxy using "blast_heterozygosity_plot.xml"
which is available as a package on the Galaxy Tool Shed:

http://toolshed.g2.bx.psu.edu/view/peterjc/blast_heterozygosity_plot
"""

# TODO - Multiple text output files?
# TODO - Graphical options, histogram vs density?

from __future__ import print_function

import os
import platform
import shutil
import sys
import tempfile

from optparse import OptionParser


# Ordered dict is a language feature from Python 3.7 onwards.
# CPython 3.6 also already has ordered dicts.
# PyPy has always had ordered dicts.
if (sys.version_info >= (3, 7)
        or platform.python_implementation() == "PyPy"
        or (sys.version_info == (3, 6)
            and platform.python_implementation() == "CPython")):
    ordered_dict = dict
else:
    from collections import OrderedDict as ordered_dict


try:
    import matplotlib
    # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.style.context('ggplot')
except ImportError:
    sys.exit("ERROR: Python is missing matplotlib")


try:
    import numpy as np
except ImportError:
    sys.exit("ERROR: Python is missing numpy")


def run(cmd):
    return_code = os.system(cmd)
    if return_code:
        sys.exit("Error %i from: %s" % (return_code, cmd))


if "--version" in sys.argv[1:]:
    # TODO - Capture version of BLAST+ binaries too?
    print("BLAST Heterozygosity Plot v0.0.1")
    sys.exit(0)

try:
    threads = int(os.environ.get("GALAXY_SLOTS", "1"))
except ValueError:
    threads = 1
assert 1 <= threads, threads

# Parse Command Line
usage = """Use as follows:

$ python blast_heterozygosity_plot.py [options] A.fasta [more FASTA file names]

Many of the options are required. Example with three assembly's gene files:

$ python blast_heterozygosity_plot.py -a nucl -t blastn -o output.pdf \\
                              genes_A.fasta genes_B.fasta genes_C.fasta

For each FASTA input file, a temporary BLAST database is built and used
to run a search of the genes against themselves. By default a minimum HSP
coverage of 50% is applied using the BLAST+ command line argument
-qcov_hsp_perc. The BLAST results are filtered to exclude self-matches
and look at the second best hit, recording the percentage identity
relative to the query sequence length.

Then a histogram is drawn using the 2nd best hit's percentage identifies
for each of the input FASTA files (this does not start at zero, the
minimum depends on the worst second best hit that BLAST reports).

There is additional guidance in the help text in the associated XML file,
blast_heterozygosity_plot.xml, which is shown to the user via the Galaxy
interface to this tool.
"""

parser = OptionParser(usage=usage)
parser.add_option("-a", "--alphabet", dest="dbtype",
                  default=None,
                  help="Alphabet type (nucl or prot; required)")
parser.add_option("-t", "--task", dest="task",
                  default=None,
                  help="BLAST task (e.g. blastp, blastn, megablast; required)")
parser.add_option("-c", "--coverage", dest="min_coverage",
                  default="50",
                  help="Minimum HSP query coverage (optional, default 50)")
parser.add_option("-o", "--output", dest="output",
                  default=None, metavar="FILE",
                  help="Output PDF filename (required)")
parser.add_option("--threads", dest="threads",
                  default=threads,
                  help="Number of threads when running BLAST. Defaults to the "
                       "$GALAXY_SLOTS environment variable if set, or 1.")
options, args = parser.parse_args()

if len(args) < 1:
    sys.exit("Expects at least one input FASTA filename")
for fasta in args:
    if not os.path.isfile(fasta):
        sys.exit("Missing specified input file: %r" % fasta)

if not options.output:
    sys.exit("Output filename required, e.g. -o heterozygosity.pdf")
out_file = options.output

try:
    min_coverage = float(options.min_coverage)
except ValueError:
    sys.exit("Expected number between 0 and 100 for minimum coverage, not %r" % min_coverage)
if not (0 <= min_coverage <= 100):
    sys.exit("Expected minimum coverage between 0 and 100, not %0.2f" % min_coverage)

if not options.task:
    sys.exit("Missing BLAST task, e.g. -t blastp")
blast_type = options.task

if not options.dbtype:
    sys.exit("Missing database type, -a nucl, or -a prot")
dbtype = options.dbtype
if dbtype == "nucl":
    if blast_type in ["megablast", "blastn", "blastn-short", "dc-megablast"]:
        blast_cmd = "blastn -task %s" % blast_type
    elif blast_type == "tblastx":
        blast_cmd = "tblastx"
    else:
        sys.exit("Invalid BLAST type for BLASTN: %r" % blast_type)
elif dbtype == "prot":
    if blast_type not in ["blastp", "blastp-fast", "blastp-short"]:
        sys.exit("Invalid BLAST type for BLASTP: %r" % blast_type)
    blast_cmd = "blastp -task %s" % blast_type
else:
    sys.exit("Expected 'nucl' or 'prot' for BLAST database type, not %r" % blast_type)

try:
    threads = int(options.threads)
except ValueError:
    sys.exit("Expected positive integer for number of threads, not %r" % options.threads)
if threads < 1:
    sys.exit("Expected positive integer for number of threads, not %r" % threads)

makeblastdb_exe = "makeblastdb"

#base_path = tempfile.mkdtemp()
base_path = "."
log = os.path.join(base_path, "blast.log")

cols = "qseqid sseqid bitscore pident qcovhsp qlen length nident"  # Or qcovs?
c_query = 0
c_match = 1
c_score = 2
c_identity = 3
c_coverage = 4
c_qlen = 5
c_length = 6
c_nident = 7

def generate_histogram(fasta, hits, histo, min_cover):
    col_count = len(cols.split())
    answer = ordered_dict()
    # Pre-fill the dictionary with 0% identify for all sequences
    # to ensure we have value for every query - some might not
    # have any second best hits (or in extreme cases, no hits
    # at all if fail BLAST's internal complexity filters etc).
    with open(fasta) as handle:
        for line in handle:
            if line.startswith(">"):
                a = line[1:].rstrip("\n").split(None, 1)[0]
                answer[a] = 0
    with open(hits) as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) != col_count:
                # Using NCBI BLAST+ 2.2.27 any undefined field is ignored
                # Even NCBI BLAST+ 2.5.0 silently ignores unknown fields :(
                sys.exit("Old version of NCBI BLAST? Expected %i columns, got %i:\n%s\n"
                         "Note the qcovhsp field was only added in version 2.2.28\n"
                         % (col_count, len(parts), line))
            if float(parts[c_coverage]) < min_coverage:
                sys.stderr.write("WARNING: Check -qcov_hsp_perc worked?: %r\n" % line)
                continue
            a = parts[c_query]
            b = parts[c_match]
            if a == b:
                continue
            # BLAST's pident is number of identites relative to alignment length
            percent_identity = int(parts[c_nident]) * 100.0 / int(parts[c_qlen])
            answer[a] = max(answer[a], percent_identity)
    with open(histo, "w") as handle:
        handle.write("#Identifier\tSecond-best-hit-identity\n")
        for a, v in answer.items():
            handle.write("%s\t%0.1f\n" % (a, v))
    return sorted(answer.values())


def plot_histograms(dict_of_values, pdf_filename):
    bins = np.arange(101, dtype=int) # 0 to 100 inclusive
    figure = plt.figure()
    for fasta, values in dict_of_values.items():
        print("%s has percentage identities from %0.1f to %0.1f for second best hit"
              % (fasta, min(values), max(values)))
        counts = np.zeros(101, int)
        for v in values:
            assert 0 <= v <= 100
            counts[int(v)] += 1
        # print(counts)
        counts[0] = 0  # Ignore zero percentage identical for the plot
        plt.plot(bins, counts, label=fasta)

    plt.xlim([0, 100])
    #plt.ylim([0, 10])

    # Set the title and labels
    plt.title('BLAST Heterozygosity Plot')
    plt.xlabel('Percentage identity of second best self-BLAST hit')
    plt.ylabel('Count')
    plt.legend(loc='upper left')

    plt.show()
    figure.savefig(pdf_filename, bbox_inches='tight')


sys.stderr.write("Generating %i BLAST databases\n" % len(args))
for i, fasta in enumerate(args):
    # TODO - Report log in case of error?
    db = os.path.join(base_path, "db_%s" % i)
    # For testing during development, skip re-generation
    if not os.path.isfile(db + ".nin") and not os.path.isfile(db + ".pin"):
        run('%s -dbtype %s -in "%s" -out "%s" -logfile "%s"'
            % (makeblastdb_exe, dbtype, fasta, db, log))

sys.stderr.write("Running self BLAST searches\n")
for i, fasta in enumerate(args):
    db = os.path.join(base_path, "db_%s" % i)
    hits = os.path.join(base_path, "hits_%s_vs_self.tsv" % i)
    # For testing during development, skip re-generation
    if not os.path.isfile(hits):
        run('%s -query "%s" -db "%s" -out "%s" -outfmt "6 %s" -num_threads %i -num_alignments 2 -qcov_hsp_perc %s'
            % (blast_cmd, fasta, db, hits, cols, threads, options.min_coverage))

sys.stderr.write("Computing histogram data\n")
values = ordered_dict()
for i, fasta in enumerate(args):
    hits = os.path.join(base_path, "hits_%s_vs_self.tsv" % i)
    histo = os.path.join(base_path, "histogram_%s.tsv" % i)
    # For testing during development, skip re-generation 
    if not os.path.isfile(histo):
        values[fasta] = generate_histogram(fasta, hits, histo, min_coverage)
    else:
        values[fasta] = [float(line.rstrip("\n").split("\t")[1]) for line in open(histo) if not line.startswith("#")]

sys.stderr.write("Producing plot\n")
plot_histograms(values, options.output)

sys.stderr.write("Done, plot of %i histograms produced\n" % len(args))

# Remove temp files...
if base_path != ".":
    shutil.rmtree(base_path)
