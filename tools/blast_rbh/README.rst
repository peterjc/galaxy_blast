Find BLAST Reciprocal Best Hits (RBH), with Galaxy wrapper
==========================================================

This tool is copyright 2011-2017 by Peter Cock, The James Hutton Institute
(formerly SCRI, Scottish Crop Research Institute), UK. All rights reserved.
See the licence text below.

This tool is a short Python script to run reciprocal BLAST searches on a
pair of sequence files, and extract the reciprocal best hits. The script
``blast_rbh.py`` can be used directly (without Galaxy) as long as NCBI
BLAST+ is installed.

It comes with an optional Galaxy tool definition file ``blast_rbh.xml``
allowing the Python script to be run from within Galaxy. It is available
from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/peterjc/blast_rbh


Citation
========

Please cite the following paper:

NCBI BLAST+ integrated into Galaxy.
P.J.A. Cock, J.M. Chilton, B. Gruening, J.E. Johnson, N. Soranzo
*GigaScience* 2015, 4:39
https://doi.org/10.1186/s13742-015-0080-7

You should also cite the NCBI BLAST+ tools:

BLAST+: architecture and applications.
C. Camacho et al. *BMC Bioinformatics* 2009, 10:421.
https://doi.org/10.1186/1471-2105-10-421


Automated Installation
======================

Installation via the Galaxy Tool Shed should take care of the Galaxy side of
things, including the dependency the NCBI BLAST+ binaries.


Manual Installation
===================

There are just three files to install:

- ``blast_rbh.py`` (the Python script)
- ``best_hits.py`` (helper script, put in same directory)
- ``blast_rbh.xml`` (the Galaxy tool definition)

The suggested location is in a ``tools/blast_rbh/`` folder. You will then
need to modify the ``tools_conf.xml`` file to tell Galaxy to offer the tool
by adding the line::

    <tool file="blast_rbh/blast_rbh.xml" />

If you want to run the functional tests, copy the sample test files under
sample test files under Galaxy's ``test-data/`` directory. Then::

    ./run_tests.sh -id blast_reciprocal_best_hits

You will need to have the NCBI BLAST+ binaries installed and on the ``$PATH``.


History
=======

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.1.0  - Initial Test Tool Shed release, targetting NCBI BLAST+ 2.2.29
v0.1.1  - Supports self-comparison, sometimes useful for spotting duplicates.
v0.1.2  - Using optparse for command line API.
        - Tool definition now embeds citation information.
        - Fixed Tool Shed dependency definition.
v0.1.3  - Option to make FASTA files non-redundant (via Biopython dependency).
        - Avoid extra database and BLAST search in self-comparison mode.
v0.1.4  - Check for duplicate FASTA identifiers (workaround for makeblastdb
          not treating this as an error, leading to confusing RBH output).
v0.1.5  - Clarify documentation for using the Python script outside Galaxy.
        - Updated to depend on NCBI BLAST+ 2.2.30 via ToolShed install.
v0.1.6  - Offer the new blastp-fast task added in BLAST+ 2.2.30.
        - Added "NCBI BLAST+ integrated into Galaxy" preprint citation.
v0.1.7  - Reorder XML elements (internal change only).
        - Planemo for Tool Shed upload (``.shed.yml``, internal change only).
        - Updated citation information with GigaScience paper.
v0.1.8  - Updated to depend on NCBI BLAST+ 2.2.31 via ToolShed install.
v0.1.9  - Updates to the command line API for the Python script.
        - PEP8 style updates to the Python script (internal change only).
        - Fix parameter help text which was not being displayed.
v0.1.11 - Updated to depend on NCBI BLAST+ 2.5.0 via ToolShed or BioConda.
        - Update Biopython dependency.
        - Tweak Python script to work under Python 2 or Python 3.
v0.1.12 - Use ``<command detect_errors="aggressive">`` (internal change only).
        - Single quote command line arguments (internal change only).
v0.2.0  - Refactored to use more than one Python file (internal change only).
======= ======================================================================


Developers
==========

This tool is developed on the following GitHub repository:
https://github.com/peterjc/galaxy_blast/tree/master/tools/blast_rbh

For pushing a release to the test or main "Galaxy Tool Shed", use the following
Planemo commands (which requires you have set your Tool Shed access details in
``~/.planemo.yml`` and that you have access rights on the Tool Shed)::

    $ planemo shed_update -t testtoolshed --check_diff tools/blast_rbh/
    ...

or::

    $ planemo shed_update -t toolshed --check_diff tools/blast_rbh/
    ...

To just build and check the tar ball, use::

    $ planemo shed_upload --tar_only tools/blast_rbh/
    ...
    $ tar -tzf shed_upload.tar.gz
    test-data/four_human_proteins.fasta
    test-data/k12_edited_proteins.fasta
    test-data/k12_ten_proteins.fasta
    test-data/rbh_blastn_three_human_mRNA_vs_rhodopsin_nucs.tabular
    test-data/rbh_blastp_four_human_vs_rhodopsin_proteins.tabular
    test-data/rbh_blastp_k12.tabular
    test-data/rbh_blastp_k12_self.tabular
    test-data/rbh_megablast_rhodopsin_nucs_vs_three_human_mRNA.tabular
    test-data/rbh_none.tabular
    test-data/rbh_tblastx_rhodopsin_nucs_vs_three_human_mRNA.tabular
    test-data/rhodopsin_nucs.fasta
    test-data/rhodopsin_proteins.fasta
    test-data/three_human_mRNA.fasta
    tools/blast_rbh/README.rst
    tools/blast_rbh/blast_rbh.py
    tools/blast_rbh/blast_rbh.xml
    tools/blast_rbh/tool_dependencies.xml


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
