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
from optparse import OptionParser

def stop_err( msg ):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)

def run(cmd):
    return_code = os.system(cmd)
    if return_code:
        stop_err("Error %i from: %s" % (return_code, cmd))

if "--version" in sys.argv[1:]:
    #TODO - Capture version of BLAST+ binaries too?
    print "BLAST RBH v0.1.3"
    sys.exit(0)

#Parse Command Line
usage = """Use as follows:

$ python blast_rbh.py [options] A.fasta B.fasta
"""

parser = OptionParser(usage=usage)
parser.add_option("-a", "--alphabet", dest="dbtype",
                  default=None,
                  help="Alphabet type (nucl or prot)")
parser.add_option("-t", "--task", dest="task",
                  default=None,
                  help="BLAST task (e.g. blastp, blastn, megablast)")
parser.add_option("-i","--identity", dest="min_identity",
                  default="70",
                  help="Minimum percentage identity (optional, default 70)")
parser.add_option("-c", "--coverage", dest="min_coverage",
                  default="50",
                  help="Minimum HSP coverage (optional, default 50)")
parser.add_option("--nr", dest="nr", default=False, action="store_true",
                  help="Preprocess FASTA files to collapse identifical "
                  "entries (make sequences non-redundant)")
parser.add_option("-o", "--output", dest="output",
                  default=None, metavar="FILE",
                  help="Output filename")
options, args = parser.parse_args()

if len(args) != 2:
    stop_err("Expects two input FASTA filenames")
fasta_a, fasta_b = args
if not os.path.isfile(fasta_a):
    stop_err("Missing input file for species A: %r" % fasta_a)
if not os.path.isfile(fasta_b):
    stop_err("Missing input file for species B: %r" % fasta_b)
if os.path.abspath(fasta_a) == os.path.abspath(fasta_b):
    self_comparison = True
    print("Doing self comparison; ignoring self matches.")
else:
    self_comparison = False

if not options.output:
    stop_err("Output filename required, e.g. -o example.tab")
out_file = options.output

try:
    min_identity = float(options.min_identity)
except ValueError:
    stop_err("Expected number between 0 and 100 for minimum identity, not %r" % min_identity)
if not (0 <= min_identity <= 100):
    stop_err("Expected minimum identity between 0 and 100, not %0.2f" % min_identity)
try:
    min_coverage = float(options.min_coverage)
except ValueError:
    stop_err("Expected number between 0 and 100 for minimum coverage, not %r" % min_coverage)
if not (0 <= min_coverage <= 100):
    stop_err("Expected minimum coverage between 0 and 100, not %0.2f" % min_coverage)

if not options.task:
    stop_err("Missing BLAST task, e.g. -t blastp")
blast_type = options.task

if not options.dbtype:
    stop_err("Missing database type, -a nucl, or -a prot")
dbtype = options.dbtype
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
tmp_a = os.path.join(base_path, "SpeciesA.fasta")
db_a = os.path.join(base_path, "SpeciesA")
a_vs_b = os.path.join(base_path, "A_vs_B.tabular")
if self_comparison:
    tmp_b = tmp_a
    db_b = db_a
    b_vs_a = a_vs_b
else:
    tmp_b = os.path.join(base_path, "SpeciesB.fasta")
    db_b = os.path.join(base_path, "SpeciesB")
    b_vs_a = os.path.join(base_path, "B_vs_A.tabular")
log = os.path.join(base_path, "blast.log")

cols = "qseqid sseqid bitscore pident qcovhsp qlen length" #Or qcovs?
c_query = 0
c_match = 1
c_score = 2
c_identity = 3
c_coverage = 4
c_qlen = 5
c_length = 6

tie_warning = 0

def best_hits(blast_tabular, ignore_self=False):
    """Iterate over BLAST tabular output, returns best hits as 2-tuples.

    Each return value is (query name, tuple of value for the best hit).

    Tied best hits to different sequences are NOT returned.

    One hit is returned for tied best hits to the same sequence
    (e.g. repeated domains).
    """
    global tie_warning
    current = None
    best_score = None
    best = None
    with open(blast_tabular) as h:
        for line in h:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if float(parts[c_identity]) < min_identity or float(parts[c_coverage]) < min_coverage:
                continue
            a = parts[c_query]
            b = parts[c_match]
            if ignore_self and a == b:
                continue
            score = float(parts[c_score])
            qlen = int(parts[c_qlen])
            length = int(parts[c_length])
            #print("Considering hit for %s to %s with score %s..." % (a, b, score))
            if current is None:
                #First hit
                assert best is None
                assert best_score is None
                best = dict()
                #Now append this hit...
            elif a != current:
                #New hit
                if len(best) == 1:
                    #Unambiguous (no tied matches)
                    yield current, list(best.values())[0]
                else:
                    #print("%s has %i equally good hits: %s" % (a, len(best), ", ".join(best)))
                    tie_warning += 1
                best = dict()
                #Now append this hit...
            elif score < best_score:
                #print("No improvement for %s, %s < %s" % (a, score, best_score))
                continue
            elif score > best_score:
                #This is better, discard old best
                best = dict()
                #Now append this hit...
            else:
                #print("Tied best hits for %s" % a)
                assert best_score == score
                #Now append this hit...
            current = a
            best_score = score
            #This will collapse two equally good hits to the same target (e.g. duplicated domain)
            best[b] = (b, score, parts[c_score], parts[c_identity], parts[c_coverage], qlen, length)
    #Best hit for final query, if unambiguous:
    if current is not None:
        if len(best)==1:
            yield current, list(best.values())[0]
        else:
            #print("%s has %i equally good hits: %s" % (a, len(best), ", ".join(best)))
            tie_warning += 1

