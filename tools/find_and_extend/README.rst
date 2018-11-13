Find BLAST matches and retrieve flanking sequence to extend them
================================================================

This tool is copyright 2018 by Peter Cock, The James Hutton Institute
(formerly SCRI, Scottish Crop Research Institute), UK. All rights reserved.
See the licence text below.

This tool is a short Python script to run a BLASTN (megablast) search on a
nucleotide BLAST database, then extract the matching sequences extended by
the desired up- and down-stream flanking region.

The script ``find_and_extend.py`` can be used directly (without Galaxy) as
long as NCBI BLAST+ are Biopython are installed.

It comes with an optional Galaxy tool definition file ``find_and_extend.xml``
allowing the Python script to be run from within Galaxy. It is available
from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/peterjc/find_and_extend


Citation
========

In the absense of a more precise citation, please cite the tool directly,
or if you need to use a formal paper:

P.J.A. Cock, J.M. Chilton, B. Gruening, J.E. Johnson, N. Soranzo (2015).
NCBI BLAST+ integrated into Galaxy.
*GigaScience* 4:39
https://doi.org/10.1186/s13742-015-0080-7

You should also cite the BLAST+ paper:

Christiam Camacho et al. (2009).
BLAST+: architecture and applications.
*BMC Bioinformatics* 15;10:421.
https://doi.org/10.1186/1471-2105-10-421


Automated Installation (into Galaxy)
====================================

Installation via the Galaxy Tool Shed should take care of the Galaxy side of
things, including the dependency the NCBI BLAST+ binaries and Biopython.


Manual Installation (into Galaxy)
=================================

There are just two files to install:

- ``find_and_extend.py`` (the Python script)
- ``find_and_extend.xml`` (the Galaxy tool definition)

The suggested location is in a ``tools/find_and_extend/`` folder. You will then
need to modify the ``tools_conf.xml`` file to tell Galaxy to offer the tool
by adding the line::

    <tool file="find_and_extend/find_and_extend.xml" />

If you want to run the functional tests, copy the sample test files under
sample test files under Galaxy's ``test-data/`` directory. Then::

    ./run_tests.sh -id blast_find_and_extend

You will need to have the NCBI BLAST+ binaries installed and on the ``$PATH``.


History
=======

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.0.1  - Initial Tool Shed release, targetting NCBI BLAST+ 2.7.1
======= ======================================================================


Developers
==========

This tool is developed on the following GitHub repository:
https://github.com/peterjc/galaxy_blast/tree/master/tools/find_and_extend

For pushing a release to the test or main "Galaxy Tool Shed", use the following
Planemo commands (which requires you have set your Tool Shed access details in
``~/.planemo.yml`` and that you have access rights on the Tool Shed)::

    $ planemo shed_update -t testtoolshed --check_diff tools/find_and_extend/
    ...

or::

    $ planemo shed_update -t toolshed --check_diff tools/find_and_extend/
    ...

To just build and check the tar ball, use::

    $ planemo shed_upload --tar_only tools/find_and_extend/
    ...
    $ tar -tzf shed_upload.tar.gz
    tools/find_and_extend/README.rst
    tools/find_and_extend/find_and_extend.py
    tools/find_and_extend/find_and_extend.xml
    tools/find_and_extend/tool_dependencies.xml
    test-data/blastdb.loc
    test-data/rhodopsin_fragment.fasta
    test-data/rhodopsin_fragment_extended.fasta
    test-data/rhodopsin_nucs.fasta
    test-data/rhodopsin_nucs.fasta.nhd
    test-data/rhodopsin_nucs.fasta.nhi
    test-data/rhodopsin_nucs.fasta.nhr
    test-data/rhodopsin_nucs.fasta.nin
    test-data/rhodopsin_nucs.fasta.nog
    test-data/rhodopsin_nucs.fasta.nsd
    test-data/rhodopsin_nucs.fasta.nsi
    test-data/rhodopsin_nucs.fasta.nsq
    test-data/rhodopsin_nucs.fasta.nnd
    test-data/rhodopsin_nucs.fasta.nni


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
