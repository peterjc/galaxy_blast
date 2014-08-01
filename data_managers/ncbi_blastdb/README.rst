Galaxy Data Manager for NCBI BLAST databases
============================================

Copyright 2014 by Daniel Blankenberg (Penn State University, PA 16802, USA),
and additional contributors. All rights reserved. See the licence text below.

Downloads and populates blastdb data table. This is just a simple example to
demonstrate the use of Data Managers for processing BLAST databases, and
uses the NCBI's ``update_blast.pl`` script internally. See:

Blankenberg et al. (2014) Wrangling Galaxy's reference data
http://dx.doi.org/10.1093/bioinformatics/btu119

This tool is currently available from the Galaxy Test Tool Shed at:
http://testtoolshed.g2.bx.psu.edu/view/blankenberg/data_manager_example_blastdb_ncbi_update_blastdb


History
=======

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.0.1  - Initial release as an example Data Manager on the Test ToolShed.
        - Depends on ``package_blast_plus_2_2_28`` in ToolShed.
v0.0.2  - Development moved to GitHub, https://github.com/peterjc/galaxy_blast
        - Updated citation information (Blankenberg et al. 2014).
        - Adopted standard MIT License.
        - Now depends on ``package_blast_plus_2_2_29`` in ToolShed.
======= ======================================================================


Bug Reports
===========

You can file an issue here https://github.com/peterjc/galaxy_blast/issues or ask
us on the Galaxy development list http://lists.bx.psu.edu/listinfo/galaxy-dev


Developers
==========

This data manager was originally developed as an example to accompany the
paper Blankenberg et al. (2014), and posted on the Galaxy Test Tool Shed at:
http://testtoolshed.g2.bx.psu.edu/view/blankenberg/data_manager_example_blastdb_ncbi_update_blastdb

As of April 2014, development is continuing within the Galaxy BLAST+ wrapper
repository on GitHub: https://github.com/peterjc/galaxy_blast


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
