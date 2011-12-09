#!/usr/bin/env python
"""Reciprocal Best Hit (RBH) using BLAST style tabular input

Takes seven command line options,
1. Tabular filename of A against B
2. Tabular filename of B against A
3. Query ID column number (assumed to be same for both input files), e.g. c1
4. Match ID column number (assumed to be same for both input files), e.g. c2
5. Score column number (assumed to be same for both input files), e.g. c12
6. Want higest or lowest score? (use string high or low)
7. Output filename

"""
import sys
if "--version" in sys.argv[1:]:
    print "RBH v0.0.2"
    sys.exit(0)

def stop_err( msg ):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)

#Parse Command Line
try:
    a_vs_b, b_vs_a, c_query, c_match, c_score, sort_order, out_file = sys.argv[1:]
except:
    stop_err("Expect 7 arguments: two input files, column settings, output file")


want_highest = want_lowest = False
if sort_order == "high":
    want_highest = True
elif sort_order == "low":
    want_lowest = True
else:
    stop_err("Sort order argument should be high or low")

if out_file in [a_vs_b, b_vs_a]:
    stop_err("Output file would overwrite an input file")

def get_col_index(col_str):
    if col_str[0]=="c":
        col_str = col_str[1:]
    return int(col_str)-1

c_query = get_col_index(c_query)
c_match = get_col_index(c_match)
c_score = get_col_index(c_score)
if len(set([c_query, c_match, c_score])) < 3:
    stop_err("Need three different column numbers!")

"""
def load_best(filename, id1col, id2col):
    best = dict()
    for line in open(a_vs_b):
        if line.startswith("#"): continue
        parts = line.rstrip("\n").split("\t")
        id1 = parts[id1col]
        id2 = parts[id2col]
        score = float(parts[c_score])
        if (a not in best_a_vs_b) \
        or (want_highest and score > best[id1][1]) \
        or (want_lowest and score < best[id1][1]):
            best[id1] = (id2, score)
    return best
best_a_vs_b = load_best(a_vs_b, c_query, c_match)
"""

best_a_vs_b = dict()
for line in open(a_vs_b):
    if line.startswith("#"): continue
    parts = line.rstrip("\n").split("\t")
    a = parts[c_query]
    b = parts[c_match]
    score = float(parts[c_score])
    if (a not in best_a_vs_b) \
    or (want_highest and score > best_a_vs_b[a][1]) \
    or (want_lowest and score < best_a_vs_b[a][1]):
        best_a_vs_b[a] = (b, score, parts[c_score])
b_short_list = set(b for (b,score, score_str) in best_a_vs_b.values())

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
    score = float(parts[c_score])
    if (b not in best_b_vs_a) \
    or (want_highest and score > best_b_vs_a[b][1]) \
    or (want_lowest and score < best_b_vs_a[b][1]):
        best_b_vs_a[b] = (a, score, parts[c_score])
#TODO - Preserve order from A vs B?
a_short_list = sorted(set(a for (a,score,score_str) in best_b_vs_a.values()))

count = 0
outfile = open(out_file, 'w')
outfile.write("#A_id\tB_id\tA_vs_B\tB_vs_A\n")
for a in a_short_list:
    b = best_a_vs_b[a][0]
    if b in best_b_vs_a and a == best_b_vs_a[b][0]:
        outfile.write("%s\t%s\t%s\t%s\n" % (a, b, best_a_vs_b[a][2], best_b_vs_a[b][2]))
        count += 1
outfile.close()
print "Done, %i RBH found" % count
