Galaxy tool to find Reciprocal Best Hits (RBH) from BLAST etc
=============================================================

This tool is copyright 2011-2014 by Peter Cock, The James Hutton Institute
(formerly SCRI, Scottish Crop Research Institute), UK. All rights reserved.
See the licence text below.

This tool is a short Python script to parse a BLAST tabular file (or similar),
and extract the reciprocal best hits.

This was an experiment. I was also considering supporting BLAST XML as input,
which could require extensions to Galaxy ideally so that the current column
selection parameters can be conditional on tabular input. This would make
it possible to integrate BLAST filtering into this tool - although that
might be better done as a separate tool instead.

This tool has been superceded by an integrated BLAST RBH tool taking two
FASTA files as input instead, see:

* https://toolshed.g2.bx.psu.edu/view/peterjc/blast_rbh
* https://testtoolshed.g2.bx.psu.edu/view/peterjc/blast_rbh
* https://github.com/peterjc/galaxy_blast/tree/master/tools/blast_rbh


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
