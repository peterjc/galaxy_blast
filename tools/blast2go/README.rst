Galaxy wrapper for Blast2GO for pipelines, b2g4pipe
===================================================

This wrapper is copyright 2011-2015 by Peter Cock, The James Hutton Institute
(formerly SCRI, Scottish Crop Research Institute), UK. All rights reserved.
See the licence text below (MIT licence).

This is a wrapper for the command line Java tool b2g4pipe v2.5, Blast2GO for
pipelines, currently a free to use download available at:
http://www.blast2go.com/data/blast2go/b2g4pipe_v2.5.zip

Note that this has been superceded by a non-free "Blast2GO Command Line (CLI)":
http://www.blast2go.com/blast2gocli/

This wrapper is freely available from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/peterjc/blast2go


Citation
========

Please cite the following papers:

Peter Cock, Bjoern Gruening, Konrad Paszkiewicz and Leighton Pritchard (2013).
Galaxy tools and workflows for sequence analysis with applications
in molecular plant pathology. PeerJ 1:e167
http://dx.doi.org/10.7717/peerj.167

S. Geotz et al. (2008).
High-throughput functional annotation and data mining with the Blast2GO suite.
Nucleic Acids Res. 36(10):3420-3435.
http://dx.doi.org/10.1093/nar/gkn176

A. Conesa and S. Geotz (2008).
Blast2GO: A Comprehensive Suite for Functional Analysis in Plant Genomics.
International Journal of Plant Genomics. 619832.
http://dx.doi.org/10.1155/2008/619832

A. Conesa et al. (2005).
Blast2GO: A universal tool for annotation, visualization and analysis in functional genomics research.
Bioinformatics 21:3674-3676.
http://dx.doi.org/10.1093/bioinformatics/bti610

See also http://www.blast2go.com/


Automated Installation
======================

Installation via the Galaxy Tool Shed should take care of the Galaxy side of
things, including the dependency on ``blast_datatypes`` which defines the
``blastxml`` file format. However, you will also probably need to configure
the Blast2GO property file(s), for example if you have a local Blast2GO
database (which we recommend for speed).


Manual Installation
===================

The main dependency is b2g4pipe which must be installed manually. Also we
strongly recommend installing a local Blast2GO database as well (see the
intructions below about the ``blast2go.loc`` file). At the time of writing,
the last free version is b2g4pipe v2.5 which is available here:

* http://www.blast2go.com/data/blast2go/b2g4pipe_v2.5.zip

You can change the path by setting the ``$B2G4PIPE`` environment variable to
the desired folder, but by default the script looks for the JAR file here::

    /opt/b2g4pipe_v2.5/blast2go.jar

To install the wrapper manually, first install ``blast_datatypes``, then
copy or move the following files under the Galaxy tools folder, e.g. in a
``tools/blast2go/`` folder:

- ``blast2go.xml`` (the Galaxy tool definition)
- ``blast2go.py`` (the Python wrapper script)
- ``massage_xml_for_blast2go.py`` (Python BLAST XML reformatting script)
- ``README.rst`` (this file)

For a manual installation of the wrapper you will also need to modify the
``tools_conf.xml`` file to tell Galaxy to offer the tool. We suggest putting
it next to the NCBI BLAST+ wrappers. Just add the line::

  <tool file="blast2go/blast2go.xml" />

If you wish to run the unit tests, also move/copy the ``test-data/`` files
under Galaxy's ``test-data/`` folder. Then::

    $ ./run_tests.sh -id blast2go


Configuration
=============

As part of setting up b2g4pipe you will need to setup one or more Blast2GO
property files which tell the tool which database to use etc. The example
``b2gPipe.properties`` provided with b2g4pipe is now out of date. The current
server IP address and database name may given on the Blast2GO website, or
can be found by running the latest GUI version via Java web-start, and
looking under the tools/options menu. These property files can be anywhere
accessable to the Galaxy Unix user, we put them with the JAR file etc.

You must tell Galaxy about these Blast2GO property files so that they can
be offered to the user. Copy file ``blast2go.loc.sample`` to
``tool-data/blast2go.loc`` under the Galaxy folder and edit this to match
your installation. This must be plain text, tab separated, with three columns:

