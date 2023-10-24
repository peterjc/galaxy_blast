.. image:: https://github.com/peterjc/galaxy_blast/actions/workflows/pr.yaml/badge.svg?branch=master
   :alt: Galaxy Tool Linting and Tests
   :target: https://github.com/peterjc/galaxy_blast/actions/workflows/pr.yaml?query=branch%3Amaster
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Code style: black
   :target: https://github.com/ambv/black

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
NCBI BLAST+ suite.

It also contains additional related Galaxy tools for working with BLAST.

Each of these Galaxy wrappers, tools, etc has its own README file.


Galaxy wrappers for NCBI BLAST+
===============================

The main focus of this work is the development of the NCBI BLAST+ command line
tool wrappers for Galaxy, published on the Galaxy Tool Shed here:

* http://toolshed.g2.bx.psu.edu/view/devteam/ncbi_blast_plus/

Development test releases are on the Test Tool Shed here:

* http://testtoolshed.g2.bx.psu.edu/view/devteam/ncbi_blast_plus/

The associated development is on GitHub at:

* https://github.com/peterjc/galaxy_blast/tree/master/tools/ncbi_blast_plus


Galaxy Datatypes
================

Historically this repository also including the associated Galaxy datatypes,
which are now included and developed within Galaxy itself:

* http://toolshed.g2.bx.psu.edu/view/devteam/blast_datatypes/
* http://testtoolshed.g2.bx.psu.edu/view/devteam/blast_datatypes/
* https://github.com/peterjc/galaxy_blast/tree/master/datatypes/blast_datatypes
* https://github.com/galaxyproject/galaxy/blob/dev/lib/galaxy/datatypes/blast.py


Galaxy Packages
===============

The NCBI BLAST+ binaries were initially included within the Galaxy wrappers
Tool Shed package (``ncbi_blast_plus``), but were then handled as individual
Tool Shed packages:

* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_26
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_27
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_28
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_29
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_30
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_31
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_3_0
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_4_0
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_5_0
* http://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_6_0

However, in line with current Galaxy policy, thereafter we assume Galaxy
will be fetching packages from Conda, specifically the BioConda channel:

* https://anaconda.org/bioconda/blast

Note all of these packages target the NCBI's C++ rewrite of BLAST called BLAST+,
available at ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/ -- we
do not support the now deprecated "legacy" BLAST suite written in C, still
available at ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/


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

Similarly, ``packages`` contains packages for Galaxy Tool Shed dependency
definitions (obsolete), ``datatypes`` contains packages for Galaxy Tool Shed
datatype definitions (obsolete), and ``data_managers`` contains Galaxy Data
Managers for tasks like setting up local copies of NCBI BLAST databases
(currently unfinished).

All of these child folders contain additional README files, which cover
things like how to install each tool manually or via the Galaxy Tool Shed.

Additionally there is a shared ``test-data`` folder used for functional test
sample data, and a shared ``tool-data`` folder used for configuration files.


Installation
============

The individual Galaxy tools (under the ``tools/`` folder as described above)
must be installed into a Galaxy instance for use.  In general the easiest
and recommended way to do this is via the Galaxy Tool Shed which should
handle the dependencies for you. However, manual installation is possible
as described in the README file of each tool.

Binary dependencies like NCBI BLAST+ are best handled by Galaxy via Conda.
If you opt to install the NCBI BLAST+ simply on the system ``$PATH`` outside
of Galaxy's control, you are giving up full reproducibility as Galaxy has no
control over which version of BLAST+ will be run.

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

In addition we are running the same functional tests via GitHub Actions
whenever this GitHub repository is updated:

.. image:: https://github.com/peterjc/galaxy_blast/actions/workflows/pr.yaml/badge.svg?branch=master
   :alt: Galaxy Tool Linting and Tests
   :target: https://github.com/peterjc/galaxy_blast/actions/workflows/pr.yaml?query=branch%3Amaster

This continuous integration testing simulates an install of these Galaxy Tools,
and their dependencies via Conda. See the files under ``.github/workflows/``
for more technical details.


Bug Reports
===========

You can file an issue here https://github.com/peterjc/galaxy_blast/issues or ask
us on the Galaxy Gitter discussion.


Citation
========

There should be more specific guidance in the README file of each folder,
and in the user-facing help text within the each Galaxy tool. In general,
please cite the following paper:

NCBI BLAST+ integrated into Galaxy.
P.J.A. Cock, J.M. Chilton, B. Gruening, J.E. Johnson, N. Soranzo.
*GigaScience* 2015, 4:39
https://doi.org/10.1186/s13742-015-0080-7


In most cases, you should also cite the NCBI BLAST+ tools:

BLAST+: architecture and applications.
C. Camacho et al. *BMC Bioinformatics* 2009, 10:421.
https://doi.org/10.1186/1471-2105-10-421


License
=======

Please see the README file in each folder, but by default the MIT license is
being used.
