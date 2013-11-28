Galaxy tool to extract top BLAST hit descriptions from BLAST XML
================================================================

This tool is copyright 2012-2013 by Peter Cock, The James Hutton Institute
(formerly SCRI, Scottish Crop Research Institute), UK. All rights reserved.
See the licence text below.

This tool is a short Python script to parse a BLAST XML file, and extract the
identifiers with description for the top matches (by default the top 3), and
output these as a simple tabular file along with the query identifiers.

It is available from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/peterjc/blastxml_to_top_descr

This requires the 'blast_datatypes' repository from the Galaxy Tool Shed
to provide the 'blastxml' file format definition.


Automated Installation
======================

This should be straightforward, Galaxy should automatically install the
'blast_datatypes' dependency.


Manual Installation
===================

If you haven't done so before, first install the 'blast_datatypes' repository.

There are just two files to install (if doing this manually):

* blastxml_to_top_descr.py (the Python script)
* blastxml_to_top_descr.xml (the Galaxy tool definition)

The suggested location is in the Galaxy folder tools/ncbi_blast_plus next to
the NCBI BLAST+ tool wrappers.

You will also need to modify the tools_conf.xml file to tell Galaxy to offer
the tool. e.g. next to the NCBI BLAST+ tools. Simply add the line::

    <tool file="ncbi_blast_plus/blastxml_to_top_descr.xml" />

To run the tool's tests, also add this line to tools_conf.xml.sample then::

    $ sh run_functional_tests.sh -id blastxml_to_top_descr


History
=======

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.0.1  - Initial version.
v0.0.2  - Since BLAST+ was moved out of the Galaxy core, now have a dependency
          on the 'blast_datatypes' repository in the Tool Shed.
v0.0.3  - Include the test files required to run the unit tests
v0.0.4  - Quote filenames in case they contain spaces (internal change)
v0.0.5  - Include number of queries with BLAST matches in stdout (peek text)
v0.0.6  - Check for errors via the script's return code (internal change)
v0.0.7  - Link to Tool Shed added to help text and this documentation.
        - Tweak dependency on blast_datatypes to also work on Test Tool Shed
        - Adopt standard MIT License.
v0.0.8  - Development moved to GitHub, https://github.com/peterjc/galaxy_blast
v0.0.9  - Updated citation information (Cock et al. 2013).
v0.0.10 - Update help text to mention BLAST+ 2.2.28 can produce tabular files
          including the description/title (via the salltitles field).
======= ======================================================================


Bug Reports
===========

You can file an issue here https://github.com/peterjc/galaxy_blast/issues or ask
us on the Galaxy development list http://lists.bx.psu.edu/listinfo/galaxy-dev


Developers
==========

This script and related tools were originally developed on the 'tools' branch of
the following Mercurial repository: https://bitbucket.org/peterjc/galaxy-central/

As of July 2013, development is continuing on a dedicated GitHub repository:
https://github.com/peterjc/galaxy_blast

For making the "Galaxy Tool Shed" http://toolshed.g2.bx.psu.edu/ tarball use
the following command from the GitHub repository root folder::

    $ tar -czf blastxml_to_top_descr.tar.gz tools/blastxml_to_top_descr/README.rst tools/blastxml_to_top_descr/blastxml_to_top_descr.* tools/blastxml_to_top_descr/repository_dependencies.xml test-data/blastp_four_human_vs_rhodopsin.xml test-data/blastp_four_human_vs_rhodopsin_top3.tabular

Check this worked::

    $ tar -tzf blastxml_to_top_descr.tar.gz
    tools/blastxml_to_top_descr/README.rst
    tools/blastxml_to_top_descr/blastxml_to_top_descr.py
    tools/blastxml_to_top_descr/blastxml_to_top_descr.xml
    tools/blastxml_to_top_descr/repository_dependencies.xml
    test-data/blastp_four_human_vs_rhodopsin.xml
    test-data/blastp_four_human_vs_rhodopsin_top3.tabular


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
