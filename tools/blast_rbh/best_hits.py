#!/usr/bin/env python
"""BLAST Reciprocal Best Hit (RBH) from two BLAST tabular files.
   This is calculated by the best_hits method below.

   The method expects the blast_tabular parameter to be a file
   that contains BLAST tabular output with these columns:
     "qseqid sseqid bitscore pident qcovhsp qlen length"

   The method iterate over the BLAST tabular output, returns best hits as 2-tuples.
   Each return value is (query name, tuple of value for the best hit).

   Tied best hits to different sequences are NOT returned.

   One hit is returned for tied best hits to the same sequence
   (e.g. repeated domains).

   The code in this module originated from blast_rbh.py in
   https://github.com/peterjc/galaxy_blast/tree/master/tools/blast_rbh

   Please cite the author per instructions in
   https://github.com/peterjc/galaxy_blast/blob/master/tools/blast_rbh/README.rst
"""

import sys

tie_warning=0

c_query = 0
c_match = 1
c_score = 2
c_identity = 3
c_coverage = 4
c_qlen = 5
c_length = 6

cols = "qseqid sseqid bitscore pident qcovhsp qlen length"

def best_hits(blast_tabular, min_identity=70, min_coverage=50, ignore_self=False):
    global tie_warning
    current = None
    best_score = None
    best = None
    col_count = len(cols.split())
    with open(blast_tabular) as h:
        for line in h:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) != col_count:
                # Using NCBI BLAST+ 2.2.27 the undefined field is ignored
                # Even NCBI BLAST+ 2.5.0 silently ignores unknown fields :(
                sys.exit(
                    "Old version of NCBI BLAST? Expected %i columns, got %i:\n%s\n"
                    "Note the qcovhsp field was only added in version 2.2.28\n"
                    % (col_count, len(parts), line)
                )
            if (
                float(parts[c_identity]) < min_identity
                or float(parts[c_coverage]) < min_coverage
            ):
                continue
            a = parts[c_query]
            b = parts[c_match]
            if ignore_self and a == b:
                continue
            score = float(parts[c_score])
            qlen = int(parts[c_qlen])
            length = int(parts[c_length])
            # print("Considering hit for %s to %s with score %s..." % (a, b, score))
            if current is None:
                # First hit
                assert best is None
                assert best_score is None
                best = dict()
                # Now append this hit...
            elif a != current:
                # New hit
                if len(best) == 1:
                    # Unambiguous (no tied matches)
                    yield current, list(best.values())[0]
                else:
                    # print("%s has %i equally good hits: %s"
                    #       % (a, len(best), ", ".join(best)))
                    tie_warning += 1
                best = dict()
                # Now append this hit...
            elif score < best_score:
                # print("No improvement for %s, %s < %s" % (a, score, best_score))
                continue
            elif score > best_score:
                # This is better, discard old best
                best = dict()
                # Now append this hit...
            else:
                # print("Tied best hits for %s" % a)
                assert best_score == score
                # Now append this hit...
            current = a
            best_score = score
            # This will collapse two equally good hits
            # to the same target (e.g. duplicated domain)
            best[b] = (
                b,
                score,
                parts[c_score],
                parts[c_identity],
                parts[c_coverage],
                qlen,
                length,
            )
    # Best hit for final query, if unambiguous:
    if current is not None:
        if len(best) == 1:
            yield current, list(best.values())[0]
        else:
            # print("%s has %i equally good hits: %s"
            # % (a, len(best), ", ".join(best)))
            tie_warning += 1

