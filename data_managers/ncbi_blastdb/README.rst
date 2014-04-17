Galaxy Data Manager for NCBI BLAST databases
============================================

Copyright 2014 by Daniel Blankenberg (Penn State University, PA 16802, USA),
and additional contributors. All rights reserved. See the licence text below.

Downloads preformatted NCBI BLAST databases and updates ``blastdb`` and
``blastdb_p``  data tables accordingly. Uses the NCBI's ``update_blast.pl``
script internally. See:

Blankenberg et al. (2014) Wrangling Galaxy's reference data
http://dx.doi.org/10.1093/bioinformatics/btu119

This tool is currently available from the Galaxy Test Tool Shed at:
http://testtoolshed.g2.bx.psu.edu/view/blankenberg/data_manager_example_blastdb_ncbi_update_blastdb


Automated Installation
======================

Galaxy should be able to automatically install this Data Manager and its
dependencies from the Galaxy ToolShed.


Manual Installation
===================

This is not recommended except for Data Manager development purposes.

First install and test the BLAST+ wrappers, their ``*.loc`` files, and
the NCBI Perl Script ``update_blastdb.pl``.

Move or copy the following files under the Galaxy ``tools`` folder, the
instructions below assume the ``tools/ncbi_blastdb`` folder is used:

* ``blastdb.xml`` (the Galaxy tool definition)
* ``fetch_blast_db.py`` (Python wrapper script)
* ``README.rst`` (this file)

Inspect the Data Manager settings in ``universe_wsgi.ini`` check the location
of the configuration file ``data_manager_config_file = data_manager_conf.xml``
which you must now edit to include the ``data_manager_conf.xml`` content
provided with this Data Manager.

Note you must alter the ``tool_file`` setting to be a relative path::

    <data_manager tool_file="ncbi_blastdb/blastdb.xml" id="ncbi_blast_plus_update_blastdb">

You will also need to modify the ``tools_conf.xml`` file to tell Galaxy to
offer this Data Manager. At any sensible location, add this line::

    <tool file="ncbi_blastdb/blastdb.xml" />

If you wish to run the unit tests, also add this to ``tools_conf.xml.sample``
and move/copy the ``test-data`` files under Galaxy's ``test-data`` folder.
Then::

    ./run_functional_tests.sh -data_managers -id data_manager_blast_db

That's it.


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
v0.0.3  - Updated ``fetch_blast_db.py`` to use the current date as the ID
        - Tool and script now also updates ``blastdb_p`` data tables as needed
        - Tool and script now also updates ``blastdb_d`` data tables as needed
        - Tool now uses a dropdown menu to select the desired database
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
