Galaxy tool to find BLAST Reciprocal Best Hits (RBH)
====================================================

This tool is copyright 2011-2014 by Peter Cock, The James Hutton Institute
(formerly SCRI, Scottish Crop Research Institute), UK. All rights reserved.
See the licence text below.

This tool is a short Python script to run reciprocal BLAST searches on a
pair of sequence files, and extract the reciprocal best hits.

This is a work in progress, and builds on an earlier implementation which
prequired the two BLAST searches be prepared in advance. Integration allows
a much simpler user experience, and can ensure sensible filters are used.


Automated Installation
======================

Installation via the Galaxy Tool Shed should take care of the Galaxy side of
things, including the dependency the NCBI BLAST+ binaries.


Manual Installation
===================

There are just two files to install:

- ``blast_rbh.py`` (the Python script)
- ``blast_rbh.xml`` (the Galaxy tool definition)

The suggested location is in a ``tools/blast_rbh/`` folder. You will then
need to modify the ``tools_conf.xml`` file to tell Galaxy to offer the tool
by adding the line::

    <tool file="blast_rbh/blast_rbh.xml" />

If you want to run the functional tests, include the same line in your
``tool_conf.xml.sample`` file, and the sample test files under Galaxy's
``test-data/`` directory. Then::

    ./run_functional_tests.sh -id blast_reciprocal_best_hits

You will need to have the NCBI BLAST+ binaries installed and on the ``$PATH``.


History
=======

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.1.0  - Initial Test Tool Shed release, targetting NCBI BLAST+ 2.2.29
v0.1.1  - Supports self-comparison, sometimes useful for spotting duplicates.
v0.1.2  - Using optparse for command line API.
        - Fixed Tool Shed dependency definition.
======= ======================================================================


Developers
==========

This tool is developed on the following GitHub repository:
https://github.com/peterjc/galaxy_blast/tree/master/tools/blast_rbh

For making the "Galaxy Tool Shed" http://toolshed.g2.bx.psu.edu/ tarball I use
the following command from the Galaxy root folder::

    $ tar -czf blast_rbh.tar.gz tools/blast_rbh/README.rst tools/blast_rbh/blast_rbh.xml tools/blast_rbh/blast_rbh.py tools/blast_rbh/tool_dependencies.xml test-data/rhodopsin_nucs.fasta test-data/rhodopsin_proteins.fasta test-data/three_human_mRNA.fasta test-data/four_human_proteins.fasta test-data/k12_edited_proteins.fasta test-data/k12_ten_proteins.fasta test-data/rbh_megablast_rhodopsin_nucs_vs_three_human_mRNA.tabular test-data/rbh_blastn_three_human_mRNA_vs_rhodopsin_nucs.tabular test-data/rbh_blastp_four_human_vs_rhodopsin_proteins.tabular test-data/rbh_none.tabular test-data/rbh_tblastx_rhodopsin_nucs_vs_three_human_mRNA.tabular test-data/rbh_blastp_k12.tabular test-data/rbh_blastp_k12_self.tabular

Check this worked::

    $ tar -tzf blast_rbh.tar.gz
    tools/blast_rbh/README.rst
    tools/blast_rbh/blast_rbh.xml
    tools/blast_rbh/blast_rbh.py
    tools/blast_rbh/tool_dependencies.xml
    test-data/rhodopsin_nucs.fasta
    test-data/rhodopsin_proteins.fasta
    test-data/three_human_mRNA.fasta
    test-data/four_human_proteins.fasta
    test-data/k12_edited_proteins.fasta
    test-data/k12_ten_proteins.fasta
    test-data/rbh_megablast_rhodopsin_nucs_vs_three_human_mRNA.tabular
    test-data/rbh_blastn_three_human_mRNA_vs_rhodopsin_nucs.tabular
    test-data/rbh_blastp_four_human_vs_rhodopsin_proteins.tabular
    test-data/rbh_none.tabular
    test-data/rbh_tblastx_rhodopsin_nucs_vs_three_human_mRNA.tabular
    test-data/rbh_blastp_k12.tabular
    test-data/rbh_blastp_k12_self.tabular


Licence (MIT)
=============

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