1. ID for the setup, e.g. ``Spain_2012_August``
2. Description for the setup, e.g. ``Database in Spain (August 2012)``
3. Properties filename for the setup, e.g. ``Spain_2012_August.properties``
   relative to the main JAR file, or with a full path
   e.g. ``/opt/b2g4pipe/Spain_2012_August.properties``

Avoid including "Blast2GO" in the description (column 2) as this text will be
included in the automatically assigned output dataset name. The ``blast2go.loc``
file allows you to customise the database setup. If for example you have a local
Blast2GO server running (which we recommend for speed), and you want this to be
the default setting, include it as the first line in your ``blast2go.loc`` file.

Consult the Blast2GO documentation for details about the property files and
setting up a local MySQL Blast2GO database. e.g.
https://www.blast2go.com/b2gsupport/resources/35-localb2gdb



History
=======

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.0.1  - Initial public release
v0.0.2  - Documentation clarifications, e.g. concatenated BLAST XML is allowed.
        - Fixed error handler in wrapper script (for when b2g4pipe fails).
        - Reformats the XML to use old NCBI-style concatenated BLAST XML since
          b2g4pipe crashes with heap space error on with large files using
          current NCBI output.
v0.0.3  - Include sample loc file, ``tool-data/blast2go.loc.sample``
v0.0.4  - Include ``repository_dependencies.xml`` file for ``blastxml`` format
          (previously included in the core Galaxy installation)
v0.0.5  - Quote arguments in case of spaces in filenames (internal change)
        - Last release supporting b2g4pipe v2.3.5
v0.0.6  - Support for b2g4pipe v2.5 instead of v2.3.5

          - Now invoked with a class path and es.blast2go.prog.B2GAnnotPipe
            rather then simply calling the jar file
          - Now uses the switch ``-annot`` instead of ``-a`` (this change
            breaks support for b2g4pipe v2.3.5 unfortunately)

        - Catch a few error messages and treat them explicitly as errors.
v0.0.7  - Update output description in XML file (b2g4pipe v2.3.5 included
          the sequence description, b2g4pipe v2.5 omits this).
v0.0.8  - Automated installation via the Galaxy Tool Shed.
        - Added unit test.
        - Explain how to load the tabular file into the Blast2GO GUI.
        - Link to Tool Shed added to help text and this documentation.
        - Switch to standard MIT licence.
        - Use reStructuredText for this README file.
        - Updated citation information (Cock et al. 2013).
        - Development moved to GitHub, https://github.com/peterjc/galaxy_blast
        - Split out ``massage_xml_for_blast2go.py`` as a standalone file.
v0.0.9  - Update README file now that BioBam are selling the latest version
          of the Blast2GO command line tool. For now b2g4pipe v2.5 is still
          available as a free download.
        - Tool definition now embeds citation information.
v0.0.10 - Reorder XML elements (internal change only).
        - Planemo for Tool Shed upload (``.shed.yml``, internal change only).
======= ======================================================================


Developers
==========

This script and related tools were originally developed on the 'tools' branch
of the following BitBucket Mercurial repository:
https://bitbucket.org/peterjc/galaxy-central/

As of September 2013, development is continuing on a dedicated GitHub repository:
https://github.com/peterjc/galaxy_blast

For pushing a release to the test or main "Galaxy Tool Shed", use the following
Planemo commands (which requires you have set your Tool Shed access details in
``~/.planemo.yml`` and that you have access rights on the Tool Shed)::

    $ planemo shed_update -t testtoolshed --check_diff ~/repositories/galaxy_blast/tools/blast2go/
    ...

or::

    $ planemo shed_update -t toolshed --check_diff ~/repositories/galaxy_blast/tools/blast2go/
    ...

To just build and check the tar ball, use::

    $ planemo shed_upload --tar_only  ~/repositories/galaxy_blast/tools/blast2go/
    ...
    $ tar -tzf shed_upload.tar.gz 
    test-data/blastp_sample.blast2go.tabular
    test-data/blastp_sample.xml
    tool-data/blast2go.loc.sample
    tools/blast2go/README.rst
    tools/blast2go/blast2go.py
    tools/blast2go/blast2go.xml
    tools/blast2go/massage_xml_for_blast2go.py
    tools/blast2go/repository_dependencies.xml
    tools/blast2go/tool_dependencies.xml



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


NOTE: This is the licence for the Galaxy Wrapper only. Blast2GO and
associated data files are available and licenced separately.
