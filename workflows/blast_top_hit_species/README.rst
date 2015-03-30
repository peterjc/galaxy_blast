Introduction
============

Galaxy is a web-based platform for biological data analysis, supporting
extension with additional tools (often wrappers for existing command line
tools) and datatypes. See http://www.galaxyproject.org/ and the public
server at http://usegalaxy.org for an example.

The NCBI BLAST suite is a widely used set of tools for biological sequence
comparison. It is available as standalone binaries for use at the command
line, and via the NCBI website for smaller searches. For more details see
http://blast.ncbi.nlm.nih.gov/Blast.cgi

This is an example workflow using the Galaxy wrappers for NCBI BLAST+,
see https://github.com/peterjc/galaxy_blast

Galaxy workflow for counting species of top BLAST hits 
======================================================

This Galaxy workflow (file ``blast_top_hit_species.ga``) is intended for an
initial assessment of a transcriptome assembly to give a crude indication of
any major contaimination present based on the species of the top BLAST hit
of 1000 representative sequences.

.. image:: https://raw.githubusercontent.com/peterjc/galaxy_blast/master/workflows/blast_top_hit_species/blast_top_hit_species.png

In words, the workflow proceeds as follows:

1. Upload/import your transcriptome assembly or any nucleotide FASTA file.
2. Samples 1000 representative sequences, selected uniformly/evenly though
   the file.
3. Convert the sampled FASTA file into a three column tabular file.
4. Runs NCBI BLASTX of the sampled FASTA file against the latest NCBI ``nr``
   database (assuming this is already available setup on your local Galaxy
   under the alias ``nr``), requesting tabular output including the taxonomy
   fields, and at most one matching target sequence.
5. Remove any duplicate alignments (multiple HSPs for the same match).
6. Combine the filtered BLAST output with the tabular version of the 1000
   sequences to give a new tabular file with exactly 1000 lines, adding
   ``None`` for sequences missing a BLAST hit.
7. Count the BLAST species names in this file.
8. Sort the counts.

Finally we would suggest visualising the sorted tally table as a Pie Chart.


Sample Data
===========

As an example, you can upload the transcriptome assembly of the nematode
*Nacobbus abberans* from Eves van den Akker *et al.* (2015),
http://dx.doi.org/10.1093/gbe/evu171 using this URL:

http://nematode.net/Data/nacobbus_aberrans_transcript_assembly/N.abberans_reference_no_contam.zip

Running this workflow with a copy of the NCBI non-redundant ``nr`` database
from 16 Oct 2014 (which did **not** contain this *N. abberans* dataset) gave
the following results - note 609 out of the 1000 sequences gave no BLAST hit.

| Count | Subject Blast Name |
| ----- | ------------------ |
|   609 | None               |
|   244 | nematodes          |
|    30 | ascomycetes        |
|    27 | eukaryotes         |
|     8 | basidiomycetes     |
|     6 | aphids             |
|     5 | eudicots           |
|     5 | flies              |
|   ... | ...                |

As you might guess from	the filename ``N.abberans_reference_no_contam.fasta``,
this transcriptome assembly has already had obvious contamination removed.

At the time of writing, Galaxy's visualizations could not be included in
a workflow. You can generate a pie chart from the final count file using
the counts (c1) and labels (c2), like this:

.. image:: https://raw.githubusercontent.com/peterjc/galaxy_blast/master/workflows/blast_top_hit_species/N_abberans_piechart_mouseover.png

Note the nematode count in this image was shown as a mouse-over effect.

