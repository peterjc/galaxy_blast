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
NCBI BLAST+ suite, associated datatype definitions for use within Galaxy.
It also contains additional related Galaxy tools for working with BLAST.


Galaxy wrappers for NCBI BLAST+	
===============================

The main focus of this work is the development of the NCBI BLAST+ command line
tool wrappers and datatype definitions for Galaxy, published on the Galaxy
Tool Shed here:
 - http://toolshed.g2.bx.psu.edu/view/devteam/ncbi_blast_plus/
 - http://toolshed.g2.bx.psu.edu/view/devteam/blast_datatypes/

Development test releases are on the Test Tool Shed here:
 - http://testtoolshed.g2.bx.psu.edu/view/peterjc/ncbi_blast_plus/
 - http://testtoolshed.g2.bx.psu.edu/view/devteam/blast_datatypes/

Note this this targets the NCBI's C++ rewrite of BLAST called BLAST+,
available at ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/ -- we
do not support the now deprecated "legacy" BLAST suite written in C, still
available at ftp://ftp.ncbi.nlm.nih.gov/blast/executables/release/


History
=======

These Galaxy BLAST+ wrappers were originally written by Peter Cock and were
incorporated into https://bitbucket.org/galaxy/galaxy-central/
the main Galaxy repository on BitBucket in September 2009, where they were
maintained via pull requests and patches from Peter's repository fork.
https://bitbucket.org/galaxy/galaxy-central/

In August 2010 Dannon Baker from the Galaxy Team migrated the BLAST+ tools
and datatypes to the Galaxy Tool Shed (links above). This was part of a long
term plan to move most tools out of the main Galaxy repository.

Development of the wrappers continued on the 'tools' branch of Peter's
Galaxy fork on BitBucket https://bitbucket.org/peterjc/galaxy-central/
with additional contributions via patches and pull requests.

Recognising the growing number of potential contributors, an informal "Birds
of a Feather" (BoF) http://wiki.galaxyproject.org/Events/GCC2013/BoF/GalaxyBlast
meeting was held in July 2013 during the annual Galaxy Community Conference.
It was agreed to move the code into a dedicated Git repository on GitHub,
with the goal of giving the project a clearer identify and making it easier
for Peter to manage.


Other Galaxy BLAST tools
========================

This repository also contains other BLAST related Galaxy tools, some already
available on the Galaxy Tool Shed:
 - http://toolshed.g2.bx.psu.edu/view/peterjc/blastxml_to_top_descr

Any development test releases are on the Test Tool Shed, for example:
 - http://testtoolshed.g2.bx.psu.edu/view/peterjc/blastxml_to_top_descr


Folder Structure
================

There is one folder for each Tool or Tool Suite released on the Galaxy Tool
Shed, and a shared `test-data` folder used for functional test sample data.


License
=======

Please see the README file in each folder, but by default the MIT license is
being used.