def make_nr(input_fasta, output_fasta, sep=";"):
    #TODO - seq-hash based to avoid loading everything into RAM?
    by_seq = dict()
    from Bio import SeqIO
    for record in SeqIO.parse(input_fasta, "fasta"):
        s = str(record.seq).upper()
        try:
            by_seq[s].append(record.id)
        except KeyError:
            by_seq[s] = [record.id]
    unique = 0
    representatives = dict()
    duplicates = set()
    for cluster in by_seq.values():
        if len(cluster) > 1:
            representatives[cluster[0]] = cluster
            duplicates.update(cluster[1:])
        else:
            unique += 1
    del by_seq
    if duplicates:
        #TODO - refactor as a generator with single SeqIO.write(...) call
        with open(output_fasta, "w") as handle:
            for record in SeqIO.parse(input_fasta, "fasta"):
                if record.id in representatives:
                    cluster = representatives[record.id]
                    record.id = sep.join(cluster)
                    record.description = "representing %i records" % len(cluster)
                elif record.id in duplicates:
                    continue
                SeqIO.write(record, handle, "fasta")
        print("%i unique entries; removed %i duplicates leaving %i representative records" % (unique, len(duplicates), len(representatives)))
    else:
        os.symlink(os.path.abspath(input_fasta), output_fasta)
        print("No perfect duplicates in file, %i unique entries" % unique)

#print("Starting...")
if options.nr:
    make_nr(fasta_a, tmp_a)
    if not self_comparison:
        make_nr(fasta_b, tmp_b)
    fasta_a = tmp_a
    fasta_b = tmp_b

#TODO - Report log in case of error?
run('%s -dbtype %s -in "%s" -out "%s" -logfile "%s"' % (makeblastdb_exe, dbtype, fasta_a, db_a, log))
if not self_comparison:
    run('%s -dbtype %s -in "%s" -out "%s" -logfile "%s"' % (makeblastdb_exe, dbtype, fasta_b, db_b, log))
#print("BLAST databases prepared.")
run('%s -query "%s" -db "%s" -out "%s" -outfmt "6 %s" -num_threads %i'
    % (blast_cmd, fasta_a, db_b, a_vs_b, cols, threads))
#print("BLAST species A vs species B done.")
if not self_comparison:
    run('%s -query "%s" -db "%s" -out "%s" -outfmt "6 %s" -num_threads %i'
        % (blast_cmd, fasta_b, db_a, b_vs_a, cols, threads))
    #print("BLAST species B vs species A done.")


best_b_vs_a = dict(best_hits(b_vs_a, self_comparison))


count = 0
outfile = open(out_file, 'w')
outfile.write("#A_id\tB_id\tA_length\tB_length\tA_qcovhsp\tB_qcovhsp\tlength\tpident\tbitscore\n")
for a, (b, a_score_float, a_score_str, a_identity_str, a_coverage_str, a_qlen, a_length) in best_hits(a_vs_b, self_comparison):
    if b not in best_b_vs_a:
        #Match b has no best hit
        continue
    a2, b_score_float, b_score_str, b_identity_str, b_coverage_str, b_qlen, b_length = best_b_vs_a[b]
    if a != a2:
        #Not an RBH
        continue
    #Start with IDs, lengths, coverage
    values = [a, b, a_qlen, b_qlen, a_coverage_str, b_coverage_str]
    #Alignment length was an integer so don't care about original string
    values.append(min(a_length, b_length))
    #Output the original string versions of the scores
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
outfile.close()
print "Done, %i RBH found" % count
if tie_warning:
    sys.stderr.write("Warning: Sequencies with tied best hits found, you may have duplicates/clusters\n")

#Remove temp files...
shutil.rmtree(base_path)
