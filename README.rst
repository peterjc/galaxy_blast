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

This repository is for the development of the main Galaxy wrappers for the
NCBI BLAST+ suite, associated datatype definitions for use within Galaxy,
and dependency handling within the Galaxy Tool Shed framework.

It also contains additional related Galaxy tools for working with BLAST.

Each of these Galaxy wrappers, tools, datatypes, etc has its own README
file.


Galaxy wrappers for NCBI BLAST+	
===============================

The main focus of this work is the development of the NCBI BLAST+ command line
tool wrappers and datatype definitions for Galaxy, published on the Galaxy
Tool Shed here:

* http://toolshed.g2.bx.psu.edu/view/devteam/ncbi_blast_plus/
* http://toolshed.g2.bx.psu.edu/view/devteam/blast_datatypes/

Development test releases are on the Test Tool Shed here:

* http://testtoolshed.g2.bx.psu.edu/view/peterjc/ncbi_blast_plus/
* http://testtoolshed.g2.bx.psu.edu/view/devteam/blast_datatypes/

The associated development is on GitHub at:

* https://github.com/peterjc/galaxy_blast/tree/master/tools/ncbi_blast_plus
* https://github.com/peterjc/galaxy_blast/tree/master/datatypes/blast_datatypes

The NCBI BLAST+ binaries were initially included within the Galaxy wrappers
(ncbi_blast_plus), but are now handled as Tool Shed packages:

* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_26
* http://testtoolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_26
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_27
* http://testtoolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_27
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_28
* http://testtoolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_28
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_29
* http://testtoolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_29
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_30
* http://testtoolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_30

Note this targets the NCBI's C++ rewrite of BLAST called BLAST+,
available at ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/ -- we
do not support the now deprecated "legacy" BLAST suite written in C, still
available at ftp://ftp.ncbi.nlm.nih.gov/blast/executables/release/


History
=======

These Galaxy BLAST+ wrappers were originally written by Peter Cock and were
incorporated into https://bitbucket.org/galaxy/galaxy-central/
the main Galaxy repository on BitBucket in September 2009, where they were
maintained via pull requests and patches from Peter's repository fork:
https://bitbucket.org/galaxy/galaxy-central/

In August 2012 Dannon Baker from the Galaxy Team migrated the BLAST+ tools
and datatypes to the Galaxy Tool Shed (links above). This was part of a long
term plan to move most tools out of the main Galaxy repository. Development
of the wrappers continued on the 'tools' branch of Peter's Galaxy fork on
BitBucket with additional contributions via patches and pull requests.

Recognising the growing number of potential contributors, an informal "Birds
of a Feather" (BoF) http://wiki.galaxyproject.org/Events/GCC2013/BoF/GalaxyBlast
meeting was held in July 2013 during the annual Galaxy Community Conference.
It was agreed to move the code into a dedicated Git repository on GitHub,
with the goal of giving the project a clearer identity and making it easier
for Peter to manage.


Other Galaxy BLAST tools
========================

This repository also contains other BLAST related Galaxy tools, some already
available on the Galaxy Tool Shed:

* http://toolshed.g2.bx.psu.edu/view/peterjc/blast_rbh
* http://toolshed.g2.bx.psu.edu/view/peterjc/blastxml_to_top_descr
* http://toolshed.g2.bx.psu.edu/view/peterjc/blast2go

Any development test releases are on the Test Tool Shed, for example:

* http://testtoolshed.g2.bx.psu.edu/view/peterjc/blast_rbh
* http://testtoolshed.g2.bx.psu.edu/view/peterjc/blastxml_to_top_descr
* http://testtoolshed.g2.bx.psu.edu/view/peterjc/blast2go


Folder Structure
================

Within the ``tools`` folder is one folder for each Tool or Tool Suite released
on the Galaxy Tool Shed (these child folder names match the Tool Shed names).

Similarly, ``dependencies`` contains packages for Galaxy Tool Shed dependency
definitions, ``datatypes`` contains packages for Galaxy Tool Shed datatype
definitions, and ``data_managers`` contains Galaxy Data Managers for tasks
like setting up local copies of NCBI BLAST databases (currently unfinished).

All of these child folders contain additional README files, which cover
things like how to install each tool manually or via the Galaxy Tool Shed.

Additionally there is a shared ``test-data`` folder used for functional test
sample data, and a shared ``tool-data`` folder used for configuration files.


Installation
============

The individual Galaxy tools (under the ``tools/`` folder as descibed above)
must be installed into a Galaxy instance for use.  In general the easiest
and recommended way to do this is via the Galaxy Tool Shed which should
handle the dependencies for you. However, manual installation is possible
as described in the README file of each tool.

Binary dependencies like NCBI BLAST+ have been packaged for the Galaxy
ToolShed (links given above), and installing via the Tool Shed allow
multiple versions to be available under Galaxy's control for full
reproducibility.  If you opt to install the NCBI BLAST+ simply on the
system ``$PATH`` outside of Galaxy's control, you are giving up full
reproducibility as Galaxy has no control over which version of BLAST+
will be run.

If you wish to use pre-existing BLAST databases, either local to your
institute or from the NCBI BLAST databases FTP site, they must currently be
managed by the Galaxy Administrator manually via the ``blastdb*.loc``
configuration files. In many cases, your system administrator may already
have automatically updated NCBI BLAST database available centrally. In this
case, telling Galaxy to use these is a simple solution, but gives up full
reproducibilty as there is only a single "live" version of each database.

Note that individual Galaxy users may also create their own databases
within Galaxy from FASTA files using the ``makeblastdb`` wrapper.


Testing
=======

Most of these Galaxy tools include a <tests> section in the tool XML files,
which defines one or more functional tests - listing sample input files and
user parameters, along with the expected output. If you install the tools,
you can run these tests via Galaxy's ``run_tests.sh`` script - and/or do
this automatically if installing the tools via the Tool Shed. See the
README file for each tool for more details.

The Galaxy team run regular tests on all the tools which have been uploaded
to the main Tool Shed and the Test Tool Shed, simulating how they would
behave in a local Galaxy instance once installed via the Tool Shed.

In addition we are running the same functional tests via TravisCI whenever
this GitHub repository is updated:

.. image:: https://travis-ci.org/peterjc/galaxy_blast.png?branch=master
   :alt: Current status of TravisCI build for master branch
   :target: https://travis-ci.org/peterjc/galaxy_blast/builds

This TravisCI integration simulates a manual install of these Galaxy Tools
and their dependencies. See the special ``.travis.yml`` file for more
technical details.


Bug Reports
===========

You can file an issue here https://github.com/peterjc/galaxy_blast/issues or ask
us on the Galaxy development list http://lists.bx.psu.edu/listinfo/galaxy-dev


License
=======

Please see the README file in each folder, but by default the MIT license is
being used.
