#!/usr/bin/env python
"""BLAST Reciprocal Best Hit (RBH) from two BLAST tabular files.

Run "blast_rbh_report.py -h" to see the help text.  Also, look at
blast_rbh.xml and README.rst files which are available on GitHub at:
https://github.com/peterjc/galaxy_blast/tree/master/tools/blast_rbh

This requires Python to be installed and on the $PATH.

You can also run this tool via Galaxy using the "blast_rbh.xml"
definition file. This is available as a package on the Galaxy
Tool Shed: http://toolshed.g2.bx.psu.edu/view/peterjc/blast_rbh
"""

# TODO - Output more columns, e.g. pident, qcovs, descriptions?
# TODO - Use new -qcov_hsp_perc option in BLAST+ 2.2.30 to filter
#        results, rather than doing minimum HSP coverage in Python.
#        [Not doing this right now as would break on older BLAST+]

from __future__ import print_function

import os
import sys
import best_hits


from optparse import OptionParser


def main():
    """Tool entry point defining command line API."""
    if "--version" in sys.argv[1:]:
        # TODO - Capture version of BLAST+ binaries too?
        print("BLAST RBH v0.1.11")
        sys.exit(0)

    # Parse Command Line
    usage = """Use as follows:

    $ python blast_rbh_report.py [options] A.tabular B.tabular

    $ python blast_rbh_report.py -o output.tsv A.tabular B.tabular

    Use the outfmt arg when you run BLAST:
       -outfmt "6 qseqid sseqid bitscore pident qcovhsp qlen length"

    There is additional guidance in the help text in the blast_rbh.xml file,
    which is shown to the user via the Galaxy interface to this tool.
    """

    parser = OptionParser(usage=usage)
    parser.add_option(
        "-i",
        "--identity",
        dest="min_identity",
        default="70",
        help="Minimum percentage identity (optional, default 70)",
    )
    parser.add_option(
        "-c",
        "--coverage",
        dest="min_coverage",
        default="50",
        help="Minimum HSP coverage (optional, default 50)",
    )
    parser.add_option(
        "-o",
        "--output",
        dest="output",
        default=None,
        metavar="FILE",
        help="Output filename (required)",
    )
    options, args = parser.parse_args()

    if len(args) != 2:
        sys.exit("Expects two input tabular BLAST filenames")
    a_vs_b, b_vs_a = args
    if not os.path.isfile(a_vs_b):
        sys.exit("Missing input file for species A: %r" % a_vs_b)
    if not os.path.isfile(b_vs_a):
        sys.exit("Missing input file for species B: %r" % b_vs_a)

    if os.path.abspath(a_vs_b) == os.path.abspath(b_vs_a):
        self_comparison = True
    else:
        self_comparison = False

    if not options.output:
        sys.exit("Output filename required, e.g. -o example.tab")
    out_file = options.output

    try:
        min_identity = float(options.min_identity)
    except ValueError:
        sys.exit(
            "Expected number between 0 and 100 for minimum identity, not %r"
            % min_identity
        )
    if not (0 <= min_identity <= 100):
        sys.exit(
            "Expected minimum identity between 0 and 100, not %0.2f" % min_identity
        )
    try:
        min_coverage = float(options.min_coverage)
    except ValueError:
        sys.exit(
            "Expected number between 0 and 100 for minimum coverage, not %r"
            % min_coverage
        )
    if not (0 <= min_coverage <= 100):
        sys.exit(
            "Expected minimum coverage between 0 and 100, not %0.2f" % min_coverage
        )

    best_b_vs_a = dict(
        best_hits.best_hits(b_vs_a, min_identity, min_coverage, self_comparison)
    )

    count = 0
    with open(out_file, "w") as outfile:
        outfile.write(
            "#A_id\tB_id\tA_length\tB_length\tA_qcovhsp\tB_qcovhsp\t"
            "length\tpident\tbitscore\n"
        )
        for (
            a,
            (
                b,
                a_score_float,
                a_score_str,
                a_identity_str,
                a_coverage_str,
                a_qlen,
                a_length,
            ),
        ) in best_hits.best_hits(a_vs_b, min_identity, min_coverage, self_comparison):
            if b not in best_b_vs_a:
                # Match b has no best hit
                continue
            (
                a2,
                b_score_float,
                b_score_str,
                b_identity_str,
                b_coverage_str,
                b_qlen,
                b_length,
            ) = best_b_vs_a[b]
            if a != a2:
                # Not an RBH
                continue
            # Start with IDs, lengths, coverage
            values = [a, b, a_qlen, b_qlen, a_coverage_str, b_coverage_str]
            # Alignment length was an integer so don't care about original string
            values.append(min(a_length, b_length))
            # Output the original string versions of the scores
            if float(a_identity_str) < float(b_identity_str):
                values.append(a_identity_str)
            else:
                values.append(b_identity_str)
            if a_score_float < b_score_float:
                values.append(a_score_str)
            else:
                values.append(b_score_str)
            outfile.write("%s\t%s\t%i\t%i\t%s\t%s\t%i\t%s\t%s\n" % tuple(values))
            count += 1
    print("Done, %i RBH found" % count)
    if best_hits.tie_warning:
        sys.stderr.write(
            "Warning: Sequences with tied best hits found, "
            "you may have duplicates/clusters\n"
        )


if __name__ == "__main__":
    main()
