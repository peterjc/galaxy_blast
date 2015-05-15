OBGalaxy tool to extract top BLAST hit descriptions from BLAST XML
================================================================

This tool is copyright 2012-2015 by Peter Cock, The James Hutton Institute
(formerly SCRI, Scottish Crop Research Institute), UK. All rights reserved.
See the licence text below.

This tool is a short Python script to parse a BLAST XML file, and extract the
identifiers with description for the top matches (by default the top 3), and
output these as a simple tabular file along with the query identifiers.

It is available from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/peterjc/blastxml_to_top_descr

This requires the ``blast_datatypes`` repository from the Galaxy Tool Shed
to provide the ``blastxml`` file format definition.


Automated Installation
======================

This should be straightforward, Galaxy should automatically install the
``blast_datatypes`` dependency.


Manual Installation
===================

If you haven't done so before, first install the ``blast_datatypes`` repository.

There are just two files to install (if doing this manually):

- ``blastxml_to_top_descr.py`` (the Python script)
- ``blastxml_to_top_descr.xml`` (the Galaxy tool definition)

The suggested location is in the Galaxy folder ``tools/ncbi_blast_plus/``
next to the NCBI BLAST+ tool wrappers.

You will also need to modify the ``tools_conf.xml`` file to tell Galaxy to offer
the tool. e.g. next to the NCBI BLAST+ tools. Simply add the line::

    <tool file="ncbi_blast_plus/blastxml_to_top_descr.xml" />

If you wish to run the unit tests, alsomove/copy the ``test-data/`` files
under Galaxy's ``test-data/`` folder. Then::

    $ sh run_tests.sh -id blastxml_to_top_descr


History
=======

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.0.1  - Initial version.
v0.0.2  - Since BLAST+ was moved out of the Galaxy core, now have a dependency
          on the ``blast_datatypes`` repository in the Tool Shed.
v0.0.3  - Include the test files required to run the unit tests
v0.0.4  - Quote filenames in case they contain spaces (internal change)
v0.0.5  - Include number of queries with BLAST matches in stdout (peek text)
v0.0.6  - Check for errors via the script's return code (internal change)
v0.0.7  - Link to Tool Shed added to help text and this documentation.
        - Tweak dependency on ``blast_datatypes`` to also work on Test Tool Shed
        - Adopt standard MIT License.
v0.0.8  - Development moved to GitHub, https://github.com/peterjc/galaxy_blast
v0.0.9  - Updated citation information (Cock et al. 2013).
v0.0.10 - Update help text to mention BLAST+ 2.2.28 can produce tabular files
          including the description/title (via the salltitles field).
v0.1.0  - Switch to using an optparse based API for Python script internally.
        - Support BLAST XML with multiple ``<Iteration>`` blocks per query.
        - Support the default 25 column extended tabular BLAST output.
v0.1.1  - Embed citation information in the tool XML (new Galaxy feature).
v0.1.2  - Reorder XML elements (internal change only).
        - Planemo for Tool Shed upload (``.shed.yml``, internal change only).
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

For pushing a release to the test or main "Galaxy Tool Shed", use the following
Planemo commands (which requires you have set your Tool Shed access details in
``~/.planemo.yml`` and that you have access rights on the Tool Shed)::

    $ planemo shed_upload --shed_target testtoolshed --check_diff ~/repositories/galaxy_blast/tools/blastxml_to_top_descr/
    ...

or::

    $ planemo shed_upload --shed_target toolshed --check_diff ~/repositories/galaxy_blast/tools/blastxml_to_top_descr/
    ...

To just build and check the tar ball, use::

    $ planemo shed_upload --tar_only  ~/repositories/galaxy_blast/tools/blastxml_to_top_descr/
    ...
    $ tar -tzf shed_upload.tar.gz 
    test-data/blastp_four_human_vs_rhodopsin.xml
    test-data/blastp_four_human_vs_rhodopsin_converted_ext.tabular
    test-data/blastp_four_human_vs_rhodopsin_top3.tabular
    test-data/blastp_four_human_vs_rhodopsin_top3_positive.tabular
    tools/blastxml_to_top_descr/README.rst
    tools/blastxml_to_top_descr/blastxml_to_top_descr.py
    tools/blastxml_to_top_descr/blastxml_to_top_descr.xml
    tools/blastxml_to_top_descr/repository_dependencies.xml


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
