Galaxy datatypes for NCBI BLAST+ suite
======================================

These Galaxy datatypes are copyright 2010-2014 by Peter Cock (The James Hutton
Institute, UK) and additional contributors including Edward Kirton, Nicola
Soranzo, and Bjoern Gruening.

See the licence text below.

Note that these files (and the associated BLAST+ wrappers) were originally
distributed as part of the main Galaxy repository, but as of August 2012 moved
to the Galaxy Tool Shed as 'blast_datatypes' (and 'ncbi_blast_plus' for the
wrappers). My thanks to Dannon Baker from the Galaxy development team for his
assistance with this.

It is available from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/devteam/blast_datatypes


History
=======

These versions numbers initially matched those for 'ncbi_blast_plus', but are
not used explicitly in the datatypes themselves.

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.0.11 - Final revision as part of the Galaxy main repository, and the
          first release via the Tool Shed
v0.0.13 - Uses ``blast.py`` instead of ``xml.py`` to define the datatypes
v0.0.14 - Includes datatypes for protein and nucleotide BLAST databases
          (``blastdbp`` and ``blastdbn``, based on work by Edward Kirton)
v0.0.15 - Fixes a MetadataElement bug and includes more of the optional
          BLAST database files (contribution from Nicola Soranzo)
v0.0.16 - Adopt standard MIT License.
        - Use reStructuredText for this README file.
        - Development moved to GitHub, https://github.com/peterjc/galaxy_blast
        - Nucleotide database definition aware of MegaBLAST index superheader
v0.0.17 - Add ``maskinfo-asn1`` and ``maskinfo-asn1-binary`` sub-datatypes
          (contribution from Nicola Soranzo)
v0.0.18 - Add retries to BLAST XML merge code.
        - Modify display_data method to allow unit tests to function.
v0.0.19 - Add ``blastdbp`` datatype for BLAST protein domain databases, for use
          with makeprofiledb and rpsblast (contribution from Bjoern Gruening).
        - Add ``pssm-asn1`` datatype for Position Specific Scoring Matrices
          (PSSMs) stored in NCBI's "scoremat" ASN.1 format (usually named
          as *.smp), used as input files for makeprofiledb.
======= ======================================================================


Installation
============

Doing this automatically via the Galaxy Tool Shed is probably simplest.


Manual Installation
===================

Normally you would install this via the Galaxy ToolShed, which would move
the provided ``blast.py`` file into a suitable location and process the
``datatypes_conf.xml`` entries to be combined with your local configuration.

However, if you really want to this should work for a manual install. First
update the ``datatypes_conf.xml`` file in the Galaxy main folder by inserting
the contents of the ``<registration>`` and ``<sniffers>`` sections from the
small ``datatypes_conf.xml`` file provided in the tar-ball.

For the ``<registration>`` section you would add several ``<datatype ... />``
lines, one per new datatype::

    <datatype extension="blastxml" type="galaxy.datatypes.blast:BlastXml" mimetype="application/xml" display_in_upload="true"/>
    ...

Similarly, some of the new dataypes have ``<sniffer ... />`` lines used to
automatically recognise the datatype when uploaded into Galaxy::

    <sniffer type="galaxy.datatypes.blast:BlastXml"/>
    ...

Also create the file ``lib/galaxy/datatypes/blast.py`` by moving, copying or linking
the ``blast.py`` file provided in this tar-ball.  Finally add ``import blast`` near
the start of file ``lib/galaxy/datatypes/registry.py`` (after the other import
lines).


Bug Reports
===========

You can file an issue here https://github.com/peterjc/galaxy_blast/issues or ask
us on the Galaxy development list http://lists.bx.psu.edu/listinfo/galaxy-dev


Developers
==========

These BLAST+ datatypes and associated tools were originally developed on the
following hg branch: http://bitbucket.org/peterjc/galaxy-central/src/tools

As of July 2013, development is continuing on a dedicated GitHub repository:
https://github.com/peterjc/galaxy_blast

For making the "Galaxy Tool Shed" http://toolshed.g2.bx.psu.edu/ tarball I use
the following command from the ``blast_datatypes`` folder::

    $ tar -czf blast_datatypes.tar.gz README.rst datatypes_conf.xml blast.py

Check this worked::

    $ tar -tzf blast_datatypes.tar.gz
    README.rst
    datatypes_conf.xml
    blast.py

For development, rather than having a local ToolShed running, I currently
use a symlink from ``lib/galaxy/datatypes/blast.py`` to the actual file as
described above.


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

NOTE: This is the licence for the Galaxy BLAST datatypes **only**. BLAST+
and associated data files are available and licenced separately.
