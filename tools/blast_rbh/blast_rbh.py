#!/usr/bin/env python
"""BLAST Reciprocal Best Hit (RBH) from two FASTA input files.

Takes the following command line options,
1. FASTA filename of species A
2. FASTA filename of species B
3. Sequence type (prot/nucl)
4. BLAST type (e.g. blastn, or blastp) consistent with sequence type
5. Minimum BLAST Percentage identity
6. Minimum BLAST query coverage
7. Output filename
"""

# TODO - Output more columns, e.g. pident, qcovs, descriptions?

import os
import sys
import tempfile
import shutil

def stop_err( msg ):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)

def run(cmd):
    return_code = os.system(cmd)
    if return_code:
        stop_err("Error %i from: %s" % (return_code, cmd))

if "--version" in sys.argv[1:]:
    #TODO - Capture version of BLAST+ binaries too?
    print "BLAST RBH v0.1.0"
    sys.exit(0)

#Parse Command Line
#TODO - optparse
try:
    fasta_a, fasta_b, dbtype, blast_type, min_identity, min_coverage, out_file = sys.argv[1:]
except:
    stop_err("Expect 7 arguments, got %i" % (len(sys.argv) - 1))

if not os.path.isfile(fasta_a):
    stop_err("Missing input file for species A: %r" % fasta_a)
if not os.path.isfile(fasta_b):
    stop_err("Missing input file for species B: %r" % fasta_b)
if os.path.abspath(fasta_a) == os.path.abspath(fasta_b):
    #TODO - is this ever useful, e.g. positive control?
    stop_err("Asked to compare the FASTA file to itself!")

try:
    min_identity = float(min_identity)
except ValueError:
    stop_err("Expected number between 0 and 100 for minimum identity, not %r" % min_identity)
if not (0 <= min_identity <= 100):
    stop_err("Expected minimum identity between 0 and 100, not %0.2f" % min_identity)
try:
    min_coverage = float(min_coverage)
except ValueError:
    stop_err("Expected number between 0 and 100 for minimum coverage, not %r" % min_coverage)
if not (0 <= min_coverage <= 100):
    stop_err("Expected minimum coverage between 0 and 100, not %0.2f" % min_coverage)


if dbtype == "nucl":
    if blast_type in ["megablast", "blastn", "blastn-short", "dc-megablast"]:
         blast_cmd = "blastn -task %s" % blast_type
    elif blast_type == "tblastx":
        blast_cmd = "tblastx"
    else:
        stop_err("Invalid BLAST type for BLASTN: %r" % blast_type)
elif dbtype == "prot":
    if blast_type not in ["blastp", "blastp-short"]:
        stop_err("Invalid BLAST type for BLASTP: %r" % blast_type)
    blast_cmd = "blastp -task %s" % blast_type
else:
    stop_err("Expected 'nucl' or 'prot' for BLAST database type, not %r" % blast_type)

try:
    threads = int(os.environ.get("GALAXY_SLOTS", "1"))
except:
    threads = 1
assert 1 <= threads, threads

makeblastdb_exe = "makeblastdb"

base_path = tempfile.mkdtemp()
db_a = os.path.join(base_path, "SpeciesA")
db_b = os.path.join(base_path, "SpeciesB")
a_vs_b = os.path.join(base_path, "A_vs_B.tabular")
b_vs_a = os.path.join(base_path, "B_vs_A.tabular")
log = os.path.join(base_path, "blast.log")

cols = "qseqid sseqid bitscore pident qcovhsp" #Or qcovs?
c_query = 0
c_match = 1
c_score = 2
c_identity = 3
c_coverage = 4

#print("Starting...")
#TODO - Report log in case of error?
run('%s -dbtype %s -in "%s" -out "%s" -logfile "%s"' % (makeblastdb_exe, dbtype, fasta_a, db_a, log))
run('%s -dbtype %s -in "%s" -out "%s" -logfile "%s"' % (makeblastdb_exe, dbtype, fasta_b, db_b, log))
#print("BLAST databases prepared.")
run('%s -query "%s" -db "%s" -out "%s" -outfmt "6 %s" -num_threads %i'
    % (blast_cmd, fasta_a, db_b, a_vs_b, cols, threads))
#print("BLAST species A vs species B done.")
run('%s -query "%s" -db "%s" -out "%s" -outfmt "6 %s" -num_threads %i'
    % (blast_cmd, fasta_b, db_a, b_vs_a, cols, threads))
#print("BLAST species B vs species A done.")

best_a_vs_b = dict()
for line in open(a_vs_b):
    if line.startswith("#"): continue
    parts = line.rstrip("\n").split("\t")
    a = parts[c_query]
    b = parts[c_match]
    if float(parts[c_identity]) < min_identity or float(parts[c_coverage]) < min_coverage:
        continue
    score = float(parts[c_score])
    if a not in best_a_vs_b or score > best_a_vs_b[a][1]:
        # Store bitscore as a float for sorting, original string for output
        best_a_vs_b[a] = (b, score, parts[c_score], parts[c_identity], parts[c_coverage])
b_short_list = set(v[0] for v in best_a_vs_b.values())

best_b_vs_a = dict()
for line in open(b_vs_a):
    if line.startswith("#"): continue
    parts = line.rstrip("\n").split("\t")
    b = parts[c_query]
    a = parts[c_match]
    if a not in best_a_vs_b:
        continue
        #stop_err("The A-vs-B file does not have A-ID %r found in B-vs-A file" % a)
    if b not in b_short_list: continue
    if float(parts[c_identity])< min_identity or float(parts[c_coverage]) < min_coverage:
        continue
    score = float(parts[c_score])
    if b not in best_b_vs_a or score > best_b_vs_a[b][1]:
        # Store bitscore as a float for sorting, original string for output
        best_b_vs_a[b] = (a, score, parts[c_score], parts[c_identity], parts[c_coverage])
#TODO - Preserve order from A vs B?
a_short_list = sorted(set(v[0] for v in best_b_vs_a.values()))

count = 0
outfile = open(out_file, 'w')
outfile.write("#A_id\tB_id\tbitscore\tpident\tA qcovhsp\tB qcovhsp\n")
for a in a_short_list:
    a_values = best_a_vs_b[a]
    b = a_values[0]
    b_values = best_b_vs_a[b]
    if b in best_b_vs_a and a == b_values[0]:
        #Output the original string versions of the scores
        values = [a,b]
        #[1] = bitscore as float, [2] = bitscore as original string 
        if a_values[1] < b_values[1]:
            values.append(a_values[2])
        else:
            values.append(b_values[2])
        #[3] = identity as string
        if float(a_values[3]) < float(b_values[3]):
            values.append(a_values[3])
        else:
            values.append(b_values[3])
        #[4] = coverage
        values.append(a_values[4])
        values.append(b_values[4])
        outfile.write("%s\t%s\t%s\t%s\t%s\t%s\n" % tuple(values))
        count += 1
outfile.close()
print "Done, %i RBH found" % count

#Remove temp files...
shutil.rmtree(base_path)
