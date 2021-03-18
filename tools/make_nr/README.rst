Make a FASTA file non-redundant, with a Galaxy wrapper
======================================================

This tool is copyright 2018 by Peter Cock, The James Hutton Institute, UK.
All rights reserved. See the licence text below.

This tool is a short Python script intended to be run prior to calling
the NCBI BLAST+ command line tool ``makeblastdb`` or in other settings
where you want to collapse duplicated sequences in a FASTA file to a
single representative.

The script ``make_nr.py`` can be used directly (without Galaxy).
It requires Biopython.

It comes with an optional Galaxy tool definition file ``make_nr.xml``
allowing the Python script to be run from within Galaxy. It is available
from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/peterjc/make_nr


Citation
========

If you cannot cite the GitHub repository directly, please cite one of the
following papers:

Cock et al 2009. Biopython: freely available Python tools for computational
molecular biology and bioinformatics. *Bioinformatics* 25(11) 1422-3.
https://doi.org/10.1093/bioinformatics/btp163 pmid:19304878.

or (and this would be more appropriate in a Galaxy setting):

NCBI BLAST+ integrated into Galaxy.
P.J.A. Cock, J.M. Chilton, B. Gruening, J.E. Johnson, N. Soranzo
*GigaScience* 2015, 4:39
https://doi.org/10.1186/s13742-015-0080-7


Standalone Installation (outside Galaxy)
========================================

Outside of Galaxy, you will need Python and Biopython, the later can usually
be installed with ``pip install biopython`` or if you are using Conda, try
``conda install biopython`` instead. Then to run the script, simply call it
using ``python /full/path/to/make_nr.py -h`` or similar.


Automated Installation
======================

Installation via the Galaxy Tool Shed should take care of the Galaxy side of
things, including the dependency on Biopython.


Manual Installation
===================

There are just two files to install:

- ``make_nr.py`` (the Python script)
- ``make_nr.xml`` (the Galaxy tool definition)

The suggested location is in a ``tools/make_nr/`` folder. You will then
need to modify the ``tools_conf.xml`` file to tell Galaxy to offer the tool
by adding the line::

    <tool file="make_nr/make_nr.xml" />

If you want to run the functional tests, copy the sample test files under
sample test files under Galaxy's ``test-data/`` directory. Then::

    ./run_tests.sh -id make_nr


History
=======

TODO:

 - Option to follow BLAST NR style with ctrl+a separator?
 - Option to give representative sequences in upper case?

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.0.2  - Fixed bug writing files when there were no duplicates
v0.0.1  - Added option to sort merged IDs, and support for gzipped files
v0.0.0  - Initial version (not published to main Galaxy Tool Shed)
======= ======================================================================


Developers
==========

This tool is developed on the following GitHub repository:
https://github.com/peterjc/galaxy_blast/tree/master/tools/make_nr

For pushing a release to the test or main "Galaxy Tool Shed", use the following
Planemo commands (which requires you have set your Tool Shed access details in
``~/.planemo.yml`` and that you have access rights on the Tool Shed)::

    $ planemo shed_update -t testtoolshed --check_diff tools/make_nr/
    ...

or::

    $ planemo shed_update -t toolshed --check_diff tools/make_nr/
    ...

To just build and check the tar ball, use::

    $ planemo shed_upload --tar_only tools/make_nr/
    ...
    $ tar -tzf shed_upload.tar.gz
    tools/make_nr/README.rst
    tools/make_nr/make_nr.py
    tools/make_nr/make_nr.xml
    tools/make_nr/tool_dependencies.xml
    test-data/duplicates.fasta
    test-data/duplicates.nr.fasta


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
